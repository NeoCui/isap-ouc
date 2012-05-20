#-*- coding:utf-8 -*-
'''
Created on 2011-11-18
食品科学与工程学院，抓取信息来自最新动态，学生工作通知，学生活动集锦，
通知公告，党团工作（工作通知，最新动态，就业信息）,将这些链接存储在序列中，注意抓取
@author: hlq
'''
import urllib,MySQLdb,re,SrdpPage
from BeautifulSoup import BeautifulSoup
def GetByShiPin(url):
    html=urllib.urlopen(url).read();
    if "gb2312" in html:
        
        html=html.decode("gb2312","ignore")
    parser=BeautifulSoup(html);
    number=len(parser('a',target='_blank'))#a标签数        
    result=[]   
    for i in range(number):  
        example=[]             
        href=parser.findAll('a',target='_blank')[i]['href']
        if "show.asp" in href:                        
            name=parser('a',target='_blank')[i].string
            example.append(name)   
            content=[]                   
            content=SrdpPage.GetHtml("http://www2.ouc.edu.cn/shipin/"+href)
            time0=str(content.find('td',width='161'))
            #print time0
            time=ChoiceTime(time0)
            example.append(time)
            article=content.findAll('table',width='96%')
            example.append(article) 
            result.append(example)           
        else:
            continue 
        
    return result                    
def ChoiceTime(time):
    time0=re.findall(r'\d\d\d\d-\d\d-\d\d',time)
    time1=re.findall(r'\d\d\d\d-\d-\d\d',time)
    time2=re.findall(r'\d\d\d\d-\d\d-\d',time)
    time3=re.findall(r'\d\d\d\d-\d-\d',time) 
    s=""
    if time0==[]:
        if time1==[]:
            if time2==[]:
                if time3==[]:
                    s="传入时间出错，系统错误！"
                else:
                    s=time3[0]
            else:
                s=time2[0]
        else:
            s=time1[0]
    else:
        s=time0[0]        
    return s            