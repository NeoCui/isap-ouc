#-*- coding:utf-8 -*-
'''
Created on 2012-3-12
数学学院抓取内容，学院公告栏，学院动态，党团工作，毕业生就业，学生工作，读书长廊
首页可以直接抓取所有内容：http://www2.ouc.edu.cn/math/Ch/Main.asp
@author: hlq
'''
import urllib,MySQLdb,re,SrdpPage
from BeautifulSoup import BeautifulSoup
def GetByShuXue(url):
    html=urllib.urlopen(url).read();
    parser=BeautifulSoup(html);
    number=len(parser('a'))#a标签数 
    print number
    result=[]#返回值的表      
    for j in range(number):       
        title=[]       
        href=parser.findAll("a")[j]["href"] 
        if 'NewsView.asp?' in href:
            name=parser.findAll("a")[j].string
            #print name,href
            title.append(name)               
            html2=urllib.urlopen("http://www2.ouc.edu.cn/math/Ch/"+href).read()            
            ##print html2
            time=SrdpPage.ChoiceTime(str(html2))
            #print time
            title.append(time)
            article=GetInformation("http://www2.ouc.edu.cn/math/Ch/"+href)
            title.append(article)
            result.append(title)                    
    return result                                                                                                                  
def GetInformation(href):
    html=urllib.urlopen(href).read()#获取文章的内容，返回的是str类型
    parser=BeautifulSoup(html)
    p=parser.findAll('table',width='100%')
    shu=len(p)
    content=str(p[shu-1]); 
    #print shu
    return content    
