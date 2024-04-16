import abc
import os

import pandas as pd
import psycopg2
import psycopg2.extras
from logger.colored_logger import ColoredLogger

logger = ColoredLogger(logger_name=__name__).get_logger()


class DBDataProcessor(abc.ABC):
    def __init__(self, table_name, config):
        self.dataframe = None
        self.table_name = table_name
        self.conf = config

        # debug options for pandas dataframe
        pd.options.display.max_colwidth = 500
        pd.options.display.max_columns = 50
        pd.options.display.max_rows = 200
        pd.options.display.width = 2000

    @staticmethod
    def check_db_objects(cur):
        logger.info("Checking DB objects ...")
        cur.execute(
            """
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
            AND table_type = 'BASE TABLE'
            ORDER BY 1,2;
        """
        )
        tables = cur.fetchall()
        for tab in tables:
            logger.info(f"Schema: {tab[0]}, Table: {tab[1]}")

    @staticmethod
    def dataframe_to_tuples(df):
        return [tuple(x) for x in df.to_numpy()]

    def load_df_to_postgres(self, reg_uuid=False):
        logger.info("Preparing data to loading ...")
        conn = None
        tuples = self.dataframe_to_tuples(self.dataframe)
        columns = ",".join(list(self.dataframe.columns))
        placeholders = ",".join(["%s"] * len(self.dataframe.columns))
        query = f'INSERT INTO "{self.table_name}" ({columns}) VALUES ({placeholders})'

        def is_table_empty(cursor, table_name):
            cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
            return cursor.fetchone()[0] == 0

        logger.info("Start loading data to the database")
        try:
            conn = psycopg2.connect(
                database=self.conf["db"]["database"],
                user=self.conf["db"]["user"],
                host=self.conf["db"]["host"],
                password=os.getenv("DB_PASS"),
                port=self.conf["db"]["port"],
            )
            cur = conn.cursor()

            if reg_uuid:
                psycopg2.extras.register_uuid()

            self.check_db_objects(cur)

            if not is_table_empty(cur, self.table_name):
                logger.info(
                    f"Truncating table {self.table_name} before inserting new data"
                )
                cur.execute(f'TRUNCATE TABLE "{self.table_name}"')

            logger.info("Start inserting ...")
            for record in tuples:
                cur.execute(query, record)
            conn.commit()
            cur.close()
            logger.info(f"Data loaded to {self.table_name}")
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f"Error: {error}")
        finally:
            if conn is not None:
                conn.close()
