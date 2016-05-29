#!/usr/bin/env python
#-*-coding:utf-8-*-
#-*-author:scrat-*-

import os
import sys

# database config
DB_config = {
    'dbname': 'gun',
    'username': 'root',
    'password': '',
    'port': 3306,
    'host': 'localhost'
}
# platform
PLATFORM = os.name

# python version
PYVERSION = sys.version.split()[0]

# max threads num
MAX_THREADS = 10
