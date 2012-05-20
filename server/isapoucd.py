# -*- coding: UTF-8 -*-
# ----
# @generated by Jiakun Huang on 2011.11.06
# ----
#服务器端守护进程
import threading

def threadFactory(*args,**kwargs): 
    t = threading.Thread(**kwargs) 
    t.setDaemon(True) 
    return t

from twisted.python import threadpool
threadpool.ThreadPool.threadFactory = threadFactory 
from twisted.python import threadable
threadable.init()
from twisted.internet.protocol import Protocol,Factory
from twisted.internet import  reactor,defer,threads
from twisted.protocols.basic import LineReceiver
import os,sys,time,traceback
import actiontojwc
import CourseMain
from news import NewsMain


#数据库操作
import SQLHelper as sql
reload(sys)
sys.setdefaultencoding('utf-8')


#协议类
class IsapoucProtocol(LineReceiver):
    def __init__(self):
        self.count=0
        self.student=None
        self.newtermstart=False
        self.firstlogin=False
        #用户当前最新新闻的id，用此id和数据库中新闻id对比，数据库中id比此id大的就是更新的新闻
        self.curnewsid={"16":'',"15":'',"3":''}
        self.LENGTH=1024
    def lineReceived(self,data):
        information=data.split('|||')
        #登录
        if information[0]=="login":
            if information[1] not in self.factory.users:
                #检查是否第一次登录
                self.checkFirstLogin(information[1], information[2])
                print "number:"+information[1]
            else:
                self.sendLine("login|||failure|||2")
        #不是登录就想获取数据！
        elif not self.transport.getPeer().host in self.factory.ip:
            self.sendLine("不登录就想获取数据！")
            self.transport.loseConnection()
            
        #模块定制
        if information[0]=="options":
#            flag==下次是否仍显示模块定制对话框
#            jwcnews==是否定制教务处新闻
#            xknews==是否定制选课系统新闻
#            facultynews==是否定制院系新闻
            sql.Update("Options", ["flag"], [information[1]], "UserNumber", self.student[1]) 
            sql.Update("Options", ["jwcnews"], [information[2]], "UserNumber", self.student[1]) 
            sql.Update("Options", ["xknews"], [information[3]], "UserNumber", self.student[1]) 
            sql.Update("Options", ["facultynews"], [information[4]], "UserNumber", self.student[1]) 
            
        #好友
        if information[0]=="friends":
            #搜索
            if information[1]=="search":
                self.searchFriend(information[2])
            #添加
            if information[1]=="add":
                self.addFriend(information[2], information[3],information[4])
            #删除
            if information[1]=="delete":
                self.deleteFriend(information[2],information[3])
                self.deleteFriend(information[3], information[2])
        #发送好友列表
        if information[0]=="getfriends":
            self.sendFriends()
        #发送消息
        if information[0]=="message":
            self.sendMsg()
        #发送新闻
        #按页数返回10条记录
        if information[0]=="get10news":
            self.send10News(information[1],information[2])
        #按id返回最新新闻
        if information[0]=="getnewsbyid":
            self.sendNewsbyID(information[1],information[2])
        #按id返回内容
        if information[0]=="getnewscontent":
            print information
            self.sendNewsContent(information[1],information[2])
        #客户端请求新闻页数
        if information[0]=="getnewspage":
            self.sendNewsPage(information[1])
#            self.sendNewsPage("15")
            self.send10News("0", information[1])
#            self.send10News("0", "15")
#            self.th.callInThread(self.listennews)
#            self.th.callInThread(self.listenMsg)  
        #发送课程信息
        if information[0]=="getcourses":
#            print information
            self.sendCourse(information[1])
        #发送学期列表
        if information[0]=="getterm":
            if self.firstlogin==False:
                self.sendTerm()
        #发送好友学期列表
        if information[0]=="getfriendterm":
            self.sendFriendTerm(information[1])
        #发送好友课程
        if information[0]=="getfriendcourses":
            self.sendFriendCourse(information[1],information[2])
        #客户端通知服务器开始检测是否有最新新闻和最新消息，一旦触发，服务器每2s验证一次
        if information[0]=="startlistening":
            threads.deferToThread(self.listennews)
            threads.deferToThread(self.listenMsg)    
            
        #注销
        if information[0]=="logout":
            self.transport.loseConnection()

        #elif information[0]=="getcourses":
    #连接打开        
    def connectionMade(self):
        print  "+ Connection from: "+ self.transport.getPeer().host#ip
    #连接关闭
    def connectionLost(self,reason):
        self.factory.num=self.factory.num-1
        if self.student:
            self.factory.users.remove(self.student[1])
        ip=self.transport.getPeer().host
        if ip in self.factory.ip:
            self.factory.ip.remove(ip)
