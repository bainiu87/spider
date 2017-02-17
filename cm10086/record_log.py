# -*- coding: utf-8 -*-
import json
class record_log(object):
    # 错误日志函数,状态码：status ,错误描述：des,页数：page , 如果是详情页则记录详情页的地址content_url
    # 状态码：页面请求错误:1，详细页请求错误:2,数据库错误：3，redis 错误：4
    def record_error_log(self, status="", des="", page="", content_url=""):
        error_dict = {"status": status, "des": des, "page": page, "content_url": content_url}
        error_json = json.dumps(error_dict)
        with open("error_log.txt", "a") as l:
            l.write(error_json + "\n")

