#!/usr/bin/env python
# -*-coding:utf-8-*-
#-*-author:scrat-*-

import os
import sys
import glob
from lxml import etree

def read_file(filename, root):
    with open(filename, 'r') as f:
        fn = get_file_name(filename)
        if check_same_node(root, fn) == False:
            root.append(etree.Element('cms', value=fn))
            for line in f.readlines():
                line = line.split('|')[0].strip()
                if check_same_value(root, '//cms/payload[@value]', line) == False:
                    root.xpath("//cms[@value='"+fn+"']")[0].append(etree.Element('payload', value=line))

def get_file_name(filepath):
     return str(os.path.splitext(filepath)[0].split('/')[-1].lower())

def check_same_value(root, node, value):

    if root.xpath(node):
        return False
    for i in root.xpath(node):
        if i.get('value') == value:
            return True
    return False


def check_same_node(root, node):
    try:
        if root.xpath(node)[0].get('value') == node:
            return True
        return False
    except IndexError:
        return False

def write_file(data):
    with open('fingerprint_rules.xml', 'a+') as f:
        f.writelines(data)

def main(filepath):
    root = etree.Element("root")
    for i in glob.glob(filepath):
        read_file(filename=i, root=root)
    write_file(etree.tostring(root, pretty_print=True))

if __name__ == '__main__':
    #filepath = sys.argv[1]
    main('zwsb/*')