#!/usr/bin/env python
# -*-coding:utf-8-*-
#-*-author:scrat-*-

import os


from libs.core.data import paths
from libs.core.data import conf


def init():
    setPaths()
    setConfAttribute()


def banner():
    """
    Banner info
    """
    print 'This is a big gun!!!\r\n'


def setPaths():
    """
    set Environment variable
    :return:
    """
    paths.PAYLOAD_PATH = os.path.join(paths.ROOT_PATH, "payload")
    paths.TMP_PATH = os.path.join(paths.ROOT_PATH, "tmp")


def setConfAttribute():
    conf.target = None
    conf.ip = None
    conf.port = []
    conf.cookie = None
    conf.useragent = None
    conf.proxies = []
    conf.web_method = 'GET'
    conf.data = None
    conf.headers = None
    conf.timeout = 10