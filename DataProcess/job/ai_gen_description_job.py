from DataProcess.scripts.GenDescriptionCountryProc import GenDescriptionCountryProc
from helpers.job_utils import get_conf, time_taken
from logger.colored_logger import ColoredLogger

logger = ColoredLogger(logger_name=__name__).get_logger()


@time_taken
def process_weather_data():
    conf = get_conf(path="config/config.yaml", logger=logger)
    processor = GenDescriptionCountryProc(
        conf["country_description"]["target_table"], conf
    )
    processor.gen_data()
    processor.load_df_to_postgres(reg_uuid=True)


if __name__ == "__main__":
    process_weather_data()
