#!/usr/bin/env python
# -*- coding:utf-8 -*-
from  Process_Stat import Process_Stat

process_stat = Process_Stat()

query_data = {"query": {
                 "filtered": {
                    "filter": {
                        "term": {
                            "processchname": "denver"
                        }
                    }
                 }
                }
            }

post_filter = { "post_filter": {
                    "term": {
                        "processdefname": "oa_flow_zhongzi.oa_flow_gw_yy.oa_flow_gw_yy_bumen"
                    }
                  }
              }

aggs_query = { "size" : 0,
               "aggregations": {
                   "aggr_processinst_time":{
                     "stats":{
                       "field": "subtime"
                    }
                }
               }
            }

aggs_script_query = { "size" : 0,
                       "aggregations": {
                           "aggr_processinst_time":{
                            "stats":{
                                "field": "subtime",
                                "script": {
                                    "lang": "painless",
                                    "inline": "_value * params.correction",
                                    "params": {
                                        "correction": 1.2
                                    }
                                }
                            }
                        }
                       }
                    }

aggs_script_gettogether_query = {"size": 0,
                                 "aggregations": {
                                       "attendees_stats": {
                                        "stats": {
                                            "script": "doc['attendees'].values.length"

                                            }
                                        }
                                    }
                                }

# 高级统计
aggs_advanced_query = { "size" : 0,
               "aggregations": {
                   "aggr_processinst_time":{
                     "extended_stats": {
                       "field": "subtime"
                    }
                }
               }
            }
#近似度分析，参与人员80%-90%的长度是多少？
percentile_query = { "size" : 0,
                     "aggregations": {
                        "attendees_percentiles": {
                            "percentiles": {
                                "script": "doc['"'attendees'"'].values.length",
                                "percents": [80, 99]
                            }
                            }
                    }
}
percentile_rank_query = {"size":0,
                          "aggs": {
                            "members_aggres": {
                              "percentile_ranks": {
                                "script": "doc['"'attendees'"'].values.length",
                                "values": [
                                  2,
                                  3
                                ]
                              }
                            }
                          }
                        }
#
cardinality_query = { "size":0,
                      "aggregations": {
                        "members_cardinality": {
                            "cardinality": {
                                "field": "members"
                            }
                        }
                      }
                    }

#process_stat.query("get-together", "event", percentile_query)
process_stat.query("get-together", "group", cardinality_query)
#process_stat.query("index_stat_processdefine", "type_stat_processdefine", aggs_query)
#process_stat.query("index_stat_process_processinst", "type_stat_process_processinst",aggs_advanced_query)
# process_stat.query("index_stat_process_activityinst", "type_stat_process_activityinst")
# process_stat.query("index_stat_process_workitem", "type_stat_process_workitem")