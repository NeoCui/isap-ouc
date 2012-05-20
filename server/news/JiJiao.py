#-*- coding:utf-8 -*-
'''
Created on 2012-3-13
基础教学中心抓取内容，重要通知，公告栏，就业信息，学生工作
@author: hlq
'''
import urllib,MySQLdb,re
from BeautifulSoup import BeautifulSoup
#ClassID号和分类名称，url为http://www2.ouc.edu.cn/shuichan/Article_Class2.asp?ClassID=1
HrefAndTitle=[["通知新闻","more1.htm"],["公告栏","more2.htm"],["学生工作","more7.htm"],["就业信息","more8.htm"]]
def GetByJiJiao(url):
    html=urllib.urlopen(url).read();
    parser=BeautifulSoup(html);
    number=len(parser('a',target='_blank'))#a标签数 
    result=[]#返回值的表  
    for j in range(number): 
        title=[]             
        href=parser.findAll("a",target='_blank')[j]["href"] 
        name=parser.findAll("a",target='_blank')[j].string
        time=parser.findAll('td',width='100')[j].string
        #print name,href,time
        title.append(name)                
        title.append(time)
        title.append(GetInformation("http://222.195.158.131/jcjxzx/"+href))        
        result.append(title)                         
    return result                                                                                                                  
def GetInformation(href):
    html=urllib.urlopen(href).read()#获取文章的内容，返回的是str类型
    parser=BeautifulSoup(html)
    p=parser.findAll('td',height='300')
    shu=len(p)
    #print shu
    content=str(p[shu-1]);    
    return content    
