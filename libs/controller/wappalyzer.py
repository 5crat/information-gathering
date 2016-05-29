#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
from libs.core.data import conf
from libs.core.common import setConfAttribute
from libs.request.httprequest import HttpRequest

try:
    import json
except ImportError:
    import simplejson as json


class Application(object):

    def __init__(self, app):
        self.app = app
        self.confidence = {}
        self.detected = False
    def set_detected(self, pattern, type, value, key=None):
        self.detected = True
        self.what = self.app['cats'][0]
        self.confidence[
            type + ' ' + (key + ' ' if key else '') + pattern.str] = pattern.confidence

        # todo: detect version

    def get_confidence(self):
        total = sum(v for v in self.confidence.itervalues())
        return min(100, total)


class Wappalyzer(HttpRequest):

    def __init__(self, data=None, datafile_path=None):
        HttpRequest.__init__(self)
        self.target = conf.target
        self.web_method = conf.web_method
        self.data = conf.data
        self.headers = conf.headers
        self.proxies = conf.proxies
        self.UserAgent = conf.useragent
        self.timeout = conf.timeout
        data = data or self.load_data(datafile_path)
        self.categories = data['categories']
        self.apps = data['apps']

    def load_data(self, datafile_path=NotImplementedError):
        if not datafile_path:
            file_dir = os.path.dirname(__file__)
            datafile_path = os.path.join(file_dir, 'apps.json')
        with open(datafile_path) as f:
            data = json.load(f)
        return data

    def analyze(self, response=None):
        if not response and not self.target:
            raise ValueError
        response = HttpRequest.http_request(self)
        if not response:
            return None
        try:
            html = response['content']
            headers = response['header']
            status_code = response['status_code']
            data = {
                'url': self.target,
                'html': html,
                'script': re.findall(r'<script[^>]+src=(?:"|\')([^"\']+)', html, re.I | re.M),
                'meta': dict((n.lower(), v) for n, v in
                             re.findall('<meta\s+(?:name|property)=["\']([^"\']+)["\'].+?content=["\']([^"\']+)["\']', html,
                                        re.I | re.M) +
                             [(m2, m1) for m1, m2 in \
                              re.findall('<meta\s+content=["\']([^"\']+)["\'].+?(?:name|property)=["\']([^"\']+)["\']', html,re.I | re.M)]),
                'headers': dict((n.lower(), v) for n, v in headers.iteritems()),
                'env': None
            }
            detected_apps = {}
            for app_name, app in self.apps.iteritems():
                application = Application(app)
                for detection_type, patterns in app.iteritems():
                    try:
                        if detection_type in ['url', 'html']:
                            for pattern in self.parse_patterns(patterns):
                                if pattern.regex.search(data[detection_type]):
                                    application.set_detected(
                                        pattern, detection_type, data[detection_type])
                        elif detection_type in ['meta', 'headers']:
                            for hm_name, hm_pattern in patterns.iteritems():
                                for pattern in self.parse_patterns(hm_pattern):
                                    value = data[detection_type].get(
                                        hm_name.lower())
                                    if value and pattern.regex.search(value):
                                        application.set_detected(
                                            pattern, detection_type, value, hm_name)
                        elif detection_type in ['script']:
                            for script in data[detection_type]:
                                for pattern in self.parse_patterns(patterns):
                                    if pattern.regex.search(script):
                                        application.set_detected(
                                            pattern, detection_type, script)
                        elif detection_type in ['website', 'excludes', 'cats', 'implies', 'env']:
                            pass
                        else:
                            raise NotImplementedError
                    except:
                        print 'error while detecting by %s application %s' % (detection_type, app)
                if application.detected:
                    detected_apps[self.categories[str(application.what)]] = app_name
            detected_apps['status_code'] = status_code
            detected_apps['html'] = html
            detected_apps['headers'] = headers
            return detected_apps
        except Exception as e:
            print e + 'WAPPALYZER'
            print __file__ + '    find error！'
            return None

    class Pattern:

        def __init__(self, str):
            self.str = str
            self.regex = re.compile(str, re.I)
            self.confidence = 100

    def parse_patterns(self, patterns):
        if isinstance(patterns, basestring):
            patterns = [patterns]
        elif not isinstance(patterns, list):
            raise ValueError

        parsed = []
        for pattern in patterns:
            parts = pattern.split('\\;')
            result = Wappalyzer.Pattern(parts[0])
            for part in parts[1:]:
                name, value = part.split(':', 1)
                if name in ['confidence']:
                    value = float(value)
                setattr(result, name, value)
            parsed.append(result)

        return parsed


if __name__ == '__main__':
    setConfAttribute()
    conf.target = 'http://cn.wordpress.org/'
    try:
        w = Wappalyzer(datafile_path='../../payload/apps.json')
        print w.analyze()
    except IndexError:
        print ('Usage: python %s <url>' % sys.argv[0])
