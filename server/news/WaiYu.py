#-*- coding:utf-8 -*-
'''
Created on 2011-11-23

@author: hlq
'''
import urllib,MySQLdb,re,SrdpPage
from BeautifulSoup import BeautifulSoup
UrlAll={
        '首页':"http://222.195.158.203/index.aspx",
        '最新动态':"http://222.195.158.203/index.aspx?menuid=8&type=article&lanmuid=303&language=cn",
        '工作通知':"http://222.195.158.203/index.aspx?menuid=8&type=article&lanmuid=323&language=cn",
        '就业信息':"http://222.195.158.203/index.aspx?menuid=8&type=article&lanmuid=310&language=cn"                          
        }
#该函数用于抓取工程学院首页的新闻和通知信息
def GetByWYShouYe(url):
    #html=urllib.urlopen(url).read();
    parser=SrdpPage.GetHtml(url) ;
    number=len(parser('a',style=''))#a标签数,根据网页分析href采用正则表达式分析出想要的a的准确数量          
    result=[]   
    #print number
    if number==0:
        result=[]
    else:
            
        for i in range(number):  
            example=[]             
            href=parser.findAll('a',style='')[i]['href']                   
            #title=parser('a',target='_blank')[i].string        
            #time=parser('td',id='time')[i].string
            if "/index.aspx?menuid=" in href:
                if "http://www." in href:
                    continue
                else:                                           
                    content=SrdpPage.GetHtml("http://222.195.158.203"+href)                                                       
                    article=content.findAll('p')
                    titleall=content('div')
                    title=GetTitle(str(titleall[0]))                
                    time=SrdpPage.ChoiceTime2(str(titleall[0]))
                    example.append(title)
                    example.append(time)    
                    example.append(article)            
            else:
                continue 
            result.append(example)
    return result  
#该函数用于获得正确的标题，去除掉没用的标签 

def GetTitle(titleall):
    pa=re.findall(r'\<div\s*class=\"articleinfor_title\"\>.*\<\/div\>',titleall)    
    t=str(pa[0])     
    title=t[32:len(t)-6]    
    return title