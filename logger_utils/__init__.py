from logger_utils.CustomFormatter import CustomFormatter
import datetime

import logging


def init_logger(logger: logging.Logger):
    logger.setLevel(logging.DEBUG)

    # Define format for logs
    fmt = '%(asctime)s | %(levelname)2s | %(message)s'

    # Create stdout handler for logging to the console (logs all five levels)
    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(CustomFormatter(fmt))

    # Create file handler for logging to a file (logs all five levels)
    today = datetime.date.today()
    file_handler = logging.FileHandler('logs\\files_server_{}.log'.format(today.strftime('%Y_%m_%d')))
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(fmt))

    # Add both handlers to the logger_utils
    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)
