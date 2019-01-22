"""Logging wrapper utility """
import logging
import os

DEFAULT_LEVEL = logging.WARN
ENV_VAR = 'LOGGING_LEVEL'


def get_logger(class_name) -> logging.Logger:
    """Gets a class's logger and sets logging level

    The logging level is determined by the environment variable 'LOGGING_LEVEL'
    first, if the environment variable is not set then WARN level is defaulted to.

    Args:
        class_name (str): The class or component name for the logger to be fetched.

    Returns:
        object: Logger object
    """
    log_level = __get_logging_level()
    logger = logging.getLogger(class_name)
    logger.setLevel(log_level)

    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    return logger


def __get_logging_level():
    if ENV_VAR in  os.environ:
        return int(os.environ[ENV_VAR])
    return DEFAULT_LEVEL
