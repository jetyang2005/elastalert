# coding:utf-8
''''' 

@author: baocheng 
'''
from db_sqlconn import Mysql
import config
import yaml
import json
import util_switch

def get_rules_from_db(conf, args):

    # 申请资源
    mysql = Mysql(conf)
    rules = []
    sql_rules = "select * from link_rules"
    result = mysql.getAll(sql_rules)
    if result:
        for row in result:

            # query_ruletypesdictvalue_sql = "select dict_name as rule_type from link_dict_entry " \
            #                     "where dict_type_code = 'alertRuletypes' and dict_code = %s"
            # query_ruletypesdictvalue_param = [row["rule_type"]]
            # rule_type = mysql.getOne(query_ruletypesdictvalue_sql, query_ruletypesdictvalue_param)

            # query_alertdictvalue_sql = "select dict_name as rule_type from link_dict_entry " \
            #                     "where dict_type_code = 'alertRuletypes' and dict_code = %s"
            # query_dictvalue_param = [row["rule_type"]]
            # rule_type = mysql.getOne(query_alertdictvalue_sql, query_dictvalue_param)


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
            alertpersons = mysql.getAll(query_alertperson_sql, query_alertperson_param) #数据库查询的接收者
            emails=[]
            for alertemail in alertpersons:
                emails.append(alertemail['user_email'])
                #print "数组=========",emails

            """if row['rule_type'] == 'frequency':
                rule = frequency_rule(conf, row) #frequency规则模板填充数据"""

            row['user_email']= emails
            for case in util_switch.switch(row['rule_type']):
                if case('frequency'):
                    rule = frequency_rule(conf, row)
                    config.load_options(rule, conf, '', args)
                    config.load_modules(rule, args)
                    rule['alertpersons'] = alertpersons
                    rule['rule_id'] = row['id']
                    rule['rule_type'] = row['rule_type']
                    rules.append(rule)
                    break
                if case('spike'):
                    rule = spike_rule(conf, row)
                    config.load_options(rule, conf, '', args)
                    config.load_modules(rule, args)
                    rule['alertpersons'] = alertpersons
                    rule['rule_id'] = row['id']
                    rule['rule_type'] = row['rule_type']
                    rules.append(rule)
                    break

                if case():  # 默认
                    print "switch something else!"

        """  config.load_options(rule, conf, '', args)
            config.load_modules(rule, args)
            rule['alertpersons'] = alertpersons
            rule['rule_id'] = row['id']
            rule['rule_type'] =row['rule_type']
            rules.append(rule)"""

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
            'alert': ['db','email'],
            'filter': [{'query': {'query_string': {'query': 'field6:Exception'}}}],
            'email_reply_to': '',
            'rule_file': '',
            'timeframe': {'minutes': 1},
            'type': 'frequency',
            'email': ['1391464709@qq.com']}

    #rule_filter_str = row["rule_filter"].replace("\n", "").strip()/Users/yangwm/log/elastalert/example_rules/example_frequency.yaml
    rule_extend_str = row["rule_extend"].replace("\n", "").strip()
    #rule_filter = json.loads(rule_filter_str)
    rule_extend = json.loads(rule_extend_str)
    alert_way = row['rule_alerts']
    rule['alert'] = alert_way.split(',')
    rule['alert_way'] = row['rule_alerts']
    rule['name'] = row["rule_name"]
    rule['index'] = row["rule_index"]
    rule['realert'] = rule_extend['realert']
    rule['num_events'] = rule_extend['num_events']
    rule['timeframe'] = rule_extend['timeframe']
    rule['type'] = 'frequency'
    rule['filter'] = rule_extend['filter']
    rule['email'] = row['user_email']
    print "frequency=========%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
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
            'alert': ['db','email'],
            'filter': [{'query': {'query_string': {'query': '_id:AVwGceqjqjtyRJ_Calx5'}},'type':{'value':'spike'}}],
            'email_reply_to': '',
            'rule_file': '',
            'timeframe': {'minutes':1},
            'type': 'spike',
            'spike_height': 1,
            'threshold_cur':1,
            'spike_type': 'up',
            'email': ['1391464709@qq.com']}

    rule_extend_str = row["rule_extend"].replace("\n", "").strip()
    rule_extend = json.loads(rule_extend_str)
    rule['filter'] = rule_extend['filter']
    rule['name'] = row["rule_name"]
    rule['index'] = row["rule_index"]
    alert_way = row['rule_alerts']
    rule['alert'] = alert_way.split(',')
    rule['alert_way'] = row['rule_alerts']
    rule['email']=row['user_email']
    rule['spike_height'] = rule_extend['spike_height']
    rule['threshold_cur'] = rule_extend['threshold_cur']
    rule['spike_type'] = rule_extend['spike_type']
    rule['timeframe'] = rule_extend['timeframe']


    print "spike=============%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
        row["id"], row["rule_name"], row["rule_type"], row["rule_index"], row["rule_desc"], row["rule_alerts"],
        row["rule_filter"], row["rule_extend"], row["rule_seq"])

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
