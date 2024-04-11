import os
import random

import pandas as pd
import psycopg2

from DataProcess.scripts.map_countries import countries, months
from logger.colored_logger import ColoredLogger

logger = ColoredLogger(logger_name=__name__).get_logger()


class DummyWeatherData:

    def __init__(self, config):
        self.conf = config

        # debug options for pandas dataframe
        pd.options.display.max_colwidth = 500
        pd.options.display.max_columns = 50
        pd.options.display.max_rows = 200
        pd.options.display.width = 2000

        self.dataframe = self.generate_dummy_data()

    @staticmethod
    def generate_dummy_data():

        data = []
        for country in countries:
            for month in months:
                data.append({
                    'country': country,
                    'month': month,
                    'average_temperature': f"{random.randint(-5, 30)} C",
                    'precipitation_level': random.choice(['Low', 'Medium', 'High']),
                    'air_speed': f"{random.uniform(0.5, 20.0):.1f} m/s",
                    'recommended_to_visit': random.choice(['Yes', 'No'])
                })

        return pd.DataFrame(data)

    @staticmethod
    def dataframe_to_tuples(df):
        return [tuple(x) for x in df.to_numpy()]

    def load_df_to_postgres(self):
        logger.info('Preparing data to loading ...')
        conn = None
        tuples = self.dataframe_to_tuples(self.dataframe)
        columns = ','.join(list(self.dataframe.columns))
        placeholders = ','.join(['%s'] * len(self.dataframe.columns))
        query = f'INSERT INTO "{self.conf["dummy_weather"]["target_table"]}" ({columns}) VALUES ({placeholders})'

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

            if not is_table_empty(cur, self.conf["dummy_weather"]["target_table"]):
                logger.info('Truncating table before inserting new data')
                cur.execute(f'TRUNCATE TABLE "{self.conf["dummy_weather"]["target_table"]}"')

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
