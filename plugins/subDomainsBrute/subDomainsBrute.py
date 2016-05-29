#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# A simple and fast sub domain brute tool
# my[at]lijiejie.com (http://www.lijiejie.com)

#

import Queue
import sys
import dns.resolver
import threading
from time import time, sleep
from libs.core.data import paths


class DNSBrute:
    def __init__(self, target, names_file='subnames_x.txt', threads_num=10, output=None):
        self.target = target.strip()
        self.names_file = names_file
        self.output = output
        self.thread_count = self.threads_num = threads_num
        self.scan_count = self.found_count = 0
        self.lock = threading.Lock()
        self.resolvers = [dns.resolver.Resolver() for _ in range(threads_num)]
        self._load_dns_servers()
        self._load_sub_names()
        self._load_next_sub()
        self.ip_dict = {}



    def _load_dns_servers(self):
        dns_servers = []
        with open(paths.ROOT_PATH + '/plugins/subDomainsBrute/dns_servers.txt') as f:
            for line in f:
                server = line.strip()
                if server.count('.') == 3 and server not in dns_servers:
                    dns_servers.append(server)
        self.dns_servers = dns_servers
        self.dns_count = len(dns_servers)

    def _load_sub_names(self):
        self.queue = Queue.Queue()
        with open(paths.ROOT_PATH + '/plugins/subDomainsBrute/' + self.names_file) as f:
            for line in f:
                sub = line.strip()
                if sub: self.queue.put(sub)

    def _load_next_sub(self):
        next_subs = []
        with open(paths.ROOT_PATH + '/plugins/subDomainsBrute/next_sub.txt') as f:
            for line in f:
                sub = line.strip()
                if sub and sub not in next_subs:
                    next_subs.append(sub)
        self.next_subs = next_subs

    def _update_scan_count(self):
        self.lock.acquire()
        self.scan_count += 1
        self.lock.release()

    def _scan(self):
        thread_id = int(threading.currentThread().getName())
        self.resolvers[thread_id].nameservers = [self.dns_servers[thread_id % self.dns_count]]  # must be a list object
        self.resolvers[thread_id].lifetime = self.resolvers[thread_id].timeout = 1.0
        while self.queue.qsize() > 0 and self.found_count < 3000:  # limit found count to 3000
            sub = self.queue.get(timeout=1.0)
            try:
                cur_sub_domain = sub + '.' + self.target
                answers = self.resolvers[thread_id].query(cur_sub_domain)
                is_wildcard_record = False

                if answers:
                    for answer in answers:
                        self.lock.acquire()
                        if answer.address not in self.ip_dict:
                            self.ip_dict[answer.address] = 1
                        else:
                            self.ip_dict[answer.address] += 1
                            if self.ip_dict[answer.address] > 6:  # a wildcard DNS record
                                is_wildcard_record = True
                        self.lock.release()
                    if is_wildcard_record:
                        self._update_scan_count()
                        continue
                    self.lock.acquire()
                    self.found_count += 1
                    ips = ', '.join([answer.address for answer in answers])
                    msg = cur_sub_domain.ljust(30) + ips
                    self.output.insert({'domain': cur_sub_domain, 'ip': ips, 'status': 0})
                    sys.stdout.write('\r' + msg + '\r\n')
                    sys.stdout.flush()
                    # print time.time()-self.start_time
                    self.lock.release()
                    for i in self.next_subs:
                        self.queue.put(i + '.' + sub)
            except Exception, e:
                print e
            self._update_scan_count()
        self.lock.acquire()
        self.thread_count -= 1
        self.lock.release()

    def run(self):
        print "[ + ] subDomainsBrute Start...."
        for i in range(self.threads_num):
            t = threading.Thread(target=self._scan, name=str(i))
            t.setDaemon(True)
            t.start()
        while self.thread_count > 0:
            sleep(0.01)
        print "[ + ] subDomainsBrute Done....!"


if __name__ == '__main__':
    pass


