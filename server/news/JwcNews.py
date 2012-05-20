#-*- coding:utf-8 -*-
'''
Created on Oct 11, 2011

@author: hlq
'''

import urllib,MySQLdb,traceback,time
import SQLHelper
from BeautifulSoup import BeautifulSoup
#获取教务处的新闻链接信息(标题，链接，时间)，返回的是一个列表
def geturl(url):
    html=urllib.urlopen(url).read()
    parser=BeautifulSoup(html)
    #print parser
    number=len(parser('a'))
    #number2=len(parser('font',color="#808080"))
    j=0
   
    #print parser('font',color='#808080')[0].string
    #print number#,number2测试时使用
    result=[]
    for i in range(number):
        name=parser('a')[i].string
        #print name
        href=parser.findAll('a')[i]['href']       
        title=[]
        time=""
        if "news_id" in href:#找到含有news_id的a标签，抓取出href
            #print name
            n=GetCount(name,"教务处")#调用GetCount函数检测数据库中是否含有该项内容
            #print name #测试时使用的
            if n<=0:
                title.append(name)
                hrefall="http://jwc.ouc.edu.cn:8080/jwwz/"+href
                title.append(hrefall)
                #抓去相应标题的文章内容，放在result列表中
                content=GetInformation(hrefall)#访问下级页面获得该链接的文章内容
                title.append(content)                
                if j<=19:  #根据对网页的分析，共有40个font，color=#808080的标签，抓去出相应的时间                             
                    time=parser('font',color="#808080")[2*j].string            
                    j=j+1              
                    title.append(str(time))
            #print title
            if(len(title)<=0):
                continue;
            else:               
                result.append(title)
            
            #else:
                #break       
    #print j
    return result
    
#存放到MySql数据库中的函数暂时先不写 
#db=MySQLdb.connect(host='localhost',user='root',passwd='1',db='SrdpDB',charset="utf8")
#db.ping()
def GetCount(title,classname):#验证数据库中是否包含该条信息
#    cur=db.cursor()
    #count=cur.execute("select * from Information where Title='"+title+"' and ClassName='"+classname+"'")
    ask=["Title","NewsClassName"]
    answer=[title,classname]
    count=SQLHelper.GetCountMore("News", ask, answer)
    #cur.close()
    #db.close()
    return count
def GetInformation(newsurl):
    html=urllib.urlopen(newsurl).read()#获取文章的内容，返回的是str类型
    parser=BeautifulSoup(html)
    p=parser.findAll('p')
    shu=len(p)
    #print shu
    content=""
    for i in range(shu):
        content=content+str(p[i])
    return content
def InsertDB(url):#插入到数据库中
    #try:
    information=[]
    information=geturl(url)
    length=len(information)
    #print length
    #print information
    if(length<=0):
        print time.ctime()+"\t"+"教务处新闻------暂无更新"
        return 0
    else:   
        information2=sorted(information,key=lambda news:news[3])
        for i in range(length):
#            print len(MySQLdb.escape_string(information2[i][2]))
#            cur=db.cursor()
            #field=["Title","Content","Time","ClassID","ClassName"]
            #value=[str(information[i][0]),MySQLdb.escape_string(information[i][2]),information[i][3],3,"教务处"]
            #insert=SQLHelper.Insert("Information", field, value)
            number="insert into News(Title,Content,Time,NewsClassName,NewsClassID) values('%s','%s','%s','%s','%d')"% (str(information2[i][0]),MySQLdb.escape_string(information2[i][2]),information2[i][3],"教务处",16)
            insert=SQLHelper.InsertAboutNumber(number)
        
            if insert==1:
                continue;
            else:
                print "插入新闻出现错误！！"
            #cur.execute("insert into Information(Title,Content,Time,ClassID,ClassName) values('%s','%s','%s','%d','%s')"% (str(information[i][0]),MySQLdb.escape_string(information[i][2]),information[i][3],3,"教务处"))
        print time.ctime()+"\t教务处新闻更新数目:"+str(length)
        #有更新
        return 1
    #print "OK"
#    cur.close()
#    db.commit()
#    db.close()