#-*- coding:utf-8 -*-
'''
Created on 2012-3-11
文新学院抓取的内容：学院通知，工作通知，学生工作（学生新闻），国际交流（新闻动态、教育交流、孔子学校院）
名家系列（最新动态、名家风采），就业信息（就业指导、通知公告）
@author: hlq
'''
import urllib,MySQLdb,re
from BeautifulSoup import BeautifulSoup
HrefAndTitle=[["CollegeNews.aspx?news=1","学院新闻"],["CollegeNews.aspx","工作通知"],["artcollege/ArticleList.aspx?ArticleClass=51","学生工作：通知公告"],["student/news.asp?cid=61","学生工作：最新动态"]]

def GetByWenXin(url):
    html=urllib.urlopen(url).read();
    parser=BeautifulSoup(html);
    number=len(parser('a',target='_blank'))#a标签数 
    timelist=[];
    timeNumber=len(parser('td'))
    #print number,timeNumber
    for t in range(timeNumber):
        time=parser.findAll('td')[t].string
        ##print str(time)
        #print time
        if time==None:
            continue
        else:
            choice=GetTime(time)
            if choice=="":
                continue
            else:                
                timelist.append(choice)  
#    for y in range(len(timelist)):
#        print str(timelist[y])     
    #print len(timelist)
    result=[]#返回值的表  
    
    for j in range(number-2):    
        title=[]          
        href=parser.findAll("a",target='_blank')[j]["href"] 
        name=parser.findAll("a",target='_blank')[j].string
        title.append(name)                       
        title.append(timelist[j])
        if "http" in href:           
            article=GetInformation2(href);
        else:
            article=GetInformation("http://www3.ouc.edu.cn/artcollege/"+href);
            
        title.append(article)
        #print name,href,str(timelist[j]),article
        result.append(title)
        
                #print href   
    return result         
def GetTime(time):
    p=re.compile(r'\d\d\d\d-\d\d-\d\d')#时间匹配条件
    p1=re.compile(r'\d\d\d\d-\d-\d\d')
    p2=re.compile(r'\d\d\d\d-\d\d-\d')
    p3=re.compile(r'\d\d\d\d-\d-\d')
    match0=p.match(time)
    match1=p1.match(time)
    match2=p2.match(time)
    match3=p3.match(time)
    s=""
    if match0:#如果匹配，则返回该条
        s=match0.group()
    elif match1:
        s=match1.group()
    elif match2:
        s=match2.group()
    elif match3:
        s=match3.group()
    else:
        s=""
    return s 
        
                                                                                                            
def GetInformation(href):
    html=urllib.urlopen(href).read()#获取文章的内容，返回的是str类型
    parser=BeautifulSoup(html) 
    p=parser.findAll('td' ,id='fontzoom')  
    #print len(p)
    content='<table><tr>'+str(p[0])+'</tr></table>'
    return content
def GetInformation2(href):
    html=urllib.urlopen(href).read()#获取文章的内容，返回的是str类型
    parser=BeautifulSoup(html) 
    p=parser.findAll('p') 
    #print len(p)
    content="";
    for i in range(len(p)-2):
        content=content+str(p[i]);
    return content
