import logging

import colorlog


def setup_colored_logger(logger_name='WebpLogs'):
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
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
        },
        secondary_log_colors={},
        style='{'
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
