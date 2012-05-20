#-*- coding:utf-8 -*-
'''
Created on 2012-3-13
艺术系抓取内容，最新公告，系内动态，学术交流，学生工作，艺术资讯
@author: hlq
'''
import urllib,MySQLdb,re
from BeautifulSoup import BeautifulSoup
def GetByYiShu(url):
    html=urllib.urlopen(url).read();
    if "gb2312" in html:
        html=html.decode("gb2312","ignore");
    elif "GB2312" in html:
        html=html.decode("GB2312","ignore"); 
    parser=BeautifulSoup(html);
    number=len(parser('a',target='_blank'))#a标签数 
    result=[]#返回值的表  
    hrefall="";
    
    for j in range(number):          
        title=[]    
        href=parser.findAll("a",target='_blank')[j]["href"] 
        name=parser.findAll("a",target='_blank')[j].string
        time=parser.findAll('td',width='100')[j].string
        #print name,href,time
        if 'http' in href:
            hrefall=href;
            article=GetInformation2(hrefall)
        else:
            hrefall="http://222.195.158.131/wanb/"+href
            article=GetInformation(hrefall)
        title.append(name)      
        title.append(time)          
        title.append(article)
       
        result.append(title)                       
    return result                                                                                                                  
def GetInformation(href):
    html=urllib.urlopen(href).read()#获取文章的内容，返回的是str类型
    if "gb2312" in html:
        html=html.decode("gb2312","ignore");
    elif "GB2312" in html:
        html=html.decode("GB2312","ignore"); 
    parser=BeautifulSoup(html)
    p=parser.findAll('td',height='569')
    shu=len(p)
    #print shu
    content=str(p[0]);
    return content    
def GetInformation2(href):
    html=urllib.urlopen(href).read()#获取文章的内容，返回的是str类型
    if "gb2312" in html:
        html=html.decode("gb2312","ignore");
    elif "GB2312" in html:
        html=html.decode("GB2312","ignore"); 
    parser=BeautifulSoup(html)
    p=parser.findAll('p')
    shu=len(p)
    content="";
    for i in range(shu):
        content=content+str(p[i])
    #print shu
    return content  