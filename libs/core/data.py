#!/usr/bin/env python
# -*-coding:utf-8-*-
#-*-author:scrat-*-

from Queue import Queue
from datatype import AttribDict
from libs.core.log import LOGGER

#PATH
paths = AttribDict()

#CONF
conf = AttribDict()

domainQueue = Queue()
ipQueue = Queue()

#log
logger = LOGGER