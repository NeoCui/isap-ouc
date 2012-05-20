#-*- coding:utf-8 -*-
'''
Created on 2012-3-9
最新公告，最新动态，学术交流（学术讲座）学生工作（动态和通知），就业信息
@author: hlq
'''
import urllib,MySQLdb,re
from BeautifulSoup import BeautifulSoup
#ClassID号和分类名称，url为http://www2.ouc.edu.cn/shuichan/Article_Class2.asp?ClassID=1
HrefAndTitle=[["news.asp?cId=58","最新公告"],["news.asp?cId=62","最新动态"],["news.asp?itemId=36&cId=37","学术讲座"],["student/news.asp?cid=61","学生工作：最新动态"],["student/news.asp?cid=66","学生工作：工作通知"],["student/jiuye-news.asp?cid=44","招聘信息"],["student/jiuye-news.asp?cid=43","招聘：工作通知"]]

HrefAndTitle2=[["student/jiuye-news.asp?itemid=63&cId=67","就业指导：公务员"],["student/jiuye-news.asp?itemid=63&cId=68","金融系统"],["student/jiuye-news.asp?itemid=63&cId=69","贸易物流"],["student/jiuye-news.asp?itemid=63&cId=70","外企其他"],["student/jiuye-news.asp?itemid=63&cId=71","行业经验"],["student/jiuye-news.asp?itemid=63&cId=72","就业讲座"],["student/jiuye-news.asp?itemid=63&cId=73","考研经验"]]
def GetByJingJi(url):
    html=urllib.urlopen(url).read();
    parser=BeautifulSoup(html);
    number=len(parser('a',{'class':'font1link'}))#a标签数 
    timelist=[];
    timeNumber=len(parser('td',{'class':'red'}))
    #print number,timeNumber
    for t in range(timeNumber):
        time=parser.findAll('td',{'class':'red'})[t].string
        #print time
        timelist.append(time)  
    result=[]#返回值的表  
  
    TitleAndHref=[]
    for j in range(number):              
        title=[]
        href=parser.findAll("a",{'class':'font1link'})[j]["href"]        
        if '-ny.asp?' in href:
            title.append("http://www2.ouc.edu.cn/jingji/"+href);
            name=parser.findAll("a",{'class':'font1link'})[j]["title"]
            title.append(name)  
            TitleAndHref.append(title)
            #print href          #标题  

    for i in range(len(TitleAndHref)):
        example=[]
        example.append(TitleAndHref[i][1])
        content=GetInformation(TitleAndHref[i][0])
        example.append(timelist[i])
        example.append(content)
        result.append(example)        
    return result  
def GetByJingJiStudent(url):
    html=urllib.urlopen(url).read();
    parser=BeautifulSoup(html);
    number=len(parser('a',{'class':'font1link'}))#a标签数 
    timelist=[];
    timeNumber=len(parser('td',{'class':'red'}))
    #print number,timeNumber
    for t in range(timeNumber):
        time=parser.findAll('td',{'class':'red'})[t].string
        #print time
        timelist.append(time)  
    result=[]#返回值的表  
  
    TitleAndHref=[]
    for j in range(number):              
        title=[]
        href=parser.findAll("a",{'class':'font1link'})[j]["href"]        
        if '-ny.asp?' in href:
            title.append("http://www2.ouc.edu.cn/jingji/student/"+href);
            name=parser.findAll("a",{'class':'font1link'})[j]["title"]
            title.append(name)  
            TitleAndHref.append(title)
            #print href          #标题  

    for i in range(len(TitleAndHref)):
        example=[]
        example.append(TitleAndHref[i][1])
        content=GetInformation(TitleAndHref[i][0])
        example.append(timelist[i])
        example.append(content)
        result.append(example)        
    return result                                                                                                                                     
def GetInformation(href):
    html=urllib.urlopen(href).read()#获取文章的内容，返回的是str类型
    parser=BeautifulSoup(html)
    p=parser.findAll('td',align='left')
    content="";
    pa=re.compile(r'\<td align="left"\>.')
    shu=len(p)
    for i in range(shu):
        match=pa.match(str(p[i]))
        if match:
            content=content+str(p[i])
    return content    
