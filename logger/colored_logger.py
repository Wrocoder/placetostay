import logging

import colorlog


class ColoredLogger:
    """ Logging for the project """
    def __init__(self, logger_name='WebLogs'):
        self.logger = logging.getLogger(logger_name)
        self._setup_logger()

    def _setup_logger(self):
        self.logger.setLevel(logging.DEBUG)
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

        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger
