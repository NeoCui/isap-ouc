# -*- coding: UTF-8 -*-
#对教务处的操作
import os,urllib2,cookielib,urllib,re,SQLHelper
import BeautifulSoup
from urllib import urlencode
import socket


#教务处网站
loginurl="http://jwc.ouc.edu.cn:8080/ouc/index.do"
logouturl="http://jwc.ouc.edu.cn:8080/ouc/logout.do"
chengji="http://jwc.ouc.edu.cn:8080/ouc/SS018.do"
class Tojwc():
    def __init__(self):
        self.session=''
        self.contents=''
    def trytoconnect(self,num,pwd,term):
        #此处未添加处理异常模块
        r=urllib2.Request(loginurl)
        h=urllib2.urlopen(r)
        html=h.read()	    
        
        #获取cookie
        cookie=h.info().getheader('Set-Cookie')
        cookie=cookie[:cookie.find(';')]
             
        #获取验证码
        htmlall=BeautifulSoup.BeautifulSoup(html)
        kaptchafield=htmlall.findAll('input',attrs={'name':'kaptchafield'})[0].parent.contents[3].attrs[3][1]
        
        post=urllib.urlencode({'subSystemName':'ouc.student','actionType':'Login','userId':num,
                'password':pwd,'kaptchafield':kaptchafield,
                'term':term,'submit.x':'0','submit.y':'0'})
        headers={'Connection':'keep-alive',
                     'Referer':'http://jwc.ouc.edu.cn:8080/ouc/index.do',
                        'Keep-Alive':'115',
                        'Content-Type':'application/x-www-form-urlencoded'}

        req=urllib2.Request(loginurl,post)
        req.add_header('Cookie',cookie)
        res=urllib2.urlopen(req).read()        
        if(res.find("登陆失败，请检查用户名、密码、验证码是否正确。")!=-1):    
            #登录失败
            return 1
        
        elif res.find("该用户已经登录，请登出或稍后再试!")!=-1:
            #该用户已经登录
            return 2
        else :
            self.contents=res.decode('GBK').encode('UTF-8')
            #soup=BeautifulSoup.BeautifulSoup(contents)
            #response=str(soup.findAll('table')[0])
            #抓取信息
            #登录成功
            self.session=cookie
            return 0
    def getContents(self):
        print "登陆成功"
    #注销
    def GetOneInformation(self):
        result=[]
        html=BeautifulSoup.BeautifulSoup(self.contents)
        name0=html('font',color='white')[0].string
        name=self.GetName(str(name0))
        p=html('p')[0].string
        print str(p)
        major=self.GetMajor(str(p))
        #pa=re.compile(r'\;')
        #name1=pa.split(str(name0))
        #name=str(name1[2])
        
        #print str(p)
        #major=re.findall(r'专业\:\S*\&nbsp',str(p[0]))
        result.append(name)
        result.append(major)
        return result
        
    def logout(self):
        r=urllib2.Request(logouturl)
        cookie=self.session
        r.add_header('Cookie',cookie)
        p=urllib2.urlopen(r)
    def getother(self):
        req=urllib2.Request(chengji)
        req.add_header('Cookie',self.session)
        res=urllib2.urlopen(req).read() 
        parser=BeautifulSoup.BeautifulSoup(res)
        print parser
    #该函数用于抓取通识限选课
    def GetAllCourse(self,academic,course,school,url):
        post=urllib.urlencode({
              'actionType':'query',
              'selAcademic':academic,
              'selCourse':course,
              'schoolhouse_select':school            
              })
        req=urllib2.Request(url,post)
        req.add_header('Cookie',self.session)
        res=urllib2.urlopen(req).read() 
        parser=BeautifulSoup.BeautifulSoup(res)
        return parser
    #该函数用于获取课程查询中某个分类的首页，例如通识必修课
    def GetAcademic(self,url):
        req=urllib2.Request(url)
        req.add_header('Cookie',self.session)
        res=urllib2.urlopen(req).read() 
        parser=BeautifulSoup.BeautifulSoup(res)
        academic=GrabAcademic(parser)
        allCourse=GrabAllCourse(parser)
        result=[]
        for i in range(len(academic)):
            for j in range(len(allCourse)):
                zong=[]
                course=str(allCourse[j])
                if str(academic[i][0])==course[2:11]:
                    zong.append(str(academic[i][0]))#开课单位代码
                    zong.append(str(academic[i][1]))#开课单位名称                
                    zong.append(course[14:26])#课程号
                    zong.append(course[29:len(course)-3])#课程名称
                    result.append(zong)
                else:
                    continue
                    #print str(academic[i][0]),str(academic[i][1]),course[2:11],course[14:26],course[29:len(course)-3]
        return result
        #print  获取成绩的页面信息
    def GetScore(self,url):
        req=urllib2.Request(url)
        req.add_header('Cookie',self.session)
        res=urllib2.urlopen(req).read() 
        parser=BeautifulSoup.BeautifulSoup(res)
        return parser
    #该函数获取已选课程页面信息
    def GetAlreadyCourse(self,url):
        req=urllib2.Request(url)
        req.add_header('Cookie',self.session)
        res=urllib2.urlopen(req).read() 
        parser=BeautifulSoup.BeautifulSoup(res)
        return parser
    def GetAreadyCourseContent(self,planyear,url):
        post=urllib.urlencode({
              'actionType':'search',             
              'xnxqF':'',
              'planYear':planyear          
              })
        req=urllib2.Request(url,post)
        req.add_header('Cookie',self.session)
        res=urllib2.urlopen(req).read() 
        parser=BeautifulSoup.BeautifulSoup(res)
        return parser
    def GetLimitCourse(self,schoolhouse,url):
        post=urllib.urlencode({
              'ActionType':'query',             
              'schoolhouse_select':schoolhouse,
              'query':'²é Ñ¯'          
              })
        req=urllib2.Request(url,post)
        req.add_header('Cookie',self.session)
        res=urllib2.urlopen(req).read() 
        parser=BeautifulSoup.BeautifulSoup(res)
        #print "parser="+str(parser)
        return parser
    def GetName(self,name0):
        pa=re.compile(r'\;')
        name1=pa.split(str(name0))
        if len(name1)<2:
            name=""
        else:
            name=str(name1[2])
        return name
    def GetMajor(self,major0):
        major=""
        p=r'&nbsp'
        pa=re.compile(p)      
        test=pa.split(major0)
    #print str(test[0])
        if len(test)<=0:
            major=""
        else:
            tr=re.findall(r'专业：\S*',str(test[0])) 
        #print str(tr[0]) 
        if len(tr)<=0:
            major="" 
        else:     
            tt=str(tr[0])                        
            major=str(tt[9:len(tt)])
            #print major
        return major
    #该函数用于获得专业课查询中的年级option
    def GetCourseGrade(self,academic,department,sepicalty, url):
        post=urllib.urlencode({
              'actionType':'querybj',
              'selAcademic':academic,
              'selDepartment':department,
              'selSepicalty':sepicalty            
              })
        req=urllib2.Request(url,post)
        req.add_header('Cookie',self.session)
        res=urllib2.urlopen(req).read() 
        html=BeautifulSoup.BeautifulSoup(res)       
        #html=BeautifulSoup(parser)
        result=[]
        length=len(html('option'))
        #print length
        if length>0:                          
            for i in range(length):
                grade=html('option')[i].string
                if len(grade)==2:
                    result.append(grade)
                else:
                    continue
        return result
    def GetMajorCourseContont(self,academic,department,sepicalty, grade,url):
        post=urllib.urlencode({
              'actionType':'query',
              'selAcademic':academic,
              'selDepartment':department,
              'selSepicalty':sepicalty,
              'schoolhouse_select':grade            
              })
        req=urllib2.Request(url,post)
        req.add_header('Cookie',self.session)
        res=urllib2.urlopen(req).read() 
        html=BeautifulSoup.BeautifulSoup(res)  
        return html     
        #html=BeautifulSoup(parser)
    def GetStudentChooseCourse(self,url):
        req=urllib2.Request(url)
        req.add_header('Cookie',self.session)
        res=urllib2.urlopen(req).read() 
        html=BeautifulSoup.BeautifulSoup(res)  
        return html     
    def GetMajorHTML(self,url):
        req=urllib2.Request(url)
        req.add_header('Cookie',self.session)
        res=urllib2.urlopen(req).read() 
        html=BeautifulSoup.BeautifulSoup(res)  
        return html     
#    #该函数是将专业课中的课程分类存储到数据库中，参数result为查询专业课后返回的一个序列，content是经过BeautifulSoup的目标网页
#    def InsertMajorClass(self,result,content):
#        for i in range(len(result)):
#            k=1
#            for j in range(len(content)):
#                getclass=SplitClass(str(content[j]))
#                Values=[]
#            #判断是否跟学院的ClassID 相同，相同的是该学院下的系
#                if str(result[i][0])==str(getclass[0]):
#            #print str(getclass[0])
#            #判断该系是否已经存储在数据库中，返回的是一个int类型
#                    count=SQLHelper.GetCountOne("CourseClass","ClassID",str(getclass[1]))                
#                    if count==1:                
#                        for y in range(len(content)):
#                            major=SplitClass(str(content[y]))
#                        #print str(major[0])
#                            v=[]
#                            if str(getclass[1])==str(major[0]):                                                                                                                                                            
#                                a=str(major[0])
#                            #print a
#                                b=str(major[1])
#                                d=""
#                                if str(getclass[1])=="jwjw":
#                                    d="jwjw"+b
#                                else:                                
#                                    d=a+b
#                                #print d
#                                c=SQLHelper.GetCountOne("CourseClass","ClassID",d)
#                            #print c
#                                if c==1:
#                                    continue
#                                else:
#                                    v=[d,str(major[2]),str(result[i][2]),b,str(getclass[1])] 
#                                    number=SQLHelper.Insert("CourseClass",["ClassID","ClassName","RootID","OrderID","ParentID"],v)
#                                    if number==1:
#                                        continue
#                                    else:
#                                        print "插入错误" 
#                                #for g in range(len(v)):
#                                   # print str(v[g])
#                             
#                    else:
#                        Values=[str(getclass[1]),str(getclass[2]),str(result[i][2]),str(k),str(result[i][0])]
#                        n=SQLHelper.Insert("CourseClass",["ClassID","ClassName","RootID","OrderID","ParentID"], Values)
#                        if n==1:                    
#                            continue
#                        else:
#                            print "插入错误"
#                #for g in range(len(Values)):
#                #    print str(Values[g])
#                        k=k+1
#                else:
#                    continue
#该函数用于抓取某课程所有开课信息，返回的是一个包含多个序列的序列，传入的参数是一个已经BeautifulSoup的字符串类型
def GrabCourse(parser):
    #number=parser('tr',id='record')
    #print len(number)
    txt=parser('td',{"class":"mytd"})
    #print parser('td',{"class":"mytd"})
    #print len(txt)
    #print str(txt[0])
    #x=str(txt[0])
    #print len(x)
    #print x[32:len(x)-11]
    result=[]
    other=[]
    for i in range(len(txt)):
        x="";
        x=str(txt[i])
        other.append(x[32:len(x)-11])
        #print x[32:len(x)-11]
        if(i+1)%8==0:
            result.append(other)
            other=[]
        else:
            continue
    #for j in range(len(result[0])):
        #print result[0][j]
    return result
