# -*- coding: utf-8 -*-
import cm10086_request
import threading
from Mysql_DB import mysql_db
class Client(object):
    def __init__(self,begin_page,over_page):
        self.over_page=over_page  #结束页数
        self.begin_page=begin_page #开始页数
        self.numb=-1
        #将页数添加到list中，可以使用定时器，每2秒提取一个
        self.page_list=[]
        for l in xrange(self.begin_page,self.over_page+1):
            self.page_list.append(l)

    #内含定时器
    def call_function(self):
        self.numb+=1
        try:
            page=self.page_list[self.numb]
        except:
            print "game over"
            return
        data=self.get_data(page)
        if data != False:
            into_mysql=mysql_db(data,page)
            into_mysql.mysql_insert()
        else:
            print "page request fail"
        t = threading.Timer(1,self.call_function)
        t.start()
        t.join()

    #实例化spider类
    def get_data(self,page):
        cm10086=cm10086_request.spider(page,"2015-1-1")
        data=cm10086.xpath_cm10086()
        return data

if __name__=="__main__":
    client=Client(1,30)
    client.call_function()