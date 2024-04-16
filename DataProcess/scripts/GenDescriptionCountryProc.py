import uuid

import g4f
import pandas as pd

from DataProcess.scripts.DBDataProcessor import DBDataProcessor
from helpers.map_countries import countries
from logger.colored_logger import ColoredLogger

logger = ColoredLogger(logger_name=__name__).get_logger()


class GenDescriptionCountryProc(DBDataProcessor):

    def __init__(self, table_name, config):
        super().__init__(table_name, config)
        self.dataframe = None

    @staticmethod
    def gen_ai_description(country):
        # Execute with a specific provider
        response = g4f.ChatCompletion.create(
            model="gpt-4",
            provider=g4f.Provider.Cnote,
            messages=[
                {
                    "role": "user",
                    "content": f"Give me a description for {country} as as as country for tourism, "
                    f"describe some attractions so that people want to go there. "
                    f"Just give me that information.",
                }
            ],
            stream=True,
        )
        return "".join(response)

    @staticmethod
    def gen_ai_continent(country):
        # Execute with a specific provider
        response = g4f.ChatCompletion.create(
            model="gpt-4",
            provider=g4f.Provider.Cnote,
            messages=[
                {
                    "role": "user",
                    "content": f"What continent does this country {country} belong to, Just give me that information "
                    f"only continent name",
                }
            ],
            stream=True,
        )
        return "".join(response)

    def gen_data(self):
        logger.info(
            [
                provider.__name__
                for provider in g4f.Provider.__providers__
                if provider.working
            ]
        )

        data = []
        for country in countries:
            row = {
                "country_name": country,
                "continent": self.gen_ai_continent(country),
                "country_description": self.gen_ai_description(country),
            }

            logger.info(f"Generated data: {row}")
            data.append(row)

        self.dataframe = pd.DataFrame(data)
        self.dataframe["country_id"] = self.dataframe["country_name"].apply(
            lambda _: uuid.uuid4()
        )
