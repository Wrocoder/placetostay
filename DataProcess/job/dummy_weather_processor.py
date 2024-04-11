from DataProcess.scripts.dummy_weather import DummyWeatherData
from helpers.job_utils import get_conf, time_taken
from logger.colored_logger import ColoredLogger

logger = ColoredLogger(logger_name=__name__).get_logger()


@time_taken
def process_weather_data():
    conf = get_conf(path='config/config.yaml', logger=logger)
    processor = DummyWeatherData(conf)
    processor.load_df_to_postgres()


if __name__ == '__main__':
    process_weather_data()
