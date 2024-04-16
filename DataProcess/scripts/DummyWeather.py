import random

import pandas as pd

from DataProcess.scripts.DBDataProcessor import DBDataProcessor
from helpers.map_countries import countries, months
from logger.colored_logger import ColoredLogger

logger = ColoredLogger(logger_name=__name__).get_logger()


class DummyWeatherData(DBDataProcessor):

    def __init__(self, table_name, config):
        super().__init__(table_name, config)
        self.dataframe = self.generate_dummy_data()

    @staticmethod
    def generate_dummy_data():

        data = []
        for country in countries:
            for month in months:
                data.append(
                    {
                        "country": country,
                        "month": month,
                        "average_temperature": f"{random.randint(-25, 30)} C\u00b0",
                        "precipitation_level": random.choice(["Low", "Medium", "High"]),
                        "air_speed": f"{random.uniform(0.5, 20.0):.1f} m/s",
                        "recommended_to_visit": random.choice(["Yes", "No"]),
                    }
                )

        return pd.DataFrame(data)