#        self.th.stop()
#        self.th=None
        self.connected=0
        print  "-Lose Connection from: "+ self.transport.getPeer().host 

#登录及选项操作        
    def checkFirstLogin(self,num,pwd):
        #检查是否第一次登录（通过查数据库）
        count=sql.GetCountOne("User", "UserNumber", num)
        if count==0:
            print "第一次登录"
            self.firstlogin=True
            stu=actiontojwc.Connectjwc()
            result=stu.tryconnect(num, pwd, '20111')
            if result==0:    #学期以后一定要设置！！！
                stu.getUserInfo()
                stu.logout()
                self.student=[]
                self.student.append("none")
                self.student.append(stu.num)
                self.student.append(stu.name)
                self.student.append(stu.pwd)
                self.student.append(stu.major)
                self.student.append(stu.grade)
                self.factory.num=self.factory.num+1
                self.factory.users.append(stu.num)
                self.factory.ip.append(self.transport.getPeer().host)
                #抓取课程，存入数据库
                Field=["UserNumber","UserName","UserPwd","UserMajor","UserGrade"]
                Values=[stu.num,stu.name,stu.pwd,stu.major,stu.grade]
                #抓取已选课程
#                self.th.callInThread(self.grabCourse)
#                self.th.callInThread(self.grabScore)
                threads.deferToThread(self.grabCourse)
                threads.deferToThread(self.grabScore)
#没有异常处理
                sql.Insert("User", Field, Values)
                sql.Insert("Options",["UserNumber"],[stu.num])
                self.sendLine("login|||success|||"+stu.num+"|||"+stu.name+"|||"+stu.major+"|||"+stu.grade)
                #在线用户增加一个,user中增加一个学号，ip增加一个ip
                self.factory.num=self.factory.num+1
                self.factory.users.append(self.student[1])
                self.factory.ip.append(self.transport.getPeer().host)
                self.sendLine("options|||1|||1|||1|||1")
            elif result==1:
                self.sendLine("login|||failure|||1")
            else :
                self.sendLine("login|||failure|||2")
            
        else:#不是第一次登录
            print "不是第一次登录"
            stu=sql.GetData("select * from User where UserNumber="+num)[0]
            self.student=stu
            if self.student =="":
                self.sendLine("login|||failure|||1")
            elif self.student[3]!=pwd:
                self.sendLine("login|||failure|||1")
            else:
                datalog="login|||success|||"+self.student[1]+"|||"+self.student[2]+"|||"+self.student[4]+"|||"+self.student[5]
                #学号、姓名、专业、年级
                self.sendLine(datalog.encode('UTF-8'))
                #在线用户增加一个,user中增加一个学号，ip增加一个ip
                self.factory.num=self.factory.num+1
                self.factory.users.append(self.student[1])
                self.factory.ip.append(self.transport.getPeer().host)
                #新学期开始
#                if self.newtermstart==True:
#                    threads.deferToThread()
                
                
                self.options=sql.GetData("select * from Options where UserNumber="+num)[0]
                
                #模块定制
                dataopt="options|||"+self.options[2]+"|||"+self.options[3]+"|||"+self.options[4]+"|||"+self.options[5]
                self.sendLine(dataopt.encode('UTF-8'))
                
