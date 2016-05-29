#!/usr/bin/env python
# -*-coding:utf-8-*-
#-*-author:scrat-*-


class FingerPrintRules:
    LanguageRegex = "x-powered-by:(\S*)\s"
    WebServerRegex = "server:(\S*)\s"
    FromRegex = "<form.*?action ?= ?\"(.*?)\""
    TitleRegex = "<title>(.*)</title>"

class CmsFingerPrintRules:
    WordPressRegex = "<\S* href=\"\S*wp-includes/"
    #.......

class ResponseHeadersRules:

    LengthRegex = "Content-Length:\S*"
    ContentTypeRules = "Content-Type:\S*"