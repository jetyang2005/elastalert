# coding:utf-8
''''' 

@author: baocheng 
'''
from db_sqlconn import Mysql
import config
import yaml


def get_rules_from_db(conf, args):

    # 申请资源
    mysql = Mysql(conf)
    rules = []
    sql_rules = "select * from link_rules;"
    result = mysql.getAll(sql_rules)
    if result:
        for row in result:

            query_dictvalue_sql = "select dict_name as rule_type from link_dict_entry " \
                                "where dict_type_code = 'alertRuletypes' and dict_code = %s"

            query_dictvalue_param = [row["rule_type"]]

            rule_type = mysql.getOne(query_dictvalue_sql, query_dictvalue_param)

            query_alertperson_sql = "select * from ( " \
                                    " select  u.id as user_id,u.user_name as user_name ,u.email as user_email " \
                                    "from LINK_RULE_RECEIVER a  ,link_role r,link_user_role ur,link_user u  " \
                                    "where a.RULE_RECEIVER_TYPE='0'  and a.RULE_RECEIVER_ID = r.id and r.id = ur.role_id " \
                                    " and ur.user_id=u.id and a.rule_id = %s " \
                                    "union " \
                                    "select  a.RULE_RECEIVER_ID as user_id,c.user_name as user_name,c.email as user_email " \
                                    "from LINK_RULE_RECEIVER a  join link_user c on a.RULE_RECEIVER_ID=c.id   " \
                                    "where a.RULE_RECEIVER_TYPE=1 and a.rule_id = %s " \
                                    ") alertpersons "

            query_alertperson_param = [row['id'], row['id']]

            alertpersons = mysql.getAll(query_alertperson_sql, query_alertperson_param)

            if rule_type['rule_type'] == 'frequency':
                rule = frequency_rule(conf, row)

            config.load_options(rule, conf, '', args)
            config.load_modules(rule, args)
            rule['alertpersons'] = alertpersons
            rule['rule_id'] = row['id']
            rule['rule_type'] = 'frequency'
            rules.append(rule)

    # 释放资源
    mysql.dispose()

    return rules


def frequency_rule(conf, row):

    rule = {'index': '',
            'name': '',
            'realert': {'minutes': 1},
            'from_addr': conf['from_addr'],
            'smtp_host': conf['smtp_host'],
            'smtp_port': conf['smtp_port'],
            'smtp_auth_file': '',
            'num_events': 1,
            'alert': ['db'],
            'filter': [{'query': {'query_string': {'query': 'field6:Exception'}}}],
            'email_reply_to': '',
            'rule_file': 'rule from db table',
            'timeframe': {'minutes': 1},
            'type': 'frequency',
            'email': ['286388651@qq.com']}

    rule_filter = yaml.load(row["rule_filter"])
    rule_extend = yaml.load(row["rule_extend"])

    rule['name'] = row["rule_name"]
    rule['index'] = row["rule_index"]
    rule['realert'] = rule_extend['realert']
    rule['num_events'] = rule_extend['num_events']
    rule['timeframe'] = rule_extend['timeframe']
    rule['type'] = 'frequency'
    rule['filter'] = rule_filter['filter']

    print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
        row["id"], row["rule_name"], row["rule_type"], row["rule_index"], row["rule_desc"], row["rule_alerts"],
        row["rule_filter"], row["rule_extend"], row["rule_seq"])

    return rule


def spike_rule(conf, row):

    rule = {'index': '',
            'name': '',
            'realert': {'minutes': 1},
            'from_addr': conf['from_addr'],
            'smtp_host': conf['smtp_host'],
            'smtp_port': conf['smtp_port'],
            'smtp_auth_file': '',
            'num_events': 1,
            'alert': ['db'],
            'filter': [{'query': {'query_string': {'query': 'field6:Exception'}}}],
            'email_reply_to': '',
            'rule_file': 'example_rules/example_frequency.yaml',
            'timeframe': {'minutes': 1},
            'type': 'frequency',
            'email': ['286388651@qq.com']}

    return rule


