# -*- coding: utf-8 -*-
#使用队列，接受队列消息
import stomp
import cm10086_request
from record_log import record_log
from Mysql_DB import mysql_db
import time

class SampleListener(object):
    def on_error(self, headers, message):
        recordLog = record_log()
        recordLog.record_error_log(status=8, des=message, page="00", content_url="00")
        print "activeMQ getMessage fail"
    def on_message(self, headers, message):
            page = int(message)
            data = self.get_data(page)
            if data != False:
                into_mysql = mysql_db(data, page)
                into_mysql.mysql_insert()
            else:
                print "page request fail"

    def get_data(self, page):
        cm10086 = cm10086_request.spider(page, "2015-1-1")
        data = cm10086.xpath_cm10086()
        return data



MQ_conn = stomp.Connection10([("127.0.0.1", 61613)])
MQ_conn.set_listener('', SampleListener())
MQ_conn.start()
MQ_conn.connect()
MQ_conn.subscribe(destination='/queue/foo', id=1, ack='auto')
while True:
    try:
        time.sleep(1)
    except:
        break




