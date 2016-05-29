#!/usr/bin/env python
# -*-coding:utf-8-*-
#-*-author:scrat-*-

import logging

level = logging.WARNING
LOGGER = logging.getLogger(nama='gun_log')

LOGGER.setLevel(level)

fh = logging.FileHandler(filename='gun_log')
fh.setLevel(level)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh.setFormatter(formatter)
ch = logging.StreamHandler()
ch.setLevel(level)
LOGGER.addHandler(fh)
LOGGER.addHandler(ch)