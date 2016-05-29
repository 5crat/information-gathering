#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, DateTime, LargeBinary, Text, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from libnmap.plugins.backendplugin import NmapBackendPlugin
from libnmap.reportjson import ReportEncoder, ReportDecoder

import json
from datetime import datetime
import binascii

Base = declarative_base()

class NmapSqlPlugin(NmapBackendPlugin):
    """
        This class handle the persistence of NmapRepport object in SQL backend
        Implementation is made using sqlalchemy(0.8.1)
        usage :

        #get a nmapReport object
        from libnmap.parser import NmapParser
        from libnmap.reportjson import ReportDecoder, ReportEncoder
        import json
        nmap_report_obj = NmapParser.parse_fromfile(
               '/home/vagrant/python-nmap-lib/libnmap/test/files/1_hosts.xml')

         #get a backend with in memory sqlite
         from libnmap.plugins.backendpluginFactory import BackendPluginFactory
         mybackend_mem = BackendPluginFactory.create(plugin_name='sql',
                                                     url='sqlite://',
                                                     echo=True)

         mybackend_mysql = BackendPluginFactory.create(plugin_name='sql',
                            url='mysql+mysqldb://scott:tiger@localhost/foo',
                            echo=True)
         mybackend = BackendPluginFactory.create(plugin_name='sql',
                                        url='sqlite:////tmp/reportdb.sql',
                                        echo=True)
         #lets save!!
         nmap_report_obj.save(mybackend)
         mybackend.getall()
         mybackend.get(1)
    """
    class Reports(Base):
        """
            Embeded class for ORM map NmapReport to a
            simple three column table
        """
        __tablename__ = 'result_ports'

        id = Column('id', Integer, primary_key=True)
        taskid = Column('taskid', Integer)
        inserted = Column('inserted', DateTime(), default='now')
        address = Column('address', String(256))
        port = Column('port', Integer)
        service = Column('service', String(256))
        state = Column('state', String(12))
        protocol = Column('protocol', String(12))
        product = Column('product', String(64))
        product_version = Column('product_version', String(64))
        product_extrainfo = Column('product_extrainfo', String(128))
        # banner = Column('banner', String(256))
        scripts_results = Column('scripts_results', Text)

        def __init__(self, obj_NmapReport):
            self.inserted = datetime.fromtimestamp(int(obj_NmapReport.endtime))
            self.taskid = obj_NmapReport.taskid
            self.address = obj_NmapReport.address
            self.port = obj_NmapReport.port
            self.service = obj_NmapReport.service
            self.state = obj_NmapReport.state
            self.protocol = str(obj_NmapReport.protocol)
            self.product = str(obj_NmapReport.product)
            self.product_version = str(obj_NmapReport.product_version)
            self.product_extrainfo = str(obj_NmapReport.product_extrainfo)
            # self.banner = str(obj_NmapReport.banner)
            # self.scripts_results = binascii.b2a_hex(str(obj_NmapReport.scripts_results))

            if len(obj_NmapReport.scripts_results) > 0:                
                self.scripts_results = obj_NmapReport.scripts_results[0]['output']
            else:
                self.scripts_results = None


        def decode(self):
            json_decoded = self.report_json.decode('utf-8')
            nmap_report_obj = json.loads(json_decoded,
                                         cls=ReportDecoder)
            return nmap_report_obj

    def __init__(self, **kwargs):
        """
            constructor receive a **kwargs as the **kwargs in the sqlalchemy
            create_engine() method (see sqlalchemy docs)
            You must add to this **kwargs an 'url' key with the url to your
            database
            This constructor will :
            - create all the necessary obj to discuss with the DB
            - create all the mapping(ORM)

            todo : suport the : sqlalchemy.engine_from_config

            :param **kwargs:
            :raises: ValueError if no url is given,
                    all exception sqlalchemy can throw
            ie sqlite in memory url='sqlite://' echo=True
            ie sqlite file on hd url='sqlite:////tmp/reportdb.sql' echo=True
            ie mysql url='mysql+mysqldb://scott:tiger@localhost/foo'
        """
        NmapBackendPlugin.__init__(self)
        self.engine = None
        self.url = None
        self.Session = sessionmaker()

        if 'url' not in kwargs:
            raise ValueError
        self.url = kwargs['url']
        del kwargs['url']
        try:
            self.engine = create_engine(self.url, **kwargs)
            Base.metadata.create_all(bind=self.engine, checkfirst=True)
            self.Session.configure(bind=self.engine)
        except:
            raise

    def insert(self, nmap_report):
        """
           insert NmapReport in the backend

           :param NmapReport:

           :returns: the ident of the object in the backend for future usage \
           or None
        """
        sess = self.Session()
        report = NmapSqlPlugin.Reports(nmap_report)
        sess.add(report)
        sess.commit()
        reportid = report.id
        sess.close()
        return reportid if reportid else None

    def get(self, report_id=None):
        """
            retreive a NmapReport from the backend

            :param id: str

            :returns: NmapReport
        """
        if report_id is None:
            raise ValueError
        sess = self.Session()
        our_report = (
            sess.query(NmapSqlPlugin.Reports).filter_by(id=report_id).first())
        sess.close()
        return our_report.decode() if our_report else None

    def getall(self):
        """
            :param filter: Nice to have implement a filter capability

            :returns: collection of tuple (id,NmapReport)
        """
        sess = self.Session()
        nmapreportList = []
        for report in (
                sess.query(NmapSqlPlugin.Reports).
                order_by(NmapSqlPlugin.Reports.inserted)):
            nmapreportList.append((report.id, report.decode()))
        sess.close()
        return nmapreportList

    def delete(self, report_id=None):
        """
            Remove a report from the backend

            :param id: str

            :returns: The number of rows deleted
        """
        if report_id is None:
            raise ValueError
        nb_line = 0
        sess = self.Session()
        nb_line = sess.query(NmapSqlPlugin.Reports).\
            filter_by(id=report_id).delete()
        sess.commit()
        sess.close()
        return nb_line
