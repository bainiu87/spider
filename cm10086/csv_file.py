# -*- coding: utf-8 -*-
import csv
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def strainering(conten):
    content = conten.replace('\r', '')
    content = content.replace('\n', '')
    content = content.replace('\t', '')
    content = content.replace(' ', '')
    print content
    content = content.replace('：', '        ')
    content = content.replace(':', '        ')
    begin = content.find("中标候选人公示如下")
    begin_1 = content.find("中选候选人公示如下")
    begin_2 = content.find("成交候选人公示如下")
    if begin != -1 or begin_1 != -1 or begin_2 != -1:
        if begin != -1:
            over = content.find("中标候选人公示期")
            data = content[begin + 30:over]
            return data
        if begin_1 != -1:
            over = content.find("中选候选人公示期")
            data = content[begin_1 + 30:over]
            return data
        if begin_2 != -1:
            over = content.find("成交候选人公示期")
            data = content[begin_2 + 30:over]
            return data
    else:
        return False

mysql_connect = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='spider',charset='utf8')
cur=mysql_connect.cursor()
sql="select * from cm10086"
csv_object=file("data.csv","a")
cur.execute(sql)
a=0
while True:

    data=cur.fetchone()
    content=data[3]
    if content:
        get_content=strainering(content)
        if get_content != False:
            a+=1
            content_list=[data[0],data[1],data[2],get_content,data[4]]
            writer = csv.writer(csv_object)
            writer.writerow(content_list)
            print a
csv_object.close()

