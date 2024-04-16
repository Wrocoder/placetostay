import numpy as np
import pandas as pd

from DataProcess.scripts.DBDataProcessor import DBDataProcessor
from helpers.map_countries import (
    country_mapping,
    tourism_concept_mapping,
    translation_dict,
    month_dict,
)
from logger.colored_logger import ColoredLogger

logger = ColoredLogger(logger_name=__name__).get_logger()


class DataTourStatProcessor(DBDataProcessor):
    def __init__(self, table_name, config):
        super().__init__(table_name, config)
        self.dataframe = None

    def load_data(self):
        logger.info("Loading source csv data ...")
        return pd.read_csv(
            self.conf["stat_tourism"]["source_path"], sep="\t", header=None
        )

    def find_field_names(self):
        new_columns = self.dataframe.iloc[0]
        self.dataframe.columns = new_columns
        self.dataframe = self.dataframe.drop(self.dataframe.index[0])

    @staticmethod
    def convert_to_float(value):
        try:
            return float(value.replace(".", ""))
        except ValueError:
            return None

    def preprocess_cols(self):
        self.dataframe = self.load_data()
        # Exclude unnecessary columns
        self.dataframe = self.dataframe[[2, 5, 6, 7]]
        # Applying the translations
        self.dataframe[2] = self.dataframe[2].map(country_mapping)
        self.dataframe[5] = self.dataframe[5].map(tourism_concept_mapping)

        # Renaming columns
        self.find_field_names()
        self.dataframe.rename(columns=translation_dict, inplace=True)
        self.dataframe["total"] = self.dataframe["total"].apply(self.convert_to_float)

        # Exclude rows with Nulls and old data
        columns_to_convert = self.dataframe.columns
        for column in columns_to_convert:
            self.dataframe[column] = self.dataframe[column].replace({np.nan: None})

        self.dataframe = self.dataframe.dropna()
        self.dataframe = self.dataframe[
            ~self.dataframe["period"].str.startswith(("2021", "2020", "2019", "2018"))
        ]
        # prepare time_period
        self.dataframe["month"] = self.dataframe["period"].apply(
            lambda x: month_dict[x[-2:]]
        )
        self.dataframe["year"] = self.dataframe["period"].str[:4].astype(int)
        # find relevant values
        idx = self.dataframe.groupby(["country", "period"])["total"].idxmax()
        self.dataframe = self.dataframe.loc[idx]
