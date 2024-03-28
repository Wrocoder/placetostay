import time
from functools import wraps

import yaml

from logger.colored_logger import ColoredLogger

logger = ColoredLogger(logger_name=__name__).get_logger()


def get_conf(path=None, logger=None, location='local') -> dict:
    try:
        if location == 'local':
            with open(path, 'r') as yaml_conf:
                configuration = yaml.safe_load(yaml_conf)
                logger.info('Config file read successfully')
                return configuration
        elif location == 'nonlocal':
            pass
    except FileNotFoundError as e:
        logger.error(f"Error reading YAML file {e}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error {e}")
        raise


def time_taken(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        total_time = end_time - start_time
        minutes = int(total_time // 60)
        seconds = total_time % 60

        logger.info(f'Function {func.__name__}{args} {kwargs} Took {minutes} minutes and {seconds:.4f} seconds')
        return result

    return timeit_wrapper