#该函数用于抓取专业课中的课程信息
def GrabMajorCourse(parser):  
    txt=parser('td',{"class":"mytd"})#获取课程其他信息的td数量
    NameNumber=parser('td',{"class":"hand"})  #获取课程名称的td数量 
    all=parser.findAll('td',{"class":"hand"});
    result=[]#初始化变量
    other=[]
    #判断条件，当两者均大于0的时候才可以继续抓取信息
    if (len(txt))>0 and (len(NameNumber))>0:
        #主节点
        #for j in range(len(NameNumber)):
        #    name="";
        #    other=[];
            #获得课程名称
            #name=parser('td',{"class":"hand"})[j].string;
        #    name=str(all[j])[63:len(all[j])-13]   
        #    print name
        #    other.append(name);
            #次节点
        for i in range(len(txt)):
            x="";
            x=str(txt[i])
            other.append(x[32:len(x)-11])
                #print x[32:len(x)-11]
            a=(i+1)%10;
            if a==0:
                b=(i+1)/10-1;
                if b<=(len(NameNumber)):
                    name=str(all[b])[95:len(all[b])-13] 
                    other.append(name);
                    result.append(other)
                    other=[]
            else:
                continue
    
    return result
#该函数用于抓取同时限选课信息
def GrabLimitCourse(parser):  
    txt=parser('td',{"class":"mytd"})#获取课程其他信息的td数量
    NameNumber=parser('td',{"class":"hand"})  #获取课程名称的td数量 
    all=parser.findAll('td',{"class":"hand"});
    result=[]#初始化变量
    other=[]
    #判断条件，当两者均大于0的时候才可以继续抓取信息
    if (len(txt))>0 and (len(NameNumber))>0:
       
        for i in range(len(txt)):
            x="";
            x=str(txt[i])
            if 'align="left"' in str(txt[i]) :
                other.append(x[30:len(x)-11])
            else:               
                other.append(x[32:len(x)-11])
                #print x[32:len(x)-11]
            a=(i+1)%9;
            if a==0:
                b=(i+1)/9-1;
                if b<=(len(NameNumber)):
                    name=str(all[b])[65:len(all[b])-13] 
                    #print name
                    other.append(name);
                    result.append(other)
                    other=[]
            else:
                continue
    
    return result
