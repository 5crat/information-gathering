#!/usr/bin/env python
#-*-coding:utf-8-*-
#-*-author:scrat-*-

import re
import chardet
import requests


class HttpRequest(object):
    """
        HTTP Request class
    """
    def __init__(
            self,
            target='',
            web_method='GET',
            data='',
            proxies='',
            timeout=10,
            useragent='Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)',
    ):
        self.target = target
        self.web_method = web_method
        self.data = data
        self.proxies = proxies
        self.timeout = timeout
        self.UserAgent = useragent
        self.headers = {
            'User-Agent': self.UserAgent,
            'Referer': self.target
        }

    def http_request(self):
        """
        http request method
        :return list {'status_code':...,''header:....,'content':...}
        """
        try:
            if not self.target:
                return
            methods = ['GET', 'POST', 'HEAD', 'OPTIONS', 'PUT', 'DELETE']
            if self.web_method.upper() not in methods:
                print r'HTTP请求的方式错误,无法识别该方式： '+ self.method

            r = requests.request(
                self.web_method.upper(),
                self.target,
                data=self.data,
                headers=self.headers,
                proxies=self.proxies,
                timeout=self.timeout,
            )
            check_jump = False
            check_jump_payloads = [
                'window.location\s?=\s?(.*);',
                'window.location.href\s?=\s?(.*);',
                '<meta http-equiv=\"refresh\".*url=(.*)\s?',
                ]
            for i in check_jump_payloads:
                check_jump = re.findall(i, r.content.lower())
                if check_jump:
                    addr = check_jump[0].strip('"')
                    if 'http' in addr:
                        self.target = addr
                    else:
                        if self.target.endswith('/') == False:
                            self.target += '/'
                        r = requests.request(
                            self.web_method.upper(),
                            self.target + addr,
                            data=self.data,
                            headers=self.headers,
                            proxies=self.proxies,
                            timeout=self.timeout,
                        )
                    break
            html = r.content
            charset = chardet.detect(html)['encoding'].lower()
            '''
            if r.encoding == 'ISO-8859-1':
                print 1
                html = r.content.decode('gbk').encode('utf8')
            else:
                print(2)
                html = r.content.decode(r.encoding).encode('utf8')
            '''
            if charset != 'utf8':
                html = html.decode(charset).encode('utf8')
            headers = {}
            for m in r.headers:
                headers[m] = r.headers[m]
            return {'status_code': str(r.status_code), 'header': headers, 'content':  html}
        except Exception as e:
            print 'error :  ' + str(e)
            return None

if __name__ == '__main__':
    a = HttpRequest('http://www.baidu.com', web_method="post")
    b = a.http_request()
    for i in b:
        print b[i]

