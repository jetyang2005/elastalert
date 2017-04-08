#! /usr/bin/env python 
# -*- coding: utf-8 -*-

#from __future__ import unicode_literals 
import urllib,urllib2
import json
import sys
import datetime
import MySQLdb as mdb
from alerts import Alerter, BasicMatchString
from requests.exceptions import RequestException
from util import elastalert_logger
from util import EAException
import requests

'''
#################################################################
# 推送消息到数据库中，便于后继查询                                              #
#################################################################
'''
class DBAlerter(Alerter):

    #数据库IP地址，数据库名称，用户名和口令必填

    required_options = frozenset(['db_ip','db_database','db_username','db_password'])

    def __init__(self, *args):

        super(DBAlerter, self).__init__(*args)
        self.db_ip = self.rule.get('db_ip', '')     #企业号id
        self.db_database = self.rule.get('db_database', '')       #secret
        self.db_username = self.rule.get('db_username', '')   #应用id
        self.db_password = self.rule.get('db_password')       #部门id


    def create_default_title(self, matches):

        subject = 'ElastAlert: %s' % (self.rule['name'])

        return subject

    def alert(self, matches):

        body = self.create_alert_body(matches)
        
        self.senddata(body)
        
        elastalert_logger.info("send message to %s" % "admin")

    def senddata(self, content):

        con = None
        try:
            # 连接 mysql 的方法： connect('ip','user','password','dbname')
            con = mdb.connect(self.db_ip, self.db_username, self.db_password, self.db_database)

            # 所有的查询，都在连接 con 的一个模块 cursor 上面运行的
            cur = con.cursor()

            now = datetime.datetime.now()
            now = now.strftime("%Y-%m-%d %H:%M:%S")

            # 以下插入了 5 条数据
            cur.execute('insert into link_alert(alert_userid,alert_username,alert_channel,alert_account,alert_rule,alert_message,alert_time,alert_status,alert_exception) '
                        'values (1,"admin","2","admin@linsdom.com","frequency","%s","%s","0","") ' % (content,now))


        except Exception as e:
            print(e)

        finally:
            if con:
                # 无论如何，连接记得关闭
                cur.close()
                con.commit()
                con.close()
        
        elastalert_logger.info("send msg and response: %s" % content)
       

    def get_info(self):
        return {'type': 'DBAlerter'}
