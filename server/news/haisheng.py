#-*- coding:utf-8 -*-
'''
Created on 2011-11-17
海洋生命学院 新闻通知，就业信息
@author: hlq
'''
import urllib,MySQLdb,re,SrdpPage
from BeautifulSoup import BeautifulSoup
def GetByHaiSheng(url):#通知和就业信息是相同的html风格
    html=urllib.urlopen(url).read();
    html=html.decode("gb2312","ignore")
    parser=BeautifulSoup(html);
    number=len(parser('a',target='_self'))#a标签数        
    result=[]    
    for i in range(number): 
        example=[]               
        href=parser.findAll('a',target='_self')[i]['href']
        if "article.asp" in href:
            name=parser('a',target='_self')[i].string
            example.append(name)
            #print name
            hrefall="http://www2.ouc.edu.cn/hysm/"+href
            time0=parser('a',target="_self")[i]["title"]    
            time=SrdpPage.ChoiceTime(time0) 
            #print time     
            example.append(time)
            content=SrdpPage.GetHtml(hrefall)
            article=content.findAll('table',width='95%')
            example.append(article[0])  
            result.append(example)  
        else:
            continue
        
    return result                                            