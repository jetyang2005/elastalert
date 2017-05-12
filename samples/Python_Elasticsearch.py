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

class ElasticsearchOperate():

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

        # extra_args = {'_source_include': ['@timestamp', '*']}
        #
        # query = {'sort': [{'@timestamp': {'order': 'asc'}}],
        #  'query':
        #      {'bool':
        #           {'filter':
        #                {'bool':
        #                     {'must':
        #                          [{'range':
        #                                {'@timestamp': {'gt': '2017-04-06T14:30:00.860000+08:00',
        #                                                'lte': '2017-04-06T14:31:00.860000+08:00'}}},
        #                           {u'query_string': {u'query': u'field6:Exception'}
        #
        #                            }
        #                           ]
        #                      }
        #                 }
        #            }
        #       }
        #  }

        res = self.es.search(scroll='30s', index='index-student', size=10000, body=query, ignore_unavailable=True)

        self.elastalert_logger.info(str(res).decode("unicode_escape").encode("utf8"))


    def create_index(self):

        if self.es.indices.exists(index='index-student') is not True:

            test_index_mapping = {"mappings": {
                                    "type_student": {
                                            "properties": {
                                              "studentNo": {
                                                "type": "string",
                                                "index": "not_analyzed"
                                              },
                                              "name": {
                                                "type": "string",
                                                "index": "analyzed",
                                                "analyzer": "ik"
                                              },
                                              "male": {
                                                "type": "string",
                                                "index": "not_analyzed"
                                              },
                                              "age": {
                                                "type": "integer"
                                              },
                                              "birthday": {
                                                "type": "date",
                                                "format": "yyyy-MM-dd"
                                              },
                                              "address": {
                                                "type": "string",
                                                "index": "analyzed",
                                                "analyzer": "ik"
                                              },
                                              "classNo": {
                                                "type": "string",
                                                "index": "not_analyzed "
                                              },
                                              "isLeader": {
                                                "type": "boolean"
                                              }
                                            }
                                          }
                                        }
                                    }

            self.es.indices.create(index="index-student",  ignore=400, body=test_index_mapping)

    def create_data(self, esdatas):
        self.elastalert_logger.info(str(esdatas).decode("unicode_escape").encode("utf8"))
        helpers.bulk(self.es, esdatas)

    def init_data(self):

        data = xlrd.open_workbook('/Users/yangwm/log/elasticsearch_data.xls')  # 打开xls文件
        table = data.sheets()[0]  # 打开第一张表
        esdatas = []
        nrows = table.nrows  # 获取表的行数
        for i in range(nrows):  # 循环逐行打印
            if i == 0:  # 跳过第一行)
                continue
            rows = table.row_values(i)

            esdata = {
                        "_index": "index-student",
                        "_type": "type_student",
                        "_id": i,
                        "_source": {
                            "studentNo": str(rows[0]),
                            "name": str(rows[1]),
                            "male": str(rows[2]),
                            "age": int(rows[3]),
                            "birthday": xlrd.xldate.xldate_as_datetime(rows[4], 1),
                            "classNo": str(rows[5]),
                            "address": str(rows[6]),
                            "isLeader": rows[7]
                        }
                     }
            esdatas.append(esdata)

        #print str(esdatas)

            helpers.bulk(self.es, esdatas)


esclient = ElasticsearchOperate()

esclient.create_index()

#esclient.init_data()

# query_str = {
#               "query": {
#                 "match_all": {}
#               }
#             }
#
# esclient.queryData(query_str)

# query_str_withpage = {
#                           "query": {
#                             "match_all": {}
#                           },
#                           "from": 2,
#                           "size": 4,
#                           "sort": {
#                             "studentNo": {
#                               "order": "asc"
#                             }
#                           }
#                     }
#
# esclient.queryData(query_str_withpage)

# term_str_query = {
#                       "query": {
#                         "term": {
#                           "name": "关羽"
#                         }
#                       }
#                     }
#
# esclient.queryData(term_str_query)

bool_str_query = {"query": {
                    "bool": {
                      "must": [
                        {
                          "term": {
                            "classNo": "2.0"
                          }
                        },
                        {
                          "term": {
                            "isLeader": "1"
                          }
                        }
                      ]
                    }
                  }
                }

esclient.queryData(bool_str_query)




