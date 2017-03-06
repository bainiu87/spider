# -*- coding: utf-8 -*-
#测试用
import requests
from lxml import etree
result=requests.get("https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=332122",verify=False)
html=result.text
select=etree.HTML(html)
#content=select.xpath("//table/tr[2]/td/h1/text()")[0]
content="".join(select.xpath("//table/descendant::text()")).encode("utf8")
a="中选候选人公示如下"
b=content.find(a)
print content[b+30:]

