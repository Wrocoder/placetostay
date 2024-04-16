from DataProcess.scripts.DataHotelProcessor import DataHotelProcessor
from helpers.job_utils import get_conf, time_taken
from logger.colored_logger import ColoredLogger

logger = ColoredLogger(logger_name=__name__).get_logger()


@time_taken
def process_hotel_data():
    conf = get_conf(path="config/config.yaml", logger=logger)

    processor = DataHotelProcessor(conf["hotels"]["target_table"], conf)
    processor.find_field_names()
    processor.preprocess_cols()
    processor.check_types()
    processor.load_df_to_postgres()


if __name__ == "__main__":
    process_hotel_data()
