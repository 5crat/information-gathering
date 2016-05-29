#!/usr/bin/env python
#-*-coding:utf-8-*-
#-*-author:scrat-*-

import re
from libs.core.data import conf
from libs.core.enums import FingerPrintRules
#from lib.core.common import setConfAttribute
from libs.core.data import logger
from libs.controller.wappalyzer import Wappalyzer
try:
    from libs.core.data import paths
except Exception as e:
    logger.warning(e)

def check_fingerprint():
    result = Wappalyzer(datafile_path=paths.PAYLOAD_PATH + '/apps.json').analyze()
    if result == None:
        logger.warning("analyze error")
        print 'analyze error!'
        return 'None'
    if result.has_key('status_code') == True:
        headers = ''
        for i in result['headers']:
            headers += i + ':' + result['headers'][i] + '\r\n'
        result['headers'] = headers
        content = result['html'].lower()
        tmp_form = re.findall(FingerPrintRules.FromRegex, content)
        tmp_title = re.findall(FingerPrintRules.TitleRegex, content)
        result['title'] = 'None'
        if tmp_title:
            result['title'] = tmp_title[0]

        '''
        tmp_language = re.findall(FingerPrintRules.LanguageRegex, headers.lower())
        if tmp_form:
            if '.php' in tmp_form:
                result['language'] = 'php'
            elif '.asp' in tmp_form or '.aspx' in tmp_form:
                result['language'] = 'asp'
            elif '.jsp' in tmp_form or '.do' in tmp_form or '.action' in tmp_form:
                result['language'] = 'jsp'
            else:
                result['language'] = 'UnKnown'
        else:
            result['language'] = 'UnKnown'
        if result['language'] == 'UnKnown':
            if tmp_language:
                if 'php' in tmp_language:
                    result['language'] = tmp_language
                elif 'asp' in tmp_language:
                    result['language'] = tmp_language
                elif 'jsp' in tmp_language or 'servlet' in tmp_language:
                    result['language'] = tmp_language
                else:
                    result['language'] = 'UnKnown'
        else:
            result['language'] = 'UnKnown'
        if result['language'] == 'UnKnown':
            if result['web-servers'].lower() in ['nginx']:
                result['language'] = 'php'
            elif result['web-servers'].lower() in ['tomcat']:
                result['language'] = 'jsp'
            elif result['web-servers'].lower() in ['iis']:
                result['language'] = 'asp/aspx'
            else:
                result['language'] = 'UnKnown'
    '''
    return result

if __name__ == '__main__':
    #setConfAttribute()
    conf.target = 'http://cn.wordpress.org/'
    conf.web_method = 'GET'
    conf.timeout = 2
    data = check_fingerprint()
    print data['headers']
    print data['title'][0]
    print data['web-servers']
    print data['language']
    print data['cms']