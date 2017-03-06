# -*- coding: utf-8 -*-
#向队列发送页数
import stomp
class send_activeMQ(object):
    def __init__(self):
        self.MQ_conn=stomp.Connection10([('127.0.0.1',61613)])
    def send_message(self,begin_page,over_page):
        self.MQ_conn.start()
        self.MQ_conn.connect()
        for i in xrange(begin_page,over_page+1):
            self.MQ_conn.send(body=str(i),destination='/queue/foo')
    def __del__(self):
        self.MQ_conn.disconnect()
if __name__=="__main__":
    sendObject=send_activeMQ()
    sendObject.send_message(1,2500)