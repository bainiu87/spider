# -*- coding: utf-8 -*-
import MySQLdb
from record_log import record_log
class mysql_db(object):
    mysql_connect = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='spider',
                                         charset='utf8')
    def __init__(self,mysql_data,page):
        self.mysql_cur=self.mysql_connect.cursor()
        self.mysql_data=mysql_data
        self.recordLog=record_log()
        self.page=page
    def mysql_insert(self):
        if len(self.mysql_data) != 0:
            for l in self.mysql_data:
                sql = "insert into cm10086 (unit,title,content,time)values('" + l["unit"].encode("utf8") + "','" + l["title"].encode("utf8") + "','" + l["content"].encode("utf8") + "','" + l["time"].encode("utf8") + "')"
                try:
                    self.mysql_cur.execute(sql)
                except:
                    self.recordLog.record_error_log(status=3.1, des=sql, page=self.page, content_url="")
                    continue
            try:
                result=self.mysql_connect.commit()
                return result
            except:
                self.recordLog.record_error_log(status=3,des="connect.commit错误",page=self.page,content_url="")
                return False
            finally:
                self.mysql_cur.close()
