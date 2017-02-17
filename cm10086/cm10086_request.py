# -*- coding: utf-8 -*-
import requests
import re
from record_log import record_log
from lxml import etree
from Redis_DB import redis_db
class spider(object):
    def __init__(self,page,over_time=0):
        self.over_time=over_time #设置截止时间
        self.page=page #设置页数
        self.data={'page.currentPage':'%d'%self.page,'page.perPageSize':'20','noticeBean.sourceCH':'',
                   'noticeBean.source':'','noticeBean.title':'','noticeBean.startDate':'','noticeBean.endDate':''}
        self.header={
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Content-Length':'138',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'b2b.10086.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'X-Requested-With':'XMLHttpRequest'
        }
        self.recordLog=record_log() #实例日志类

    #入口
    def spider_cm10086(self):
        print "now_page:"+str(self.page)
        url = "https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=7"
        try:
            response=requests.post(url,data=self.data,headers=self.header,verify=False,allow_redirects=False,timeout=60)
        except:
            self.recordLog.record_error_log(status="1",des="请求页错误：",page=self.page,content_url="")
            self.request_status=False
            return False
        if (response.status_code == 200):
            body=response.text
            return body
        else:
            self.recordLog.record_error_log(status=response.status_code,des="解析错误",page=self.page,content_url="")
            return False

    #选择内容，内容字典
    def xpath_cm10086(self):
        html=self.spider_cm10086()
        if html != False:
            select=etree.HTML(html)
            unit = select.xpath("//table/tr/td[1]/text()") #采购需求单位 del删除标题栏
            del(unit[0])
            title = select.xpath("//table/tr/td[3]/a/text()") #标题 不需要del()  因为标题栏中没有a标签
            time = select.xpath("//table/tr/td[4]/text()")
            del(time[0]) #发布时间 del删除标题栏
            over_time_list_key=self.beyond_time(time)  #该变量表示超出时间的那一页中爬取的时间list 对应的key位置

            # 链接参数 element为list  list[0] type: str
            content_url_element = select.xpath("//table/tr/@onclick")
            content=[]
            for l in xrange(0,over_time_list_key):
                element = re.findall('\d+',content_url_element[l])[0]
                redisObject=redis_db(element)
                redisResult=redisObject.redis_insert()
                print "redis status:"+str(redisResult)
                if redisResult:
                    cont = self.get_content(element)
                else:
                    cont="-10"
                content.append(cont)
            data=self.def_dict(unit,title,content,time,over_time_list_key)
            return data
        else:
            return False

    #时间判断
    def beyond_time(self,nowtime):
        now_time = nowtime
        if self.over_time == 0:
            return len(now_time)
        else:
            for l in xrange(0,len(now_time)):
                if now_time[l].encode("utf8") >= self.over_time:
                    a=-1
                else:
                    a=l
                    break
            if a==-1:
                return len(now_time)
            else:
                return a

    #定义dict
    def def_dict(self,unit,title,content,time,over_time_list_key):
        data=[]
        for l in xrange(0,over_time_list_key):
            if content[l] == "-10" or content[l] == False:
                continue
            else:
                data_dict={"unit":unit[l],"title":title[l],"content":content[l],"time":time[l]}
                data.append(data_dict)
        return data

    #返回内容页
    def get_content(self,element):
        url="https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id="+element
        try:
            response=requests.get(url,verify=False)
        except:
            self.recordLog.record_error_log(status=2,des="详情页请求错误",page=self.page,content_url=url)
            return False
        if (response.status_code == 200):
            body=response.text
            select=etree.HTML(body)
            #得到内容 content type：list
            content = "".join(select.xpath("//table/descendant::text()"))
            return content
        else:
            self.recordLog.record_error_log(status=response.status_code, des="解析错误", page=self.page, content_url=url)
            return False


if __name__=="__main__":
    test=spider(6,"2017-2-13")
    data=test.xpath_cm10086()
    #print data[0]["unit"].encode("utf8")
    for l in data:
        print l["unit"].encode("utf8"),l["title"].encode("utf8"),l["content"].encode("utf8"),l["time"]
    print len(data)