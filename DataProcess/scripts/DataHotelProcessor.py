import numpy as np
import pandas as pd

from DataProcess.scripts.DBDataProcessor import DBDataProcessor
from logger.colored_logger import ColoredLogger

logger = ColoredLogger(logger_name=__name__).get_logger()


class DataHotelProcessor(DBDataProcessor):
    def __init__(self, table_name, config):
        super().__init__(table_name, config)
        self.dataframe = None

    def load_data(self):
        logger.info("Loading source csv data ...")
        return pd.read_csv(self.conf["hotels"]["source_path"], header=None)

    def find_field_names(self):
        self.dataframe = self.load_data()
        new_columns = self.dataframe.iloc[0]
        self.dataframe.columns = new_columns
        self.dataframe = self.dataframe.drop(self.dataframe.index[0])

    def preprocess_cols(self):
        columns_to_convert = [
            "numberrooms",
            "numberfloors",
            "yearopened",
            "yearrenovated",
        ]

        for column in columns_to_convert:
            self.dataframe[column] = pd.to_numeric(
                self.dataframe[column], errors="coerce"
            ).astype("Int64")
            # self.dataframe[column] = self.dataframe[column].replace({np.nan: None})

        columns_to_convert = self.dataframe.columns
        for column in columns_to_convert:
            self.dataframe[column] = self.dataframe[column].replace({np.nan: None})

    @staticmethod
    def calculate_length(x):
        return len(str(x))

    def check_types(self):
        max_length_indices = self.dataframe.apply(
            lambda col: col.astype(str).map(self.calculate_length).idxmax()
        )
        max_length_values = {
            col: self.dataframe[col].iloc[max_length_indices[col]]
            for col in self.dataframe.columns
        }
        for column, value in max_length_values.items():
            logger.info(f"{column}: {value} (Length: {len(str(value))})")
