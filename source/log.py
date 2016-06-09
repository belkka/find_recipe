# -*- coding: utf-8 -*-
import logging
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

from config import LOG_DIR


def logger_list():
    for key in logging.Logger.manager.loggerDict:
        print key

# urllib logger off
# logging.getLogger("requests.packages.urllib3").setLevel(logging.WARNING)


FILE_FORMATTER = logging.Formatter(
    "%(asctime)s (%(filename)s:%(lineno)d) "
    "%(levelname)s %(name)s: %(message)s")

CONSOLE_FORMATTER = logging.Formatter("%(levelname)s %(name)s: %(message)s")


def make_logger(name):
    fh = logging.FileHandler("".join((LOG_DIR, name, ".log")))
    sh = logging.StreamHandler()

    fh.setFormatter(FILE_FORMATTER)
    sh.setFormatter(CONSOLE_FORMATTER)

    fh.setLevel(INFO)
    sh.setLevel(DEBUG)

    logger = logging.getLogger(name)
    logger.setLevel(-1)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


bot = make_logger("bot")
sqlite = make_logger("sqlite")