#该函数用于抓取开课单位的，返回的是一个含有多个序列的序列，传入的参数是一个已经BeautifulSoup的字符串类型
def GrabAcademic(parser):
    academic=[]
    number=len(parser('option'))
    #print number
    for i in range(number):
        value=parser('option')[i]['value']
        academic0=[]
        if len(value)<9:
            continue
        else:
            name=parser('option')[i].string
            academic0.append(value)
            academic0.append(name)
            academic.append(academic0)
    
    #for j in range(len(academic)):
    #    for k in range(len(academic[j])):
    #        print str(academic[j][k])
            
    return academic
def GrabAllCourse(parser):
    p=r'MATRIX(\S*)'
    pa=re.findall(p,parser.prettify())
    return pa
#该函数用于将专业课中的院系和专业分开，返回的是一个序列
def SplitClass(content):
    result=[]
    p=re.compile(r'\,')
    pa=p.split(content)
    
    pa0=str(pa[0])[2:len(pa[0])-1]#根据网页分析，pa0可以是系的类号或者是院的分类号
    pa1=str(pa[1])[1:len(pa[1])-1]#可能是院的分类号或者是系的分类号
    pa2=str(pa[2])[1:len(pa[2])-3]#可能是系的名称或者是专业的名称
    result.append(pa0)
    result.append(pa1)
    result.append(pa2)
    return result

#该函数是将专业课中的课程分类存储到数据库中，参数result为查询专业课后返回的一个序列，content是经过BeautifulSoup的目标网页
def InsertClass(result,content):
    for i in range(len(result)):
        k=1
        for j in range(len(content)):
            getclass=SplitClass(str(content[j]))
            Values=[]
            #判断是否跟学院的ClassID 相同，相同的是该学院下的系
            if str(result[i][0])==str(getclass[0]):
            #print str(getclass[0])
            #判断该系是否已经存储在数据库中，返回的是一个int类型
                count=SQLHelper.GetCountOne("CourseClass","ClassID",str(getclass[1]))                
                if count==1:                
                    for y in range(len(content)):
                        major=SplitClass(str(content[y]))
                        #print str(major[0])
                        v=[]
                        if str(getclass[1])==str(major[0]):                                                                                                                                                            
                            a=str(major[0])
                            #print a
                            b=str(major[1])
                            d=""
                            if str(getclass[1])=="jwjw":
                                d="jwjw"+b
                            else:                                
                                d=a+b
                                #print d
                            c=SQLHelper.GetCountOne("CourseClass","ClassID",d)
                            #print c
                            if c==1:
                                continue
                            else:
                                v=[d,str(major[2]),str(result[i][2]),b,str(getclass[1])] 
                                number=SQLHelper.Insert("CourseClass",["ClassID","ClassName","RootID","OrderID","ParentID"],v)
                                if number==1:
                                    continue
                                else:
                                    print "插入错误" 
                                #for g in range(len(v)):
                                   # print str(v[g])
                             
                else:
                    Values=[str(getclass[1]),str(getclass[2]),str(result[i][2]),str(k),str(result[i][0])]
                    n=SQLHelper.Insert("CourseClass",["ClassID","ClassName","RootID","OrderID","ParentID"], Values)
                    if n==1:                    
                        continue
                    else:
                        print "插入错误"
                #for g in range(len(Values)):
                #    print str(Values[g])
                    k=k+1
            else:
                continue
            
    