def cardinality_rule(conf, row):

    rule = {'index': '',
            'name': '',
            'realert': {'minutes': 1},
            'from_addr': conf['from_addr'],
            'smtp_host': conf['smtp_host'],
            'smtp_port': conf['smtp_port'],
            'smtp_auth_file': '',
            'num_events': 1,
            'alert': ['db'],
            'filter': [{'query': {'query_string': {'query': 'field6:Exception'}}}],
            'email_reply_to': '',
            'rule_file': 'example_rules/example_frequency.yaml',
            'timeframe': {'minutes': 1},
            'type': 'frequency',
            'email': ['286388651@qq.com']}

    return rule


def change_rule(conf, row):
        rule = {'index': '',
                'name': '',
                'realert': {'minutes': 1},
                'from_addr': conf['from_addr'],
                'smtp_host': conf['smtp_host'],
                'smtp_port': conf['smtp_port'],
                'smtp_auth_file': '',
                'num_events': 1,
                'alert': ['db'],
                'filter': [{'query': {'query_string': {'query': 'field6:Exception'}}}],
                'email_reply_to': '',
                'rule_file': 'example_rules/example_frequency.yaml',
                'timeframe': {'minutes': 1},
                'type': 'frequency',
                'email': ['286388651@qq.com']}

        return rule


def new_term_rule(conf, row):
    rule = {'index': '',
            'name': '',
            'realert': {'minutes': 1},
            'from_addr': conf['from_addr'],
            'smtp_host': conf['smtp_host'],
            'smtp_port': conf['smtp_port'],
            'smtp_auth_file': '',
            'num_events': 1,
            'alert': ['db'],
            'filter': [{'query': {'query_string': {'query': 'field6:Exception'}}}],
            'email_reply_to': '',
            'rule_file': 'example_rules/example_frequency.yaml',
            'timeframe': {'minutes': 1},
            'type': 'frequency',
            'email': ['286388651@qq.com']}

    return rule


def opsgenie_frequency_rule(conf, row):
    rule = {'index': '',
            'name': '',
            'realert': {'minutes': 1},
            'from_addr': conf['from_addr'],
            'smtp_host': conf['smtp_host'],
            'smtp_port': conf['smtp_port'],
            'smtp_auth_file': '',
            'num_events': 1,
            'alert': ['db'],
            'filter': [{'query': {'query_string': {'query': 'field6:Exception'}}}],
            'email_reply_to': '',
            'rule_file': 'example_rules/example_frequency.yaml',
            'timeframe': {'minutes': 1},
            'type': 'frequency',
            'email': ['286388651@qq.com']}

    return rule


def percentage_match_rule(conf, row):
    rule = {'index': '',
            'name': '',
            'realert': {'minutes': 1},
            'from_addr': conf['from_addr'],
            'smtp_host': conf['smtp_host'],
            'smtp_port': conf['smtp_port'],
            'smtp_auth_file': '',
            'num_events': 1,
            'alert': ['db'],
            'filter': [{'query': {'query_string': {'query': 'field6:Exception'}}}],
            'email_reply_to': '',
            'rule_file': 'example_rules/example_frequency.yaml',
            'timeframe': {'minutes': 1},
            'type': 'frequency',
            'email': ['286388651@qq.com']}

    return rule


def single_metric_rule(conf, row):
    rule = {'index': '',
            'name': '',
            'realert': {'minutes': 1},
            'from_addr': conf['from_addr'],
            'smtp_host': conf['smtp_host'],
            'smtp_port': conf['smtp_port'],
            'smtp_auth_file': '',
            'num_events': 1,
            'alert': ['db'],
            'filter': [{'query': {'query_string': {'query': 'field6:Exception'}}}],
            'email_reply_to': '',
            'rule_file': 'example_rules/example_frequency.yaml',
            'timeframe': {'minutes': 1},
            'type': 'frequency',
            'email': ['286388651@qq.com']}

    return rule
