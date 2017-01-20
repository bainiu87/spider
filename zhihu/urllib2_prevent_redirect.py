# -*- coding: utf-8 -*-
import urllib2
import cookielib
'''
urllib2 会自动处理重定向
禁止urllib2 自动重定向处理
cookie_name为我们创建的cookie文件名称
class RedirctHandler() 这个类为urllib2中内置的类，我们这里重写该类，并对301 302 不进行任何处理
hasattr(object,name) 判断object中是否含有name属性

'''
def state_code(url=None,cookie_name=None,header=None):
    class RedirctHandler(urllib2.HTTPRedirectHandler):
        """docstring for RedirctHandler"""

        def http_error_301(self, req, fp, code, msg, headers):
            pass

        def http_error_302(self, req, fp, code, msg, headers):
            pass
    cookie = cookielib.LWPCookieJar()
    cookie.load("cookie", ignore_discard=True, ignore_expires=True)
    request = urllib2.Request(url, headers=header)
    cookie_handler = urllib2.HTTPCookieProcessor(cookie)
    debug_handler = urllib2.HTTPHandler(debuglevel=1)
    opener = urllib2.build_opener(debug_handler, RedirctHandler, cookie_handler)
    response=None
    code=None
    try:
        response = opener.open(request)
        code=response.code
    except urllib2.URLError as e:
        if hasattr(e, 'code'):
            #状态码
            error_info = e.code
        elif hasattr(e, 'reason'):
            error_info = e.reason
    finally:
        if response:
            response.close()
    if code:
        return code
    else:
        return error_info

