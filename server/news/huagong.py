#-*- coding:utf-8 -*-
'''
Created on 2011-11-17
化学化工学院，该院的新闻，通知和就业信息分为3个链接抓取
@author: hlq
'''
import urllib,MySQLdb,re,SrdpPage
from BeautifulSoup import BeautifulSoup
def GetByHuaGong(url):
    html=urllib.urlopen(url).read();
    parser=BeautifulSoup(html);
    number=len(parser('a',target='_blank'))#a标签数        
   # n=0#将时间循环插入到result序列中的判断标志
    #k=0#将href和title取出，如果a标签中没有href或title属性，程序将抛出KeyError异常 
    result=[]   
    
    for i in range(number):  
        example=[]             
        href=parser.findAll('a',target='_blank')[i]['href']
        if "ShowArticle.asp" in href:            
            title=parser('a',target='_blank')[i]['title']
            name=parser('a',target='_blank')[i].string
            example.append(name)
            #example.append("http://www2.ouc.edu.cn/chem/"+href)
            time=ChoiceTime(title)
            example.append(time)
            content=SrdpPage.GetHtml("http://www2.ouc.edu.cn/chem/"+href)
            article=content.findAll('p')
            example.append(article)            
        else:
            continue 
        result.append(example)
    return result                                           
#时间正则表达式，筛选符合的时间条件            
def ChoiceTime(time):
    time0=re.findall(r'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d',time)
    time1=re.findall(r'\d\d\d\d-\d-\d\d \d\d:\d\d:\d\d',time)
    time2=re.findall(r'\d\d\d\d-\d\d-\d \d\d:\d\d:\d\d',time)
    time3=re.findall(r'\d\d\d\d-\d-\d \d\d:\d\d:\d\d',time)
    time4=re.findall(r'\d\d\d\d-\d\d-\d\d \d:\d\d:\d\d',time)
    time5=re.findall(r'\d\d\d\d-\d-\d\d \d:\d\d:\d\d',time)
    time6=re.findall(r'\d\d\d\d-\d\d-\d \d:\d\d:\d\d',time)
    time7=re.findall(r'\d\d\d\d-\d-\d \d:\d\d:\d\d',time)   
    s=""
    if time0==[]:
        if time1==[]:
            if time2==[]:
                if time3==[]:
                    if time4==[]:
                        if time5==[]:
                            if time6==[]:
                                if time7==[]:
                                    s="传入时间出错，系统错误！"
                                else:
                                    s=time7[0]                
                            else:
                                s=time6[0]
                        else:
                            s=time5[0]
                    else:
                        s=time4[0]
                else:
                    s=time3[0]
            else:
                s=time2[0]
        else:
            s=time1[0]
    else:
        s=time0[0]
        
    return s            