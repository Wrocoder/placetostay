import os

import numpy as np
import pandas as pd
import psycopg2

from logger.colored_logger import ColoredLogger

logger = ColoredLogger(logger_name=__name__).get_logger()


class DataHotelProcessor:
    def __init__(self, config):
        self.conf = config
        self.filename = self.conf['hotels']['source_path']
        self.dataframe = self.load_data()

        # debug options for pandas dataframe
        pd.options.display.max_colwidth = 500
        pd.options.display.max_columns = 50
        pd.options.display.max_rows = 200
        pd.options.display.width = 2000

    def load_data(self):
        logger.info("Loading source csv data ...")
        return pd.read_csv(self.filename, header=None)

    def find_field_names(self):
        new_columns = self.dataframe.iloc[0]
        self.dataframe.columns = new_columns
        self.dataframe = self.dataframe.drop(self.dataframe.index[0])

    def preprocess_cols(self):
        columns_to_convert = ['numberrooms', 'numberfloors', 'yearopened', 'yearrenovated']

        for column in columns_to_convert:
            self.dataframe[column] = pd.to_numeric(self.dataframe[column], errors='coerce').astype('Int64')
            # self.dataframe[column] = self.dataframe[column].replace({np.nan: None})

        columns_to_convert = self.dataframe.columns
        for column in columns_to_convert:
            self.dataframe[column] = self.dataframe[column].replace({np.nan: None})

    @staticmethod
    def calculate_length(x):
        return len(str(x))

    def check_types(self):
        max_length_indices = self.dataframe.apply(lambda col: col.astype(str).map(self.calculate_length).idxmax())
        max_length_values = {col: self.dataframe[col].iloc[max_length_indices[col]] for col in self.dataframe.columns}
        for column, value in max_length_values.items():
            logger.info(f"{column}: {value} (Length: {len(str(value))})")

    @staticmethod
    def dataframe_to_tuples(df):
        return [tuple(x) for x in df.to_numpy()]

    @staticmethod
    def check_db_objects(cur):
        logger.info('Checking DB objects ...')
        cur.execute("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
            AND table_type = 'BASE TABLE'
            ORDER BY 1,2;
        """)
        tables = cur.fetchall()
        for tab in tables:
            logger.info(f"Schema: {tab[0]}, Table: {tab[1]}")

    def load_df_to_postgres(self):
        logger.info('Preparing data to loading ...')
        conn = None
        tuples = self.dataframe_to_tuples(self.dataframe)
        columns = ','.join(list(self.dataframe.columns))
        placeholders = ','.join(['%s'] * len(self.dataframe.columns))
        query = f'INSERT INTO "{self.conf["hotels"]["target_table"]}" ({columns}) VALUES ({placeholders})'

        def is_table_empty(cursor, table_name):
            cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
            return cursor.fetchone()[0] == 0

        logger.info('Start loading data to the database')
        try:
            conn = psycopg2.connect(database=self.conf['db']['database'],
                                    user=self.conf['db']['user'],
                                    host=self.conf['db']['host'],
                                    password=os.getenv('DB_PASS'),
                                    port=self.conf['db']['port'])
            cur = conn.cursor()

            self.check_db_objects(cur)

            if not is_table_empty(cur, self.conf["hotels"]["target_table"]):
                logger.info('Truncating table before inserting new data')
                cur.execute(f'TRUNCATE TABLE "{self.conf["hotels"]["target_table"]}"')

            logger.info('Start inserting ...')
            for record in tuples:
                cur.execute(query, record)
            conn.commit()
            cur.close()
            logger.info('Data loaded')
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f"Error: {error}")
        finally:
            if conn is not None:
                conn.close()
