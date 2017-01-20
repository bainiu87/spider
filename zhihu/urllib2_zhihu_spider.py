# -*- coding: utf-8 -*-
import urllib2
import urllib
import time
import cookielib
import re
from urllib2_prevent_redirect import state_code
from PIL import Image
from lxml import etree

"""
urllib2 发送请求会自动处理重定向，同时携带cookie数据会在第二次跳转的时候丢失
"""
class Logzhihu(object):
    def __init__(self,user=None,password=None):
        self.user=user
        self.password=password
        self.cookie_name="cookie"
        self.header={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            #'Accept-Encoding':'gzip, deflate, sdch, br',  没有报错，但是获取到的html为乱码 主要问题出在gzip上
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'no-cache',
            'Connection':'keep-alive',
            'Pragma':'no-cache',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
                }
        print "设置cookie保存文件，自定义请求头"


    #获取xsrf 码
    def __getXsrf(self):
        url="http://www.zhihu.com"
        request=urllib2.Request(url, headers=self.header)
        response=None
        try:
            response=urllib2.urlopen(request)
        except:
            print "请求失败，未能获取xsrf码"
            return "0"
        if response:
            html=response.read()
            select=etree.HTML(html)
            xsrf=select.xpath("//form[@class='zu-side-login-box']/input[@name='_xsrf']/@value")[0]
            if xsrf != '':
                print "得到xsrf码："+str(xsrf)
                return xsrf
            else:
                print "获取xsrf码失败"

    #获取验证码图片
    def __getCapt(self):
        t = str(int(float(time.time()) * 1000))
        capt_url = "https://www.zhihu.com/captcha.gif?r="+t+"&type=login"
        image = urllib.urlretrieve(capt_url, './cap.jpg')
        try:
            im = Image.open("cap.jpg")
            im.show()
            im.close
        except:
            print("请到当前目录寻找cap.jpg图片，打开后填写验证码")
        capt_num = raw_input("填写验证码：")
        return capt_num

    #登录
    def log(self):
        if self.__isLog():
            print "该cookie有效，可以使用，需要爬取页面请调用 getSelfUrl方法，该方法返回页面源码"
            return True
        else :
            if re.match(r"^1\d{10}$", self.user):
                print("手机号登录")
                url = 'https://www.zhihu.com/login/phone_num'
                formdata = {
                    '_xsrf': self.__getXsrf(),
                    'password': self.password,
                    'remember_me': 'true',
                    'phone_num': self.user,
                }

            else:
                if "@" in self.user:
                    print "邮箱登录"
                else:
                    print "邮箱不合法"
                    return False
                url = 'https://www.zhihu.com/login/email'
                formdata = {
                    '_xsrf': self.__getXsrf(),
                    'password': self.password,
                    'remember_me': 'true',
                    'email': self.user,
                }

            try:
                #需要验证码
                formdata['captcha'] = self.__getCapt()
                data = urllib.urlencode(formdata)# 初始化数据，服务器易于识别的编码
                cookie = cookielib.LWPCookieJar(self.cookie_name)
                handler = urllib2.HTTPCookieProcessor(cookie)
                opener = urllib2.build_opener(handler)
                request = urllib2.Request(url, headers=self.header)
                response = opener.open(request, data=data)
                cookie.save(ignore_discard=True, ignore_expires=True)
                state=self.__isLog()
                if state:
                    print "登录成功，需要爬取页面请调用 getSelfUrl方法，该方法返回页面源码"
                    return True
                else:
                    print "登录失败，请重新登录"
                    return False
            except:
                print "登录失败，异常问题，请查看源码解决"
                return False

    #判断是否登录
    def __isLog(self):
        code=state_code("https://www.zhihu.com/settings/profile", self.cookie_name, self.header)
        if code == 200:
            return True
        else:
            return False

    #获取登录以后的页面信息
    def getSelfUrl(self,url=None):
        request=urllib2.Request(url,headers=self.header)
        cookie=cookielib.LWPCookieJar()
        cookie.load(self.cookie_name,ignore_discard=True,ignore_expires=True)
        hand=urllib2.HTTPCookieProcessor(cookie)
        opener=urllib2.build_opener(hand)
        response=opener.open(request)
        return response


if __name__ == '__main__':
    user = raw_input("请输入用户名：")
    password = raw_input("请输入密码：")
    state=Logzhihu(user,password)
    result=state.log()
    if result:
        html=state.getSelfUrl(url="https://www.zhihu.com/settings/profile")
    print html.read()