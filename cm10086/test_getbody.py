# -*- coding: utf-8 -*-
#测试用
import requests
from lxml import etree
import re
data={"page.perPageSize":'20',"noticeBean.sourceCH":"",
      "noticeBean.source":"","noticeBean.title":"","noticeBean.startDate":"","noticeBean.endDate":"",'page.currentPage':'2500'}
header={
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Content-Length':'138',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'b2b.10086.cn',
    #'Referer':'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'X-Requested-With':'XMLHttpRequest'
}
url="https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=7"
result=requests.post(url,data=data,headers=header,verify=False,allow_redirects=False)
body =  result.text
print body
# select= etree.HTML(body)
#
# unit=select.xpath("//table/tr/td[1]/text()")
# del(unit[0])
#
#
# title=select.xpath("//table/tr/td[3]/a/text()")
#
#
# content_url=select.xpath("//table/tr/@onclick")
# element=re.findall('\d+',content_url[0])
#
#
# time=select.xpath("//table/tr/td[4]/text()")
# del(time[0])
#
# print unit[0]
