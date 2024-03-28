import logging

import colorlog


def setup_colored_logger(logger_name='SleepLogs'):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter_string = (
        "{white}{asctime} {log_color}{levelname: <8} {name} {reset} {white}{message}"
    )

    formatter = colorlog.ColoredFormatter(
        formatter_string,
        datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='{'
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
