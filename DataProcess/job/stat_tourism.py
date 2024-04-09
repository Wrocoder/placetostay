from DataProcess.scripts.tour_stat_data_processor import DataTourStatProcessor
from helpers.job_utils import get_conf, time_taken
from logger.colored_logger import ColoredLogger

logger = ColoredLogger(logger_name=__name__).get_logger()


@time_taken
def process_tourism_data():
    conf = get_conf(path='config/config.yaml', logger=logger)
    processor = DataTourStatProcessor(conf)
    processor.load_data()
    processor.preprocess_cols()
    processor.load_df_to_postgres()


if __name__ == '__main__':
    process_tourism_data()
