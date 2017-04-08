# coding:utf-8
''''' 

@author: baocheng 
'''
from MySqlConn import Mysql


# 申请资源
mysql = Mysql()

sqlAll = "select id,user_name from link_user;"
result = mysql.getAll(sqlAll)
if result:
    print "get all"
    for row in result:
        print "%s\t%s" % (row["id"], row["user_name"])

# 释放资源
mysql.dispose()