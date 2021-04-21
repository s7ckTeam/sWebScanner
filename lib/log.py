# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/4/12 15:44
# @Author : 冰海
# @File : log.py
import sys
import logging
from config.colors import mkPut
from colorama import init


class LoggingLevel:
    SUCCESS = 9
    SYSINFO = 8
    ERROR = 7
    WARNING = 6


init(autoreset=True)

logging.addLevelName(LoggingLevel.SUCCESS, mkPut.cyan("[+]"))
logging.addLevelName(LoggingLevel.SYSINFO, mkPut.green("[INFO]"))
logging.addLevelName(LoggingLevel.ERROR, mkPut.red("[ERROR]"))
logging.addLevelName(LoggingLevel.WARNING, mkPut.yellow("[WARNING]"))

LOGGER = logging.getLogger("GlassLog")

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s",
    datefmt=mkPut.fuchsia("[%H:%M:%S]")
)
LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
LOGGER_HANDLER.setFormatter(formatter)
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER.setLevel(LoggingLevel.WARNING)


class MY_LOGGER():
    def info(self, msg):
        return LOGGER.log(LoggingLevel.SYSINFO, msg)

    def error(self, msg):
        return LOGGER.log(LoggingLevel.ERROR, msg)

    def warning(self, msg):
        return LOGGER.log(LoggingLevel.WARNING, msg)

    def success(self, msg):
        return LOGGER.log(LoggingLevel.SUCCESS, msg)


logger = MY_LOGGER()
