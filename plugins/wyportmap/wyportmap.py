#!/usr/bin/env python
# encoding: utf-8
# mail: ringzero@0x557.org

import re
import sys
from time import sleep
from libs.core.data import logger
from plugins.wyportmap.libnmap.process import NmapProcess
from plugins.wyportmap.libnmap.parser import NmapParser

# 重试次数 & 超时时间(s)
retrycnt = 3
timeout = 3600
scanPort = '21-25,80-89,110,111,143,161,210,389,443,513,873,1080,1352,1433,1521,1158,2601,2604,3128,3306-3308,3389,3690,3700,4440,4848,5000,5432,5632,5900-5902,6379,7001,8000-8090,8888,9200,9300,9080-9090,9999-10001,9000,9418,27017-27019,50060,11211,2049'

global_options = '-sS -P0 -sV -O --script=banner -p T:' + scanPort

# 处理端口状态
global_log_states = ['open']  # open, filtered, closed, unfiltered


def do_nmap_scan(targets, options=global_options):
    # 运行次数初始化
    trycnt = 0

    while True:
        # 运行时间初始化
        runtime = 0

        if trycnt >= retrycnt:
            logger.warning('nmap retrycnt > 3(重试次数)')
            print '-' * 50
            return 'retry overflow'

        try:
            nmap_proc = NmapProcess(targets=targets, options=options, safe_mode=False)
            nmap_proc.run_background()

            while nmap_proc.is_running():
                if runtime >= timeout:  # 运行超时，结束掉任务，休息1分钟, 再重启这个nmap任务
                    logger.warning('nmap scan timeout')
                    print '-' * 50
                    print "* timeout. terminate it..."
                    nmap_proc.stop()
                    # 休眠时间
                    sleep(60)
                    trycnt += 1
                    break
                else:
                    print 'running[%ss]:%s' % (runtime, nmap_proc.command)
                    sleep(5)
                    runtime += 5
            if nmap_proc.is_successful():
                print '-' * 50
                print nmap_proc.summary
                return nmap_proc.stdout

        except Exception, e:
            # raise e
            print e
            trycnt += 1
            if trycnt >= retrycnt:
                logger.warning('nmap retrycnt > 3(重试次数)')
                print '-' * 50
                print '* retry overflow'
                return e


def parse_nmap_report(nmap_stdout, taskid=None):
    result = {}
    try:
        # 处理结果并写入后台数据库
        nmap_report = NmapParser.parse(nmap_stdout)
        # host.address
        hd = ''
        # 开始处理扫描结果
        for host in nmap_report.hosts:

            # print("Nmap scan : {0}".format(host.address))
            host.taskid = taskid
            hd = host.address
            # 处理主机开放的服务和端口
            portInfo = []
            for serv in host.services:
                serv.address = host.address
                serv.taskid = taskid
                serv.endtime = host.endtime
                if serv.state in global_log_states:
                    p = re.findall('\[(.*)\]', str(serv))
                    portInfo.append(p[0])
            result[hd] = portInfo
            #print {host.address: portInfo}
        #print '* Scan finished'
        return result

    except Exception, e:
        logger.error('parse nmap report error')
        # 处理报表出错，返回错误结果
        return e


def run_wyportmap(targets, DB=None, taskid=None):
    print '-' * 50
    print '* Starting id:(%s) [%s] portmap scan' % (taskid, targets)
    print '-' * 50
    nmap_result = do_nmap_scan(targets)
    print '-' * 50
    result = parse_nmap_report(nmap_result, taskid)
    if save_port_info(result, DB):
        return True
    else:
        return False


def save_port_info(result, DB):
    if result is None or DB is None:
        return False
    for ip in result:
        data = {}
        data['ip'] = ip
        ports = ''
        for port in result[ip]:
            ports += port+'|||'
        data['port'] = ports.rstrip("|||")
        if data:
            if DB.check_exist({'ip': data['ip']}) is False:
                if DB.insert(data):
                    sql = 'update gun_domains set status=1 where ip like "%'+data['ip']+'%"'
                    print(sql)
                    DB.execute(sql)
                    print '[ + ] Insert Success: ' + str(result)
                else:
                    logger.error('nmap result insert db error')
                    print '[ - ] Insert Failed: ' + str(result)
            else:
                logger.warning('nmap result insert data was existed')
                print '[ ! ] Data Was Existed: ' + str(result)

if __name__ == "__main__":

    if len(sys.argv) == 2:
        run_wyportmap(sys.argv[1])
        sys.exit(0)
    elif len(sys.argv) == 3:
        print run_wyportmap(sys.argv[1], sys.argv[2])
    else:
        print "usage: %s targets taskid" % sys.argv[0]
        sys.exit(-1)