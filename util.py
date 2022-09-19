# coding: utf-8
"""
共通のロガーを定義
"""

import logging
import os
import re


def get_shared_logger():
    if logging.getLogger("addchapter").hasHandlers() is True:
        return logging.getLogger("addchapter")
    else:
        logging.basicConfig(level=logging.DEBUG)
        log_fmt = logging.Formatter(fmt='%(asctime)s [%(levelname)s] %(module)s - %(funcName)s : %(message)s')
        logger = logging.getLogger("addchapter")
        log_fh = logging.FileHandler("addchapter.log", "a+")
        log_fh.formatter = log_fmt
        log_fh.level = logging.DEBUG
        logger.addHandler(log_fh)
        return logger
