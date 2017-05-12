#!/usr/bin/env python
# -*- coding:utf-8 -*-
from  Process_Stat import Process_Stat

process_stat = Process_Stat()

terms_data = { "size": 0,
                "aggregations": {
                  "tags": {
                    "terms": {
                        "field": "tags.verbatim",
                        "order": {
                            "_term": "asc"
                            }
                    }
                  }
                }
}

terms_incluede_data = { "size": 0,
                        "aggregations": {
                          "tags": {
                            "terms": {
                                "field": "tags.verbatim",
                                "include": {
                                      "pattern": ".*search.*"
                                }
                            }
                          }
                        }
}


significant_terms  = { "size":0,
                        "query": {
                            "match": {
                                "attendees": "Lee"
                            }
                        },
                        "aggregations": {
                            "significant_attendees": {
                                    "significant_terms": {
                                        "field": "attendees",
                                        "min_doc_count": 2,
                                        "exclude": "lee"
                          } }
                        }}

range_query = {"size":0,
                "aggregations": {
                    "attendees_breakdown": {
                        "range": {
                            "script": "doc['"'attendees'"'].values.length",
                            "ranges": [
                                { "to": 4 },
                                { "from": 4, "to": 6 },
                                { "from": 6 }
                            ]
                        }
                    }
                 }
               }
date_ranger_query = { "aggregations": {
                            "dates_breakdown": {
                                "date_range": {
                                    "field": "date",
                                    "format": "YYYY.MM",
                                    "ranges": [
                                            { "to": "2013.07" },
                                            {"from": "2013.07"}
                                    ]
                                }
                            }
                        }
                    }
histogram_query = { "size": 0,
                        "aggregations": {
                            "attendees_histogram": {
                                "histogram": {
                                        "script": "doc['"'attendees'"'].values.length",
                                        "interval": 1
                                }
                            }
                        }
                    }
date_histogram_query = { "size":0,
                            "aggregations": {
                                "event_dates": {
                                    "date_histogram": {
                                        "field": "date",
                                        "interval": "1M"
                                    }
                                }
                            }
                        }
#process_stat.query("get-together", "event", terms_data)
process_stat.query("get-together", "group", terms_incluede_data)
#process_stat.query("index_stat_processdefine", "type_stat_processdefine", aggs_query)
#process_stat.query("index_stat_process_processinst", "type_stat_process_processinst",aggs_advanced_query)
# process_stat.query("index_stat_process_activityinst", "type_stat_process_activityinst")
# process_stat.query("index_stat_process_workitem", "type_stat_process_workitem")