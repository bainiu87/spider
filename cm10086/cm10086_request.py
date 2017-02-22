# -*- coding: utf-8 -*-
import requests
import re
import json
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
            self.recordLog.record_error_log(status="1",des="spider_cm10086 page request fail",page=self.page,content_url="")
            return False
        if (response.status_code == 200):
            body=response.text
            return body
        else:
            self.recordLog.record_error_log(status=6,des="status_code fail:"+str(response.status_code),page=self.page,content_url="")
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
            element_gather=[] #参数集合，后期mysql存入失败,则删除对应element
            for l in xrange(0,over_time_list_key):
                element = re.findall('\d+',content_url_element[l])[0]
                element_gather.append(element)
                redisObject=redis_db(element)
                redisResult=redisObject.redis_insert()

                print "redis status-twig:"+str(redisResult)+"--"+element+"--"+str(l+1)
                if redisResult:
                    cont = self.get_content(element)
                else:
                    cont=False
                content.append(cont)
            data=self.def_dict(unit,title,content,time,over_time_list_key,element_gather)
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
                print "time over"
                return a

    #定义dict
    def def_dict(self,unit,title,content,time,over_time_list_key,element_gather):
        data=[]
        for l in xrange(0,over_time_list_key):
            if content[l] == False:
                continue
            else:
                data_dict={"unit":unit[l],"title":title[l],"content":content[l],"time":time[l],"element":element_gather[l]}
                data.append(data_dict)
        return data

    #返回内容页
    def get_content(self,element):
        url="https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id="+element
        try:
            response=requests.get(url,verify=False)
        except:
            self.recordLog.record_error_log(status=2,des="get_content request fail",page=self.page,content_url=url)
            return False
        if (response.status_code == 200):
            body=response.text
            select=etree.HTML(body)
            #得到内容 content type：list
            raw_data=select.xpath("//table/descendant::text()")
            content = self.strainer(raw_data=raw_data,url=url)
            return content
        else:
            self.recordLog.record_error_log(status=6, des="get_content  status_code fail:"+str(response.status_code), page=self.page, content_url=url)
            return False

    #详情页过滤器，只要中标人信息
    def strainer(self,raw_data,url):
        try:
            content = "|".join(raw_data).encode("utf8")
        except:
            self.recordLog.record_error_log(status=5,des="strainer encode fail:"+json.dumps(raw_data),page=self.page,content_url=url)
            return False
        content = content.replace('\r', '')
        content = content.replace('\n', '')
        content = content.replace('\t', '')
        content = content.replace(' ', '')
        content = content.replace('：','        ')
        content = content.replace(':','        ')
        begin = content.find("中标候选人公示如下")
        begin_1 = content.find("中选候选人公示如下")
        begin_2 = content.find("成交候选人公示如下")
        print begin,begin_2,begin_1
        if begin != -1 or begin_1 != -1 or begin_2 != -1:
            if begin != -1:
                over = content.find("中标候选人公示期")
                data = content[begin + 30:over]
                return data
            if begin_1 != -1:
                over = content.find("中选候选人公示期")
                data = content[begin_1+30:over]
                return data
            if begin_2 !=-1:
                over = content.find("成交候选人公示期")
                data = content[begin_2 + 30:over]
                return data
        else:
            self.recordLog.record_error_log(status=7, des="strainer fail", page=self.page, content_url=url)
            return False
if __name__=="__main__":
    test=spider(1,"2017-2-13")
    data=test.xpath_cm10086()
    #print data[0]["unit"].encode("utf8")
    for l in data:
        #print l["unit"].encode("utf8"),l["title"].encode("utf8"),l["content"].encode("utf8"),l["time"]
        print l