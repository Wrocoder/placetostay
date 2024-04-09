import os

import numpy as np
import pandas as pd
import psycopg2

from DataProcess.scripts.map_countries import country_mapping, tourism_concept_mapping, translation_dict
from logger.colored_logger import ColoredLogger

logger = ColoredLogger(logger_name=__name__).get_logger()


class DataTourStatProcessor:
    def __init__(self, config):
        self.conf = config
        self.filename = self.conf['stat_tourism']['source_path']
        self.dataframe = self.load_data()

        # debug options for pandas dataframe
        pd.options.display.max_colwidth = 500
        pd.options.display.max_columns = 50
        pd.options.display.max_rows = 200
        pd.options.display.width = 2000

    def load_data(self):
        logger.info("Loading source csv data ...")
        return pd.read_csv(self.filename, sep='\t', header=None)

    def find_field_names(self):
        new_columns = self.dataframe.iloc[0]
        self.dataframe.columns = new_columns
        self.dataframe = self.dataframe.drop(self.dataframe.index[0])

    @staticmethod
    def convert_to_float(value):
        try:
            return float(value.replace('.', ''))
        except ValueError:
            return None

    def preprocess_cols(self):
        # Exclude unnecessary columns
        self.dataframe = self.dataframe[[2, 5, 6, 7]]
        # Applying the translations
        self.dataframe[2] = self.dataframe[2].map(country_mapping)
        self.dataframe[5] = self.dataframe[5].map(tourism_concept_mapping)

        # Renaming columns
        self.find_field_names()
        self.dataframe.rename(columns=translation_dict, inplace=True)
        self.dataframe['total'] = self.dataframe['total'].apply(self.convert_to_float)

        # Exclude rows with Nulls and old data
        columns_to_convert = self.dataframe.columns
        for column in columns_to_convert:
            self.dataframe[column] = self.dataframe[column].replace({np.nan: None})

        self.dataframe = self.dataframe.dropna()
        self.dataframe = self.dataframe[~self.dataframe['period'].str.startswith(('2021', '2020', '2019', '2018'))]

        # find relevant values
        idx = self.dataframe.groupby(['country', 'period'])['total'].idxmax()
        self.dataframe = self.dataframe.loc[idx]

    @staticmethod
    def dataframe_to_tuples(df):
        return [tuple(x) for x in df.to_numpy()]

    def load_df_to_postgres(self):
        logger.info('Preparing data to loading ...')
        conn = None
        tuples = self.dataframe_to_tuples(self.dataframe)
        columns = ','.join(list(self.dataframe.columns))
        placeholders = ','.join(['%s'] * len(self.dataframe.columns))
        query = f'INSERT INTO "{self.conf["stat_tourism"]["target_table"]}" ({columns}) VALUES ({placeholders})'

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

            if not is_table_empty(cur, self.conf["stat_tourism"]["target_table"]):
                logger.info('Truncating table before inserting new data')
                cur.execute(f'TRUNCATE TABLE "{self.conf["stat_tourism"]["target_table"]}"')

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
