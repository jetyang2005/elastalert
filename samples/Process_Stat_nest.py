#!/usr/bin/env python
# -*- coding:utf-8 -*-
from  Process_Stat import Process_Stat

process_stat = Process_Stat()
nest_aggres_query = {   "size": 0,
                        "aggregations": {
                            "top_tags": {
                                "terms": {
                                    "field": "tags.verbatim"
                                },
                                "aggregations": {
                                    "groups_per_month": {
                                        "date_histogram": {
                                            "field": "created_on",
                                            "interval": "1M"
                                        }
                                #         ,
                                #     "aggregations": {
                                #         "number_of_members": {
                                #             "range": {
                                #                 "script": "doc['"'members'"'].values.length",
                                #             "ranges": [
                                #                 {"to": 3},
                                #                 {"from": 3}
                                #             ]
                                #         }
                                #
                                #     }
                                # }
                            }
                        }
                    }
                 }
             }

nested_get_group = {"size":0,
                    "aggregations": {
                            "frequent_attendees": {
                                "terms": {
                                    "field": "attendees",
                                    "size": 2
                                },
                                "aggregations": {
                                    "recent_events": {
                                        "top_hits": {
                                            "sort": {
                                                "date": "desc"
                                            },
                                            "_source": {
                                                "include": [ "title" ]
                                            },
                                            "size": 1
                                        }
                                    }
                                }
                            }
                        }
                    }


bank_query = {
                  "query": {
                    "query_string": {
                      "query": "*",
                      "analyze_wildcard": "true"
                    }
                  },
                  "size": 0,
                  "_source": {
                    "excludes": []
                  },
                  "aggs": {
                    "2": {
                      "range": {
                        "field": "balance",
                        "ranges": [
                          {
                            "from": 0,
                            "to": 1000
                          },
                          {
                            "from": 985,
                            "to": 2000
                          },
                          {
                            "from": 2001,
                            "to": 6000
                          },
                          {
                            "from": 6001,
                            "to": 10000
                          },
                          {
                            "from": 10001,
                            "to": 20000
                          },
                          {
                            "from": 20001,
                            "to": 50000
                          }
                        ]
                      },
                      "aggs": {
                        "3": {
                          "terms": {
                            "field": "age",
                            "size": 5,
                            "order": {
                              "_count": "desc"
                            }
                          }
                        }
                      }
                    }
                  }
                }

#process_stat.query("get-together", "event", bank_query)
process_stat.query_index("bank", bank_query)
#process_stat.query("get-together", "group", nested_get_group)
#process_stat.query("index_stat_processdefine", "type_stat_processdefine", aggs_query)
#process_stat.query("index_stat_process_processinst", "type_stat_process_processinst",aggs_advanced_query)
# process_stat.query("index_stat_process_activityinst", "type_stat_process_activityinst")
# process_stat.query("index_stat_process_workitem", "type_stat_process_workitem")