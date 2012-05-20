# -*- coding: UTF-8 -*-
#对教务处的操作
import os,urllib2,cookielib,urllib,re
import BeautifulSoup

#教务处网站
loginurl="http://jwc.ouc.edu.cn:8080/ouc/index.do"
logouturl="http://jwc.ouc.edu.cn:8080/ouc/logout.do"
chengji="http://jwc.ouc.edu.cn:8080/ouc/SS018.do"

class Connectjwc():
#    def __init__(self):
#        self.session=''
##        self.num=''
##        self.pwd=''
##        self.name=''
##        self.
    def tryconnect(self,num,pwd,term):
        #此处未添加处理异常模块
        r=urllib2.Request(loginurl)
        h=urllib2.urlopen(r)
        html=h.read()
        
        #获取cookie
        cookie=h.info().getheader('Set-Cookie')
        cookie=cookie[:cookie.find(';')]
        
        #获取验证码
        htmlall=BeautifulSoup.BeautifulSoup(html)
        kaptchafield=htmlall.findAll('input',attrs={'name':'kaptchafield'})[0].parent.contents[3].attrs[3][1]
        
        post=urllib.urlencode({'subSystemName':'ouc.student','actionType':'Login','userId':num,
                'password':pwd,'kaptchafield':kaptchafield,
                'term':term,'submit.x':'0','submit.y':'0'})
        headers={'Connection':'keep-alive',
                     'Referer':'http://jwc.ouc.edu.cn:8080/ouc/index.do',
                        'Keep-Alive':'115',
                        'Content-Type':'application/x-www-form-urlencoded'}

        req=urllib2.Request(loginurl,post)
        req.add_header('Cookie',cookie)
        res=urllib2.urlopen(req).read()
            
        if(res.find("登陆失败，请检查用户名、密码、验证码是否正确。")!=-1):    
            #登录失败
            return 1
        
        elif res.find("该用户已经登录，请登出或稍后再试!")!=-1:
            #该用户已经登录
            return 2
        else :
            self.contents=res.decode('GBK').encode('UTF-8')
            #soup=BeautifulSoup.BeautifulSoup(contents)
            #response=str(soup.findAll('table')[0])
            #登录成功
            self.session=cookie
            self.logout()
            self.num=num
            self.pwd=pwd   
            #抓取信息
            return 0
        
    #获取姓名、专业等
    def getUserInfo(self):
#抓姓名、专业、年级
        a=self.contents[self.contents.find("姓名："):self.contents.find("20111学期开课计划")]
        self.name=a[a.find("姓名：")+9:a.find(" ")]
        self.major=a[a.find("专业：")+9:a.find("&nbsp")]
        self.grade=self.num[5:9]
        
    #注销
    def logout(self):
        r=urllib2.Request(logouturl)
        cookie=self.session
        r.add_header('Cookie',cookie)
        p=urllib2.urlopen(r)
        
    