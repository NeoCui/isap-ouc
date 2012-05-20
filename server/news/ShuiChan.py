#-*- coding:utf-8 -*-
'''
Created on 2012-2-15
水产学院信息抓取，信息包括学院要闻、学院通知、党团工作、本科生教育、
研究生培养、就业工作、学术交流、实验室基地、水漾年华、星空等
@author: hlq
'''
import urllib,MySQLdb,re,SrdpPage
from BeautifulSoup import BeautifulSoup
#ClassID号和分类名称，url为http://www2.ouc.edu.cn/shuichan/Article_Class2.asp?ClassID=1
ID=[["1","学院要闻"],["59","学院通知"],["2","党团工作"],["3","本科生教育"],["63","研究生培养"],["65","就业工作"],["66","学术交流"],["67","水漾年华"],["68","星空"] ]
def GetByShuiChan(url):
    html=urllib.urlopen(url).read();
    if "gb2312" in html:
        html=html.decode("gb2312","ignore");
    elif "GB2312" in html:
        html=html.decode("GB2312","ignore"); 
    parser=BeautifulSoup(html);
    
    number=len(parser('a',href=re.compile('Article\_Show\.asp\?ArticleID\=')))#a标签数 
    href=re.findall(r'Article\_Show\.asp\?ArticleID\=\d+',html);
    #print str(href[0])
    font=len(parser('font',color='#333333'))
    #print number,font     
    result=[]#返回值的表
    for i in range(number):            
        title=[]        
            #调用正则表达式取出含有news-ny.asp的href和title
        name=parser.findAll("a",href=re.compile('Article\_Show\.asp\?ArticleID\='))[i]["title"]

        name0=ChoiceTitle(str(name))
            #href=parser.findAll("a",href=re.compile('news-ny\.asp.'))[i]["href"]
        #print str(name0)
       
        title.append(name0);
        time=SrdpPage.ChoiceTime(str(name))
        title.append(time)
        content=SrdpPage.GetHtml("http://www2.ouc.edu.cn/shuichan/"+str(href[i]));
        
        article=content.findAll('p');
        #print len(article)
        title.append(article)
        result.append(title)
#        else:
#            break                            
    return result
                                               
def ChoiceTitle(title):
    p=re.findall(r'文章标题：\S+',title)#时间匹配条件
#    match0=p.match(title)
    s=str(p[0])
    
#    if match0:#如果匹配，则返回该条
#        s=match0.group()
    name=s[15:len(s)]
    return name 
        