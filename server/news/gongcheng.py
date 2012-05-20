#-*- coding:utf-8 -*-
'''
Created on 2011-11-19
工程学院信息
@author: hlq
'''
import urllib,MySQLdb,re,SrdpPage
from BeautifulSoup import BeautifulSoup
UrlAll={
        '首页':"http://www3.ouc.edu.cn/gongcheng/",
        '学生活动通知':"32",
        '学生活动新闻':"33",
        '工作通知':"38",
        '就业信息':"39",
        '就业指导':"40",
        '资助公示':"42",
        '资助通知':"43"              
        }
#该函数用于抓取工程学院首页的新闻和通知信息
def GetByGongCheng(url):
    html=urllib.urlopen(url).read();
    html=html.decode("gb2312","ignore")
    parser=BeautifulSoup(html);
    number=len(parser('a',href=re.compile('ShowNotice\.aspx.')))#a标签数,根据网页分析href采用正则表达式分析出想要的a的准确数量          
    result=[]       
    for i in range(number):  
        example=[]             
        href=parser.findAll('a',href=re.compile('ShowNotice\.aspx.'))[i]['href']
        if "ShowNotice.aspx" in href:                       
            content=SrdpPage.GetHtml("http://www3.ouc.edu.cn/gongcheng/"+href)
            title=str(content('p',id='title'))            
            time0=str(content.find('div',id='intro'))
            time=SrdpPage.ChoiceTime(time0)
            article=content.findAll('div',id='content')
            example.append(GetTitle(title))            
            example.append(time)  
            example.append(article)                                 
        else:
            continue 
        result.append(example)
    return result  
#该函数用于获得学生工作以及毕业生工作等其他的信息，由于这些网页格式与首页不同因此分开来抓取
def GetByGongCheng2(url):
    html=urllib.urlopen(url).read();
    html=html.decode("gb2312","ignore")
    parser=BeautifulSoup(html);
    number=len(parser('a',href=re.compile('ShowArticle\.aspx.')))#根据网页分析，该网页中含有ShowArticleList.aspx，故用正则表达式来选择正确的标题文章链接  
    #print number       
    result=[]     
    for i in range(number):  
        example=[]             
        href=parser.findAll('a',href=re.compile('ShowArticle\.aspx.'))[i]['href']
        #print href
        if "ShowArticle.aspx" in href:            
            title=parser('a',href=re.compile('ShowArticle\.aspx.'))[i].string
            choicetitle=SrdpPage.ChoiceTime(title)
            #print choicetitle
            if choicetitle=="":                
                content=SrdpPage.GetHtml("http://www3.ouc.edu.cn/gongcheng/"+href)
                title=str(content('p',id='title'))
                time0=str(content.find('div',id='intro'))
                time=SrdpPage.ChoiceTime(time0)
                article=content.findAll('div',id='content')
                example.append(GetTitle(title))
                
                example.append(time)            
                example.append(article)
            else:
                continue                                                    
        else:
            continue 
        result.append(example)
    return result 
#该函数用于获得正确的标题，去除掉没用的标签 
def GetTitle(title):
    length=len(title)
    name=title[58:length-5] 
    return name                                        
