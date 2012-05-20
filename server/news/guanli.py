#-*- coding:utf-8 -*-
'''
Created on 2011-11-19

@author: hlq
'''
import urllib,MySQLdb,re,SrdpPage
from BeautifulSoup import BeautifulSoup
UrlAll={
        '最新动态左':"http://www2.ouc.edu.cn/glxy/Article/zuixindongtai/",
        '最新动态右':"http://www2.ouc.edu.cn/glxy/Article/zuixindongtai2/",
        '学院工作':"http://www2.ouc.edu.cn/glxy/Article/ShowClass.asp?ClassID=24",
        '学生工作':"25",
        '本科生教学工作':"58",
        '研究生教学工作':"62",
        '毕业生工作':"http://www2.ouc.edu.cn/glxy/Article/deyugongzuo/biyeshenggongzuo/"
                   
        }
#该函数用于抓取工程学院首页的新闻和通知信息
def GetByGuanLi(url):
    html=urllib.urlopen(url).read();
    if "gb2312" in html:
        html=html.decode("gb2312","ignore");
    parser=BeautifulSoup(html);
    number=len(parser('a',target='_blank'))#a标签数,根据网页分析href采用正则表达式分析出想要的a的准确数量          
    result=[]   
    #print number
    if number==0:
        result=[]
    else:
            
        for i in range(number):  
            example=[]             
            href=parser.findAll('a',target='_blank')[i]['href']      
            title=parser('a',target='_blank')[i].string        
            time=parser('td',id='time')[i].string
            if "/glxy/Article/" in href:                       
                content=SrdpPage.GetHtml("http://www2.ouc.edu.cn"+href)                                               
                article=content.findAll('table',width='80%');
                #print len(article)
                if len(article)==0:
                    l=str(content)
                    tt=re.findall(r'href=\'http\S+\'',l)
                    #print tt
                    s=str(tt[0])
                    href2=s[6:len(s)-1];
                    #print href2
                    content2=SrdpPage.GetHtml(href2)   
                    article=content2.findAll('p')
                    #print article
                example.append(title)
                example.append(time)          
                example.append(article) 
                      
                result.append(example) 
            else:
                continue 
            
    return result  
#该函数用于抓取管理学院的学生会网站的信息
def GetByGLXueSHui(url):
    html=urllib.urlopen(url).read();
    parser=BeautifulSoup(html);
    number=len(parser('a',title="查看详细"))#a标签数,根据网页分析href采用正则表达式分析出想要的a的准确数量          
    result=[]   
    #print number
    if number==0:
        result=[]
    else:
            
        for i in range(number):  
            example=[]             
            hrefall=parser.findAll('a',title="查看详细")[i]['href']
            
            href=hrefall[3:len(hrefall)]
            
            title=parser('a',title="查看详细")[i].string 
                 
            time=parser('p')[i].string
            if "info/info_detail.asp?intArticleid=" in href:  
                #print href                     
                content=SrdpPage.GetHtml("http://www.hdglxyxsh.com/"+href)                                               
                article=content.findAll('p')
                example.append(title)
                example.append(time)            
                example.append(article)            
            else:
                continue 
            result.append(example)
    return result  
#该函数用于获得正确的标题，去除掉没用的标签 
def GetTitle(title):
    length=len(title)
    name=title[58:length-5] 
    return name                                        
