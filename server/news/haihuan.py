#-*- coding:utf-8 -*-
'''
Created on 2011-11-5
海洋环境学院抓取分析新闻和通知类
@author: hlq
'''
import urllib,MySQLdb,re
from BeautifulSoup import BeautifulSoup
def GetByHaiHuan(url):
    html=urllib.urlopen(url).read();
    html=html.decode("gb2312","ignore")
    parser=BeautifulSoup(html);
    number=len(parser('a'))#a标签数        
    n=0#将时间循环插入到result序列中的判断标志
    k=0#将href和title取出，如果a标签中没有href或title属性，程序将抛出KeyError异常    
    all=parser.findAll('span')#取出所有span标签的内容，用于提取文章时间
    timelist=[]#时间序列表
    result=[]#返回值的表
    for j in range(len(all)):#循环获得时间序列
        gettime=""
        if "lv2" in str(all[j]):
            gettime=GetTime(str(all[j]))
            #print str(all[j])
            if gettime=="":
                print "海洋环境学院获取时间类出现错误"
            else:
                timelist.append(gettime)
            #print gettime   
    for i in range(number):            
        title=[]        
        if k<16:
            #调用正则表达式取出含有news-ny.asp的href和title
            name=parser.findAll("a",href=re.compile('news-ny\.asp.'))[i]["title"]
            href=parser.findAll("a",href=re.compile('news-ny\.asp.'))[i]["href"]
            k=k+1
            title.append(name);
            title.append(GetInformation( "http://www2.ouc.edu.cn/cpeo/"+href))
            numbertime=len(timelist)
            if n<=numbertime:
                title.append(timelist[n])
                n=n+1
            result.append(title)
        else:
            break                       
    return result
                
                                 
#时间正则表达式，筛选符合的时间条件            
def ChoicTime(time):
    p=re.compile(r'\d\d\d\d-\d\d-\d\d')#时间匹配条件
    p1=re.compile(r'\d\d\d\d-\d-\d\d')
    p2=re.compile(r'\d\d\d\d-\d\d-\d')
    p3=re.compile(r'\d\d\d\d-\d-\d')
    match0=p.match(time)
    match1=p1.match(time)
    match2=p2.match(time)
    match3=p3.match(time)
    s=""
    if match0:#如果匹配，则返回该条
        s=match0.group()
    elif match1:
        s=match1.group()
    elif match2:
        s=match2.group()
    elif match3:
        s=match3.group()
    else:
        s=""
    return s 
def GetTime(times):
    time2=""#截取的times
    n=len(times)
    
    if n==39:#根据times的长度来截取字符串（通知）
        time2=times[24:32]
    elif n==40:
        time2=times[24:33]
    elif n==41:
        time2=times[24:34]
    elif n==34:#（新闻动态）
        time2=times[19:27]
    elif n==35:
        time2=times[19:28]
    elif n==36:
        time2=times[19:29]
    else:#如果不符合以上三种条件，time2继续为空
        time2=""
    #time0返回值                
    time0=""
    time0=ChoicTime(str(time2))  
    #print time2                
    if time0=="":
        time0=""
    else:
        return time0
          
def GetInformation(href):
    html=urllib.urlopen(href).read()#获取文章的内容，返回的是str类型
    html=html.decode("gb2312","ignore")
    parser=BeautifulSoup(html)
    p=parser.findAll('td',{'class':'font1'})
    #shu=len(p)
    ##print shu
    #content=""
    content="<table><tr>"+str(p[3])+"</tr></table>"
    return content    