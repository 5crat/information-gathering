#!/usr/bin/env python
# -*-coding:utf-8-*-
#-*-author:scrat-*-

import logging


# 设置记录日志等级
level = logging.WARNING
LOGGER = logging.getLogger(name='gun_log')

LOGGER.setLevel(level)

fh = logging.FileHandler(filename='gun_log')
fh.setLevel(level)
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(funcName)s - %(message)s')

fh.setFormatter(formatter)
ch = logging.StreamHandler()
ch.setLevel(level)
LOGGER.addHandler(fh)
LOGGER.addHandler(ch)