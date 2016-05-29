#!/usr/bin/env python
# -*-coding:utf-8-*-
#-*-author:scrat-*-

import socket


def dns_parse(host):
    result = []
    regx = ['http://', 'https://', 'ftp://']
    for i in regx:
        if i in host:
            host = host.split(i)[1]
    try:
        datas = socket.getaddrinfo(host, None, 0, socket.SOCK_STREAM)
        for data in datas:
            result.append(data[4][0])
        return result
    except Exception as e:
        print e + 'dns_parse'
        return '0.0.0.0'


def reverse_lookup(host):
    result = []
    regx = ['http://', 'https://', 'ftp://']
    for i in regx:
        if i in host:
            host = host.split(i)[1]
    try:
        datas = socket.gethostbyaddr(host)
        result.append(datas[0])
    except Exception as e:
        print e + 'DNS'
        result = 'None'
    return result


if __name__ == '__main__':
    #a = reverse_lookup(host='http://219.141.191.145')
    a = dns_parse(host='www.bankofluoyang.com.cn')
    print a