#好友
    #搜索好友
    def searchFriend(self,name):
        result=sql.GetData("select * from User where UserName='"+name+"'")
        #搜索结果
        #不存在
        if len(result)==0:
            self.sendLine("friends|||search|||0") 
        else:
            for item in result:
                self.sendLine(("friends|||search|||1|||"+item[1]+"|||"+item[2]+"|||"+item[4]+"|||"+item[5]).encode('UTF-8'))
    #添加好友
    def addFriend(self,number,hostnum,flag):
        result=sql.GetData("select * from User where UserNumber='"+number+"'")
        if len(result)==0: 
            self.sendLine("friends|||add|||0")        
        else:
            #self.sendLine("friends|||add|||3")
            sql.Insert("Message", ["sourcenum","desnum","flag"], [hostnum,number,flag])
            if flag=="2":
                #同意好友申请，数据库中增加记录
                self.inserFriend(number)
                self.sendFriends()
    #删除好友
    def deleteFriend(self,number,hostnum):
        id=sql.GetDataByMore("Friend", ["UserNumber","FriendNumber"], [str(hostnum),str(number)])[0][0]
        sql.Delete("Friend", "id", str(id))
    
                
        #未处理异常
        
        
    def sendNewsPage(self,newsclass):
        #教务处新闻页数
        jwc=sql.GetCountOne("News", "NewsClassID", newsclass)
        page=jwc/10
        if jwc%10 !=0:
            page=page+1
        self.sendLine("newspage|||"+str(page)+"|||"+newsclass)
        #选课系统新闻页数
        
    def send10News(self,page,newsclass):
        #发送10条新闻，客户端一页显示10条
        ten=sql.GetData("SELECT * FROM News where NewsClassID="+newsclass+" order by id desc LIMIT "+str(int(page)*10)+ ",10")
        if len(ten)!=0:
            for item in ten:
                print item[0]
                self.sendLine("news|||"+str(item[0])+"|||"+str(item[1])+"|||"+str(item[4]))
            if page=="0":
                self.curnewsid[newsclass]=str(ten[0][0])
    
    def sendNewsbyID(self,id,newsclass):
        #id=新闻id，newsclass=新闻类型
        #按照id发送新闻
        result=sql.GetData("select * from News where NewsClassID="+newsclass+" and id >'"+id+"' order by id desc ")
        if len(result) !=0:
            self.curnewsid[newsclass]=str(result[0][0])
            for item in result:
                self.sendLine("newsupdated|||"+str(item[0])+"|||"+str(item[1])+"|||"+str(item[4]))
        else:
            print newsclass+"\tNo new news."
    def listennews(self):
        #检测最新新闻
        if self.connected:
            if self.curnewsid["16"]!="":
                self.sendNewsbyID(self.curnewsid["16"], "16")
            if self.curnewsid["15"]!="":    
                self.sendNewsbyID(self.curnewsid["15"], "15")
#            self.sendNewsbyID(self.curnewsid["5"], "5")
            reactor.callLater(10,self.listennews)
    
        
    def sendNewsContent(self,id,newsclass):
        #发送id的新闻内容
        result=sql.GetData("select * from News where id="+id+" and NewsClassID="+newsclass)[0]
#        self.sendLine("newscontent")
        self.send("newscontent|||",str(result[2]))
#        self.send(str(result[2]))
#    def getjwcNewsid(self):
#        self.sendLine("getnewsbyid|||5")

    def sendTerm(self):
        #发送用户的学期列表，用户通过学期来获取课程信息
        result=sql.GetData("select Term from Course where UserNumber="+str(self.student[1]))
        length=len(result)
        for one in result:
            self.sendLine("term|||"+str(one[0]))
#        self.sendLine("termend")
        self.sendCourse(result[length-2][0])
    def sendCourse(self,term):
        #发送课程
        result=sql.GetData("select * from Course where UserNumber="+str(self.student[1])+" and Term="+term)[0]
#        self.sendLine("coursetable")
#        self.send(str(result[2]))
#        self.sendLine("yeah")
#        self.sendLine("coursetable|||"+str(term)+"|||0|||")
#        self.transport.write(str(result[2]))
#        print result[2]
        self.send("coursetable|||"+str(term)+"|||1|||",str(result[3]))
    def sendFriendTerm(self,number):
        result=sql.GetData("select Term from Course where UserNumber="+str(number))
        for one in result:
            self.sendLine("friendterm|||"+str(one[0]))
#        self.sendLine("termend")
#        self.sendFriendCourse(result[length-2][0])
    def sendFriendCourse(self,number,term):
        #发送课程
        result=sql.GetData("select * from Course where UserNumber="+str(number)+" and Term="+str(term))[0]
