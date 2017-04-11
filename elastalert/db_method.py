# coding:utf-8
''''' 

@author: baocheng 
'''
from db_sqlconn import Mysql
import config
import yaml


def get_rules_from_db(conf,args):

    # 申请资源
    mysql = Mysql(conf)
    rules = []
    sql_rules = "select * from link_rules;"
    result = mysql.getAll(sql_rules)
    if result:
        for row in result:
            rule_filter = yaml.load(row["rule_filter"])
            rule_extend = yaml.load(row["rule_extend"])
            rule = {'index': '',
                    'name': '',
                    'realert': {'minutes': 1},
                    'from_addr': conf['from_addr'],
                    'smtp_host': conf['smtp_host'],
                    'smtp_port':  conf['smtp_port'],
                    'smtp_auth_file': '',
                    'num_events': 1,
                    'alert': ['db'],
                    'filter': [{'query': {'query_string': {'query': 'field6:Exception'}}}],
                    'email_reply_to': '',
                    'rule_file': 'example_rules/example_frequency.yaml',
                    'timeframe': {'minutes': 1},
                    'type': 'frequency',
                    'email': ['286388651@qq.com']}

            rule['name'] = row["rule_name"]
            rule['index'] = row["rule_index"]
            rule['realert'] = rule_extend['realert']
            rule['num_events'] = rule_extend['num_events']

            rule['timeframe'] = rule_extend['timeframe']

            queryDictValueSql = "select dict_name as rule_type from link_dict_entry where dict_type_code = 'alertRuletypes' and dict_code = %s"

            queryParam = [row["rule_type"]]

            ruleType = mysql.getOne(queryDictValueSql,queryParam)

            rule['type'] = ruleType['rule_type']
            rule['filter'] = rule_filter['filter']

            print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
            row["id"], row["rule_name"], row["rule_type"], row["rule_index"], row["rule_desc"], row["rule_alerts"],
            row["rule_filter"], row["rule_extend"], row["rule_seq"])

            config.load_options(rule, conf, '', args)
            config.load_modules(rule, args)

            rules.append(rule)

    # 释放资源
    mysql.dispose()

    return rules


# get_all_rules = get_rules_from_db()