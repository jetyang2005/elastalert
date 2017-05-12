#!/usr/bin/env python
# -*- coding:utf-8 -*-

from elasticsearch import Elasticsearch
from elasticsearch import helpers
import logging
import xlrd
import datetime
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )

class Process_Stat():

    def __init__(self):

        # 日志基本配置，将日志文件输出到当前目录下的elastticsearch_sample.log文件中
        logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='elastticsearch_sample.log',
                filemode='w')

        # 将日志打印在屏幕上

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

        self.elastalert_logger = logging.getLogger('elasticsearch_test')

        # 连接elasticsearch

        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def queryData(self, query):

        res = self.es.search(scroll='30s', index='index-student', size=10000, body=query, ignore_unavailable=True)

        self.elastalert_logger.info(str(res).decode("unicode_escape").encode("utf8"))

    def query(self, index_name, type_name, querybody):

        res = self.es.search(index=index_name, doc_type=type_name, body=querybody)
        print(" res value is : "+str(res).decode("unicode_escape").encode("utf8"))

    def query_index(self, index_name, querybody):

        res = self.es.search(index=index_name, body=querybody)
        print(" res value is : "+str(res).decode("unicode_escape").encode("utf8"))

    def query_count(self, index_name , type_name):

        res = self.es.search(index=index_name, doc_type=type_name, body={"query":{"match_all":{}}})

        print(index_name +" Got %d Hits: " % res.get("hits").get("total"))

    def create_data(self, esdatas):
        self.elastalert_logger.info(str(esdatas).decode("unicode_escape").encode("utf8"))
        helpers.bulk(self.es, esdatas)

    def create_index(self):

            # processdefine
            if self.es.indices.exists(index='index_stat_processdefine') :
                self.es.indices.delete("index_stat_processdefine")
            processdef_index_mapping = {"mappings": {
                                    "type_stat_processdefine": {
                                            "properties": {
                                              "processdefname": {
                                                "type": "string",
                                                "index": "not_analyzed"
                                              },
                                              "processchname": {
                                                    "type": "string",
                                                    "index": "not_analyzed"
                                                },
                                              "versionsign": {
                                                    "type": "string",
                                                    "index": "not_analyzed"
                                                },
                                              "createtime": {
                                                "type": "date",
                                                "format": "yyyy-MM-dd HH:mm:ss"
                                              }
                                            }
                                          }
                                        }
                                    }
            self.es.indices.create(index="index_stat_processdefine", ignore=400,
                                       body=processdef_index_mapping)

            # process
            if self.es.indices.exists(index='index_stat_process_processinst') :
                self.es.indices.delete("index_stat_process_processinst")
            processinst_index_mapping = {"mappings": {
                                    "type_stat_process_processinst": {
                                            "properties": {
                                              "processinstid": {
                                                "type": "string",
                                                "index": "not_analyzed"
                                              },
                                              "processinstname": {
                                                "type": "string",
                                                "index": "analyzed"
                                              },
                                              "processdefname": {
                                                "type": "string",
                                                "index": "not_analyzed"
                                              },
                                              "processchname": {
                                                    "type": "string",
                                                    "index": "not_analyzed"
                                                },
                                              "versionsign": {
                                                    "type": "string",
                                                    "index": "not_analyzed"
                                                },
                                              "currentstate": {
                                                    "type": "string",
                                                    "index": "not_analyzed"
                                                },
                                              "createtime": {
                                                "type": "date",
                                                "format": "yyyy-MM-dd HH:mm:ss"
                                              },
                                              "endtime": {
                                                "type": "date",
                                                "format": "yyyy-MM-dd HH:mm:ss"
                                              },
                                              "subtime": {
                                                "type": "integer"
                                              }
                                            }
                                          }
                                        }
                                    }
            self.es.indices.create(index="index_stat_process_processinst", ignore=400,
                                       body=processinst_index_mapping)
            # activity
            if self.es.indices.exists(index='index_stat_process_activityinst') :
                self.es.indices.delete("index_stat_process_activityinst")
            activityinst_index_mapping = {"mappings": {
                                    "type_stat_process_activityinst": {
                                            "properties": {
                                              "processinstid": {
                                                "type": "string",
                                                "index": "not_analyzed"
                                              },
                                              "processinstname": {
                                                "type": "string",
                                                "index": "analyzed"
                                              },
                                              "versionsign": {
                                                "type": "string",
                                                "index": "not_analyzed"
                                              },
                                              "processdefname": {
                                                    "type": "string",
                                                    "index": "not_analyzed"
                                                },
                                             "processchname": {
                                                    "type": "string",
                                                    "index": "not_analyzed"
                                                },
                                              "activityinstid": {
                                                "type": "string",
                                                "index": "not_analyzed"
                                              },
                                              "activityinstname": {
                                                    "type": "string",
                                                    "index": "not_analyzed"
                                                },
                                              "currentstate": {
                                                    "type": "string",
                                                    "index": "not_analyzed"
                                                },
                                              "createtime": {
                                                "type": "date",
                                                "format": "yyyy-MM-dd HH:mm:ss"
                                              },
                                              "endtime": {
                                                "type": "date",
                                                "format": "yyyy-MM-dd HH:mm:ss"
                                              },
                                              "subtime": {
                                                "type": "integer"
                                              }
                                            }
                                          }
                                        }
                                    }
            self.es.indices.create(index="index_stat_process_activityinst", ignore=400,
                                       body=activityinst_index_mapping)

            # workitem
            if self.es.indices.exists(index='index_stat_process_workitem') :
                self.es.indices.delete("index_stat_process_workitem")
            workitem_index_mapping = {"mappings": {
                        "type_stat_process_workitem": {
                            "properties": {
                                "processinstid": {
                                    "type": "string",
                                    "index": "not_analyzed"
                                },
                                "processinstname": {
                                    "type": "string",
                                    "index": "analyzed"
                                },
                                "processdefname": {
                                    "type": "string",
                                    "index": "not_analyzed"
                                },
                                "processchname": {
                                    "type": "string",
                                    "index": "analyzed"
                                },
                                "workitemid": {
                                    "type": "string",
                                    "index": "not_analyzed"
                                },
                                "workitemname": {
                                    "type": "string",
                                    "index": "not_analyzed"
                                },
                                "currentstate": {
                                    "type": "string",
                                    "index": "not_analyzed"
                                },
                                "istimeout": {
                                    "type": "string",
                                    "index": "not_analyzed"
                                },
                                "timeoutnum": {
                                    "type": "integer"
                                },
                                "createtime": {
                                    "type": "date",
                                    "format": "yyyy-MM-dd HH:mm:ss"
                                },
                                "endtime": {
                                    "type": "date",
                                    "format": "yyyy-MM-dd HH:mm:ss"
                                },
                                "activityinstid": {
                                    "type": "string",
                                    "index": "analyzed"
                                },
                                "activityinstname": {
                                    "type": "string",
                                    "index": "analyzed"
                                },
                                "userid": {
                                    "type": "string",
                                    "index": "analyzed"
                                },
                                "orgid": {
                                    "type": "string",
                                    "index": "not_analyzed"
                                },
                                "orgname": {
                                    "type": "string",
                                    "index": "analyzed"
                                }
                            }
                        }
                    }
                }

            self.es.indices.create(index="index_stat_process_workitem",  ignore=400, body=workitem_index_mapping)

# esclient = Process_Stat()
#
# #esclient.create_index()
# esclient.query_count("index_stat_processdefine", "type_stat_processdefine")
# esclient.query_count("index_stat_process_processinst", "type_stat_process_processinst")
# esclient.query_count("index_stat_process_activityinst", "type_stat_process_activityinst")
# esclient.query_count("index_stat_process_workitem", "type_stat_process_workitem")





