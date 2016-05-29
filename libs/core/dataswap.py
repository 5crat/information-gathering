#!/usr/bin/env python
# -*-coding:utf-8-*-
#-*-author:scrat-*-

from Queue import Queue
from libs.core.data import paths
from libs.core.data import conf
from libs.core.xmlhandle import XmlHandle
from libs.core.common import setConfAttribute

def _readXml(filename, node_name, parent_node='', parent_attr=''):
    xdoc = XmlHandle(filepath=paths.PAYLOAD_PATH+filename)
    datas = xdoc.getNodesAttr(node_name, parent_node, parent_attr)
    return datas

conf.fingerprint = Queue()
conf.fingerprint.put('2')
print conf.fingerprint.get()