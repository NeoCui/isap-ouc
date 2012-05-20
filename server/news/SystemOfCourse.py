# -*- coding: UTF-8 -*-
'''
Created on 2012-3-25

@author: hlq
'''
import urllib,re,SrdpPage
from BeautifulSoup import BeautifulSoup
#该函数用于抓取选课系统首页的通知信息
def GetByCourse(url):
    html=urllib.urlopen(url).read();
    if "gb2312" in html:
        html=html.decode("gb2312","ignore");
    parser=BeautifulSoup(html);
    p=re.findall(r'winopen\S+\)',str(html))
    for k in range(len(p)):
        print str(p[k])
    number=len(p)#a标签数,根据网页分析href采用正则表达式分析出想要的a的准确数量          
    number2=len(parser('td'))
    result=[]   
    timelist=[]
    #print number,number2
    for j in range(number2):      
        time=parser('td')[j].string       
        if time!="":
            time0=SrdpPage.ChoiceTime3(str(time))
            if time0!="":
                #print time0
                timelist.append(time0)
            else:
                continue
        else:
            continue
    if number==0:
        result=[]
    else:                      
        #http://jwc.ouc.edu.cn:8080/ouc/News.html?nid=              
        for i in range(number):  
            example=[]             
            #href=parser.findAll('a',onClick=re.compile(r'winopen\S+\)'))[i]['OnClick']      
            href0="http://jwc.ouc.edu.cn:8080/ouc/News.html?nid="+ str(p[i])[8:len(str(p[i]))-1]
            title=parser('a')[i+4].string                         
            content=SrdpPage.GetHtml(href0)                                                             
            article=content.findAll('td',align='left')
            example.append(title)
            example.append(timelist[i])          
            example.append("<table><tr>"+str(article[0])+"</tr></table>")                       
            result.append(example) 
    return result   