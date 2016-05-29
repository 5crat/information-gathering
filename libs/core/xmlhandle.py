#!/usr/bin/env python
#-*-coding:utf-8-*-
#-*-author:scrat-*-

from lxml import etree

class XmlHandle(object):
    """
    XML Operating Class
    """
    def __init__(self, rootnode=None, filepath=None):
        if rootnode is None and filepath is not None:
            self.xdoc = etree.parse(filepath)
            self.rootNode = self.xdoc.getroot()
        elif rootnode is not None and filepath is None:
            self.rootNode = etree.Element(rootnode)
        else:
            self.rootNode = etree.Element('root')


    def addNode(self, parent_node, child_node):
        """
        add one node
        :param parent_node:
        :param child_node:
        :return:
        """
        return etree.SubElement(parent_node, child_node)

    def addNodeAttribute(self, parent_node, child_node, attribute):
        """
        add one node and attribute
        :param parent_node:
        :param child_node:
        :param attribute:
        :return:
        """
        return etree.SubElement(parent_node, child_node, attribute)

    def getNode(self, node_name):
        """
        get node
        :param node_name:
        :return node:
        """
        return self.rootNode.xpath(node_name)
    def getNodeAttr(self, node_name, attr, parent_node='', parent_attr=''):
        """
        get One Node Attribute Value
        :param node_name:
        :param attr:
        :return:
        """
        if parent_node is not '' and parent_attr is not '':
            node = self.rootNode.xpath("//"+parent_node+"[@value='"+parent_attr+"']/"+node_name+"[@"+attr+"]")
        elif parent_node is not '':
            node = self.rootNode.xpath("//"+parent_node+"/"+node_name+"[@"+attr+"]")
        else:
            node = self.rootNode.xpath('//'+node_name+'[@'+attr+']')
        value = node[0].get(attr)
        return value

    def getNodes(self, node_name):
        """
        get node list
        :param node_name:
        :return nodes (list):
        """
        nodes = []
        for i in self.rootNode.xpath(node_name):
            nodes.append(i)
        return nodes

    def getNodesAttr(self, node_name, attr, parent_node='', parent_attr=''):
        """
        get same node same attribute value
        :param node_name:
        :param attr:
        :return:
        """
        values = []
        if parent_node is not '' and parent_attr is not '':
            nodes = self.rootNode.xpath("//"+parent_node+"[@value='"+parent_attr+"']/"+node_name+"[@"+attr+"]")
        elif parent_node is not '':
            nodes = self.rootNode.xpath("//"+parent_node+"/"+node_name+"[@"+attr+"]")
        else:
            nodes = self.rootNode.xpath('//'+node_name+'[@'+attr+']')
        for node in nodes:
            values.append(node.get(attr))
        return values

if __name__ == '__main__':
    a = XmlHandle(filepath='../../payload/fingerprint_rules.xml')
    b = a.getNodesAttr('payload', 'value', parent_node='cms', parent_attr='wordpress')
    for i in b:
        print i
    print len(b)