#-*- coding:utf-8 -*-
'''
Created on 2012-3-5
医药学院信息抓取，信息包括学院新闻、工作通知、党团工作（工作通知，最新动态、就业信息）、学院工作、本科教育
研究生教育、科学研究、学术交流、学生工作等
@author: hlq
'''
import urllib,MySQLdb,re
from BeautifulSoup import BeautifulSoup
HrefAndTitle=[["more3.htm","学院要闻"],["more4.htm","学院通知"],["more5.htm","党团工作"],["more6.htm","学院工作"],["more7.htm","本科生教育"],["more8.htm","研究生教育"],["more9.htm","科学研究"],["more10.htm","学术交流"],["more11.htm","学生工作"]]
HrefAndTitle2=[["more2.htm","工作通知"],["more3.htm","最新动态"],["more4.htm","就业信息"]]
HrefAndTitle3=[["more18.htm","工作通知"],["more19.htm","最新动态"],["more20.htm","就业信息"]]
def GetByYiYao(url):
    html=urllib.urlopen(url).read();
    parser=BeautifulSoup(html);
    number=len(parser('a'))#a标签数 
    timelist=[];
    timeNumber=len(parser('td',width='100'))
    #print number,timeNumber
    for t in range(timeNumber):
        time=parser.findAll('td',width="100")[t].string
        ##print time
        timelist.append(time)  
#    for y in range(len(timelist)):
#        print str(timelist[y])     
    result=[]#返回值的表  
    i=1
    title=[]
    p=re.compile(r'\d+\.htm')
    for j in range(number):      
        title0=[]  
        if i<=number-2:
            i=i+1;
            href=parser.findAll("a")[i]["href"] 
            name=parser('a')[i].string
            more=str(href)[0:4]
            if 'more' ==more:
                continue
            else:
                match=p.match(href)
                if match:
                    
                    title0.append("http://222.195.158.131/yiyao/"+href)
                else:
                    title0.append(href)
                title0.append(name)
                title.append(title0)
                #print href,name
                #print href
    #print len(timelist),len(title)
    for k in range(len(timelist)):
        list=[];
        #print title[k][1],title[k][0]
        list.append(title[k][1])
        list.append(timelist[k])      
        content=GetInformation(title[k][0])
        list.append(content)
#        print str(timelist[k])
#        print str(title[k])
#        print str(content)
        result.append(list)   
    return result                                    
def GetByYiYaoDangTuan(url):
    html=urllib.urlopen(url).read();
    parser=BeautifulSoup(html);
    number=len(parser('a'))#a标签数 
    timelist=[];
    timeNumber=len(parser('td',width='100'))
    print number,timeNumber
    for t in range(timeNumber):
        time=parser.findAll('td',width="100")[t].string
        #print time
        timelist.append(time)  
#    for y in range(len(timelist)):
#        print str(timelist[y])     
    result=[]#返回值的表  
    i=0
    title=[]
    p=re.compile(r'\d+\.htm')
    for j in range(number):  
        title0=[]      
        if i<number-1:
            i=i+1;
            href=parser.findAll("a")[i]["href"] 
            name=parser('a')[i].string
            more=str(href)[0:4]
            if 'more' ==more:
                continue
            else:
                match=p.match(href)
                if match:                  
                    title0.append("http://222.195.158.131/yiyaodtgz/"+href)
                else:
                    title0.append(href)
                title0.append(name)
                title.append(title0)
                #print href
    #print len(timelist),len(title)
    for k in range(len(timelist)):
        list=[];
        list.append(title[k][1])
        list.append(timelist[k])        
        content=GetInformation(title[k][0])
        list.append(content)
#        print str(timelist[k])
#        print str(title[k])
#        print str(content)
        result.append(list)        
    return result        
def GetByYiYaoXingZheng(url):
    html=urllib.urlopen(url).read();
    parser=BeautifulSoup(html);
    number=len(parser('a'))#a标签数 
    timelist=[];
    timeNumber=len(parser('td',width='100'))
    print number,timeNumber
    for t in range(timeNumber):
        time=parser.findAll('td',width="100")[t].string
        #print time
        timelist.append(time)  
#    for y in range(len(timelist)):
#        print str(timelist[y])     
    result=[]#返回值的表  
    i=0
    title=[]
    p=re.compile(r'\d+\.htm')
    for j in range(number):     
        title0=[]   
        if i<number-1:
            i=i+1;
            href=parser.findAll("a")[i]["href"] 
            name=parser('a')[i].string
            more=str(href)[0:4]
            if 'more' ==more:
                continue
            else:
                match=p.match(href)
                if match:                  
                    title0.append("http://222.195.158.131/xydw/"+href)
                else:
                    title0.append(href)
                title0.append(name)
                title.append(title0)
                #print href
    #print len(timelist),len(title)
    for k in range(len(timelist)):
        list=[];
        print title[k][1],title[k][0]
        list.append(title[k][1])
        list.append(timelist[k])
        content=GetInformation(title[k][0])
        list.append(content)
        result.append(list)
#    for m in range(len(result)):
#        print str(result[m][0]),str(result[m][1])         
    return result                
def GetInformation(href):
    html=urllib.urlopen(href).read()#获取文章的内容，返回的是str类型
    parser=BeautifulSoup(html)
    p=parser.findAll('p')
    shu=len(p)
    content=""
    for i in range(shu):
        content=content+str(p[i])
    return content    
