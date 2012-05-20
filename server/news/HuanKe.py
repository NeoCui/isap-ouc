#-*- coding:utf-8 -*-
'''
Created on 2012-3-9
医药学院信息抓取，信息包括学院新闻、教学工作、就业信息、学生风采、规章制度

@author: hlq
'''
import urllib,re,SrdpPage
from BeautifulSoup import BeautifulSoup

HrefAndTitle=[["more1.htm","学院要闻"],["more2.htm","就业信息"],["more4.htm","教学工作"],["more5.htm","学生风采"],["more6.htm","规章制度"]]
def GetByHuanKe(url):
    html=urllib.urlopen(url).read();
    if "gb2312" in html:
        html=html.decode("gb2312","ignore");
    elif "GB2312" in html:
        html=html.decode("GB2312","ignore"); 
    parser=BeautifulSoup(html);
    number=len(parser('a',target='_blank'))#a标签数 
    timeNumber=len(parser('td',width='100'))
    #print number,timeNumber
    result=[]#返回值的表       
    for i in range(number):    
        example=[]    
        title=parser.findAll("a",target='_blank')[i].string
        time=parser.findAll('td',width='100')[i].string 
        href=parser.findAll("a",target='_blank')[i]['href'] 
        #print len(href)          
        more=re.findall(r'\d+\.htm',href);
        #print more
        if 'http' in href:   
            content=SrdpPage.GetHtml(href)
            article=content.findAll('p')            
                
        else:
            article=GetInformation("http://222.195.158.131/huanjing/"+str(href))
        #print str(href)       
        example.append(title)
        example.append(time)          
        example.append(article)
        result.append(example)
    return result                                    
def GetInformation(href):
    html=urllib.urlopen(href).read()#获取文章的内容，返回的是str类型
    parser=BeautifulSoup(html)
    p=parser.findAll('td',{"class":"text12h"})
    #print len(p)
    #print str(p[3])
    content="<table><tr>"+str(p[3])+"</tr></table>"
    return content    
