#!/usr/bin/env python
#-*-coding:utf-8-*-
#-*-author:scrat-*-


from plugins.subDomainsBrute.subDomainsBrute import DNSBrute
from plugins.wyportmap.wyportmap import run_wyportmap


def enum_domain_worker(domain, DB):
    if DB is not None:
        DB.set_table('gun_domains')
        DNSBrute(domain, output=DB).run()
    else:
        DNSBrute(domain).run()


def enum_port(ip, DB=None, taskId=None):
    if DB is not None:
        DB.set_table('gun_ips')
        run_wyportmap(ip, DB=DB, taskid=taskId)
    else:
        run_wyportmap(ip)