#        self.sendLine("friendcoursetable")
        self.send("friendcoursetable|||"+str(number)+"|||"+str(term)+"|||",str(result[3]))
    #将新闻、课表等长的数据拆分发送     
    def send(self,cmd,str):
        print cmd
        print len(str)
        a=0
        while len(str)>self.LENGTH:
            e=cmd+str[0:self.LENGTH]
            str=str[self.LENGTH:]
            self.sendLine(e)
            a=a+1
            print a
            print e
        e=cmd+str
        self.sendLine(e)
        self.sendLine(cmd)
            

#-------------------
#    def checkNewsandMsg(self):
#        pass
#发送最新消息
    def sendMsg(self):
        result=sql.GetData("select * from Message where desnum='"+self.student[1]+"'")
        if not len(result)==0:
            for item in result:
                if item[3]=="2":
                    self.sendFriends()
                stu=sql.GetData("select * from User where UserNumber='"+item[1]+"'")
                for one in stu:
                    self.sendLine("friends|||add|||"+str(item[3])+"|||" +str(one[1])+"|||"+str(one[2])+"|||"+str(one[4])+"|||"+str(one[5]))
                    sql.Delete("Message", "desnum", self.student[1])
        else:
            print self.student[1]+"\tNo new message."
    #监听最新消息
    def listenMsg(self):
        if self.connected:
            self.sendMsg()
            reactor.callLater(10,self.listenMsg)
    def sendFriends(self):
        #发送好友列表
        result=sql.GetData("select * from Friend where UserNumber='"+self.student[1]+"'")
        length=len(result)
        if length !=0:
            for item in result:
                stu=sql.GetData("select * from User where UserNumber='"+item[2]+"'")[0]
                self.sendLine("friendlist|||"+str(stu[1])+"|||"+str(stu[2])+"|||"+str(stu[4])+"|||"+str(stu[5]))
        
    def inserFriend(self,number):
        #添加一条好友记录
        field=["UserNumber","FriendNumber"]
        values=[str(self.student[1]),str(number)]
        values1=[str(number),str(self.student[1])]
        if sql.GetCountMore("Friend", field,values)==0:
            sql.Insert("Friend", field, values)
        if sql.GetCountMore("Friend", field,values1)==0:
            sql.Insert("Friend",field,values1)
    #获取课表
    def grabCourse(self):
        CourseMain.GetCourseOfAready(self.student[1], self.student[3], "20112")
        CourseMain.GetCourseOfAready(self.student[1], self.student[3], "20112")
        self.sendTerm()
    #获取成绩
    def grabScore(self):
        CourseMain.GetStudentScore(self.student[1], self.student[3], "20112")
        CourseMain.GetStudentScore(self.student[1], self.student[3], "20112")
        
        
class IsapoucFactory(Factory):
    protocol=IsapoucProtocol
    def __init__(self,gui):
        #num=当前在线人数
        #users=当前在线人学号
        #ip=当前在线人ip
        self.num=0
        self.users=[]
        self.ip=[]
#        self.th=threadpool.ThreadPool()
#        self.th.start()
#        self.th.callInThread(self.grabNews)
#        threads.deferToThread(self.grabNews)
        self.gui=gui
    def grabNews(self):
#        try:
        print time.ctime()+"\t开始更新新闻"
        NewsMain.InsertJiaoWuChu()
        NewsMain.InsertSystemOfCourse()
        NewsMain.InsertGongCheng()
#        NewsMain.InsertGuanLi()
        NewsMain.InsertHaiHuan()
        NewsMain.InsertHaiSheng()
        NewsMain.InsertHuanKe()
        NewsMain.InsertJiJiao()
        NewsMain.InsertJingJi()
        NewsMain.InsertShiPin()
        NewsMain.InsertShuiChan()
        NewsMain.InsertShuXue()
#        NewsMain.InsertWaiYu()
        NewsMain.InsertWenXin()
        NewsMain.InsertYiShu()
        NewsMain.InsertYiYao()
        print time.ctime()+"\t新闻更新结束"
#        except Exception:
#            print time.ctime()+"\t"+"新闻抓取操作失败，60s后重试。"
#            print "错误类型："
#            print traceback.print_exc()
        reactor.callLater(60,self.grabNews)
             
if __name__=="__main__":
    factory=IsapoucFactory(0)
    #监听端口
    reactor.listenTCP(10000,factory)
    reactor.run()

        
