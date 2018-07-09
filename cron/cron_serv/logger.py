import logging
import sys


class ConsoleLogger:
    """
    Output log to stdout
    """

    def __init__(self, name=None, level=logging.INFO):
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(level)
        if not self.__logger.handlers:
            self.__ch = logging.StreamHandler(sys.stdout)
            self.__logger.addHandler(self.__ch)
        self.__logger.propagate = False

    def debug(self, msg, *args, **kwargs):
        self.__logger.debug(msg, *args, **kwargs)
        self.__ch.flush()

    def info(self, msg, *args, **kwargs):
        self.__logger.info(msg, *args, **kwargs)
        self.__ch.flush()

    def warning(self, msg, *args, **kwargs):
        self.__logger.warning(msg, *args, **kwargs)
        self.__ch.flush()

    def error(self, msg, *args, **kwargs):
        self.__logger.error(msg, *args, **kwargs)
        self.__ch.flush()

    def critical(self, msg, *args, **kwargs):
        self.__logger.critical(msg, *args, **kwargs)
        self.__ch.flush()
