# -*- coding: utf-8 -*-
import MySQLdb
class mysql_db(object):
    def __init__(self,mysql_data):
        self.mysql_connect=MySQLdb.connect(host='127.0.0.1',port=3306,user='root',passwd='root',db='spider',charset ='utf8')
        self.mysql_cur=self.mysql_connect.cursor()
        self.mysql_data=mysql_data
    def mysql_insert(self):
        if len(self.mysql_data) != 0:
            for l in self.mysql_data:
                sql = "insert into cm10086 (unit,title,content,time)values('" + l["unit"].encode("utf8") + "','" + l["title"].encode("utf8") + "','" + l["content"].encode("utf8") + "','" + l["time"].encode("utf8") + "')"
                self.mysql_cur.execute(sql)
            result=self.mysql_connect.commit()
            return result
