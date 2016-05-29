#!/usr/bin/env python
#-*-coding:utf-8-*-
#-*-author:scrat-*-

import os
import sys
import time
import inspect
from libs.core.data import paths
from libs.core.common import banner, setPaths, setConfAttribute
from libs.core.dbhandle import DB
from libs.controller.controlCenter import enum_domain_worker, enum_port
from libs.core.setting import DB_config


def modulePath():
    """
    get the script's directory
    """
    _ = inspect.getsourcefile(modulePath)
    return os.path.dirname(os.path.realpath(_))


def main():
    try:
        paths.ROOT_PATH = modulePath()
        setPaths()
        setConfAttribute()
        banner()
        db = DB('mysql', DB_config['dbname'], DB_config['username'], DB_config['password'])

        #-----------暴力猜解域名-----------
        print '\r\n[*] starting at %s\n' % time.strftime("%X")
        #enum_domain_worker('qq.com', DB=db)
        db.set_table('gun_domains')
        r = db.select({'status': '0'})
        for i in r:
            print i[2]
        enum_port(str(i[2]))
        db.close()
    except KeyboardInterrupt:
        print 'User Aborted!'
    except EOFError:
        print 'Exit!'
    except SystemExit:
        pass
    finally:
        print '[ * ] shutdown at %s\n' % time.strftime("%X")
if __name__ == '__main__':
    main()