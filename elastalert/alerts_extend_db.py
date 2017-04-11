#! /usr/bin/env python 
# -*- coding: utf-8 -*-

#from __future__ import unicode_literals 

import datetime

from alerts import Alerter, BasicMatchString

from util import elastalert_logger
from db_sqlconn import Mysql

'''
#################################################################
# 推送消息到数据库中，便于后继查询                                              #
#################################################################
'''


class DBAlerter(Alerter):

    # 数据库IP地址，数据库名称，用户名和口令必填


    def __init__(self, *args):

        super(DBAlerter, self).__init__(*args)


    def create_default_title(self, matches):

        subject = 'ElastAlert: %s' % (self.rule['name'])

        return subject

    def alert(self, matches):

        body = self.create_alert_body(matches)
        
        self.senddata(body)
        
        elastalert_logger.info("send message to %s" % "admin")

    def senddata(self, content):

        mysql = Mysql(self.rule)

        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        insert_sql = 'insert into link_alert(' \
                   'alert_userid,' \
                   'alert_username,' \
                   'alert_channel,' \
                   'alert_account,' \
                   'alert_rule,' \
                   'alert_message,' \
                   'alert_time,' \
                   'alert_status,' \
                   'alert_exception' \
                   ')  values ' \
                   '(1,"admin","2","admin@linsdom.com","frequency",%s,%s,"0","")'

        insert_data = [content, now]

        mysql.insertOne(insert_sql, insert_data)

        mysql.dispose()

        elastalert_logger.info("send msg and response: %s" % content)
       

    def get_info(self):
        return {'type': 'DBAlerter'}
