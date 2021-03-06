#!/usr/bin/env python
# -*-coding:utf-8-*-
#-*-author:scrat-*-


import MySQLdb
import sqlite3
from libs.core.data import logger

class DB():
    def __init__(self, db_type, db_name='', username='', password='', host='localhost', port=3306, charset='utf8'):
        """
        init function
        :param db_type:
        :param db_name:
        :param username:
        :param password:
        :param host:
        :param port:
        :param charset:
        :return:
        """
        if db_type is None:
            print 'Not Enter db_type!'
            exit()
        self.db_type = db_type
        self.db_name = db_name
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.charset = charset
        self.__table = ''
        self.__where = ''
        self.__like = ''

        if self.db_type == 'mysql':
            self.conn = MySQLdb.connect(
                db=self.db_name,
                host=self.host,
                user=self.username,
                passwd=self.password,
                charset=self.charset)
        elif self.db_type == 'sqlite':
            self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def get_table(self):
        """
        get current table name
        :return table_name<str>:
        """
        return self.__table

    def set_table(self, table):
        """
        set current table name
        :param table:
        :return:
        """
        if 'str' not in str(type(table)):
            print '[-] praram must be string!' + str(__file__)
            table = ''
        self.__table = table

    @staticmethod
    def _param(p):
        """
        parameter handle
        :param p:
        :return result<str> or result<dict>:
        """
        if 'dict' in str(type(p)):
            result = {}
            v = []
            k = ''
            for i in p:
                v.append(p[i])
                k += i + ','
                result = {'key': i, 'value': v}
            result = {'key': k.rstrip(','), 'value': tuple(result['value'])}
            return result
        elif 'tuple' in str(type(p)):
            result = ''
            for i in p:
                result += i + ','
            result = result.rstrip(',')
            return result

    def execute(self, sql):
        """
        execute sql
        :param sql:
        :return:
        """
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()
        except Exception as e:
            logger.error(e)
            return False

    def select(self, condition={}, field=('*')):
        """
        select data
        :param condition:
        :param field
        :return result:
        """
        if type(()) is type(field):
            field = self._param(field)
        else:
            field = ('*')
        sql = 'select %s from %s' % (field, self.__table)
        args = []
        if condition:
            condition = self._param(condition)
            sql += ' where %s=' % condition['key']
            sql += '%s'
            args.append([condition['value'][0]])
        self.cur.execute(sql, args)
        return self.cur.fetchall()


    def insert(self, field):
        """
        insert data
        :param field:
        :return bool:
        """
        fields = self._param(field)
        n = len(fields['value'])
        try:
            sql = 'insert into '+self.__table+' ('+fields['key']+') values('+(n*'%s,').rstrip(',')+')'
            self.cur.execute(sql, fields['value'])
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def update(self, field, condition):
        """
        update data
        :param field:
        :param condition:
        :return bool:
        """
        fields = self._param(field)
        con = self._param(condition)
        params = fields['key'].split(',')
        p = ''
        for param in params:
            p += param + '=%s,'
        try:
            self.cur.execute('update '+self.__table+' set '+p.rstrip(',')+' where '+con['key']+'='+con['value'][0], fields['value'])
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def delete(self, condition):
        """
        delete
        :param condition:
        :return:
        """
        condition = self._param(condition)
        sql = 'delete from %s where %s=' % (self.__table, condition['key'])
        sql += '%s'
        args = [condition['value'][0]]
        try:
            self.cur.execute(sql, args)
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def check_exist(self, condition):
        """
        existed : True
        no exist: False
        :param condition:
        :return: bool
        """
        if self.select(condition=condition):
            return True
        else:
            return False

    def close(self):
        """
        close DB
        :return:
        """
        self.cur.close()
        self.conn.close()

if __name__ == '__main__':
    t = {'hehe': 1, 'haha': 2, 'xixi': 3, 'woca': 4}
    h = DB(db_type='mysql', username='root', password='password', host='localhost', db_name='bank')

    h.set_table('host')
    a=h.select({'id': 1})
    #a=h.insert({'ip': '123', 'bank_id': '555'})
    #a=h.update({'ip': '123.456.789'}, {'id': '2'})
    #a=h.delete({'id': '2'})
    print a
    h.close()
