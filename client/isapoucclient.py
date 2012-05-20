# -*- coding: UTF-8 -*-
#客户端协议
from twisted.internet import reactor,defer,threads
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.protocols import basic
from user.SecFrame import ChildFrame 
import wx

class ProtocolofClient(basic.LineReceiver):
    def __init__(self):
        self.output=None
        #将从服务器发送过来的感兴趣的模块放至一个元组
        #索引：options[0]是jwcnews,options[1]是xknews,options[2]是facultynews；值：True代表显示此模块，False代表不显示
        self.options=[False, False, False,False,False,False]
        self.msg=[]
        self.defered=defer.Deferred()
        self.coursebuf=''
        self.fricoursebuf=''
        self.newsbuf=''


        
    def connectionMade(self):
        print "连接成功！"
        self.factory.logingui.protocol=self
        self.Login()
    def connectionLost(self,reason):
        if self.factory.ufgui!=None:
            parent=self.factory.ufgui
        elif self.factory.opgui!=None:
            parent=self.factory.opgui
        else:
            parent=self.factory.logingui
        dlg = wx.MessageDialog(parent, '失去连接，请重新登录。', 'Warnning', wx.OK|wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        reactor.stop()
        print "失去连接！"
        
    #用于发送内容
    def Send(self,str):
        self.transport.write(str)  
#    def dataReceived(self,data):
#        print data
         
#处理接收到的命令
    def lineReceived(self,data):
        information=data.split("|||")
#        print data
        #登录
        if information[0]=="login":
            if information[1]=="success" :
                #此处很复杂
                #self.factory.gui.TurntoOP()
                #self.factory.gui.protocol=self
                
                #学生属性
                self.number=information[2]
                self.name=information[3]
                self.major=information[4]
                self.grade=information[5]
            elif information[1]=="failure" and information[2]=="1":
                print "登陆失败，请检查用户名、密码、验证码是否正确。"
                self.factory.logingui.waitdlg.Destroy()
                self.factory.logingui.LoginError("登陆失败，请检查用户名、密码、验证码是否正确。")
                
            else :
                print "该用户已经在网页登录，请登出或稍后再试!"
                self.factory.logingui.waitdlg.Destroy()
                self.factory.logingui.LoginError("该用户已经在网页登录，请登出或稍后再试!")
                
                
        #获取选项设置
        if information[0]=="options":
            #设置选中的模块
            if information[2]=="1":
                self.options[0]=True
            else:
                self.options[0]=False
            if information[3]=="1":
                self.options[1]=True
            else:
                self.options[1]=False
            if information[4]=="1":
                self.options[2]=True
            else:
                self.options[2]=False
            #有谈窗提示
            if information[1]=="1":
                self.factory.logingui.TurntoOP()
            else:
                self.factory.logingui.TurntoUf()
            self.setOption()
        #好友
        if information[0]=="friendlist":
            self.factory.ufgui.insertOneFri([information[1],information[4],information[2],information[3]])
        if information[0]=="friends":            
            if information[1]=="search":
                if information[2]=="1":
                    self.factory.ufgui.Friendchoice()
                    self.factory.ufgui.dlg.lsInit([information[6],information[4],information[5],information[3]])
#                    dlg.inserlc
                else:
                    pass
                    self.factory.ufgui.showmsg("此学生不存在！")
            #添加
            if information[1]=="add":
            #设置提示按钮
                self.factory.ufgui.count=self.factory.ufgui.count+1
                self.factory.ufgui.TXButton.SetLabel(str(self.factory.ufgui.count))
                self.msg.append([information[6],information[5],information[4],information[3],information[2]])
                print self.msg
        if information[0]=="newspage":
            if information[2]=="16":
                if information[1]=="1":
                    self.factory.ufgui.nextpage2.Enable(False)
                self.factory.ufgui.pcount2=int(information[1])
                self.factory.ufgui.lblPageCount2.SetLabel(information[1])
                #教务处、
#                self.get10News("0","5")
                #开始监听
            elif information[2]=="15":
                if information[1]=="1":
                    self.factory.ufgui.nextpage.Enable(False)
                self.factory.ufgui.pcount=int(information[1])
                self.factory.ufgui.lblPageCount.SetLabel(information[1])
            else:
                if information[1]=="1":
                    self.factory.ufgui.nextpage1.Enable(False)
                self.factory.ufgui.pcount1=int(information[1])
                self.factory.ufgui.lblPageCount1.SetLabel(information[1])
        #新闻        
        if information[0]=="news":
            #选课系统新闻
            if information[3]=="16":
                a=self.factory.ufgui.newstree2.AppendItem(self.factory.ufgui.jwc0, information[2])    
                self.factory.ufgui.newstree2.SetItemText(a, information[1], 1)
                self.factory.ufgui.newstree2.Expand(self.factory.ufgui.jwc0)
            elif information[3]=="15":
                a=self.factory.ufgui.newstree.AppendItem(self.factory.ufgui.xk0, information[2])    
                self.factory.ufgui.newstree.SetItemText(a, information[1], 1)
                self.factory.ufgui.newstree.Expand(self.factory.ufgui.xk0)
            else:
                a=self.factory.ufgui.newstree1.AppendItem(self.factory.ufgui.fac0, information[2])    
                self.factory.ufgui.newstree1.SetItemText(a, information[1], 1)
                self.factory.ufgui.newstree1.Expand(self.factory.ufgui.fac0)
        #更新的新闻
        if information[0]=="newsupdated":
            if information[3]=="16":
                #插入至第一项
                a=self.factory.ufgui.newstree2.InsertItemBefore(self.factory.ufgui.jwc0, 0,information[2])    
                self.factory.ufgui.newstree2.SetItemText(a, information[1], 1)
                #删除最后一项
                lastitem,cookie=self.factory.ufgui.newstree2.GetLastChild(self.factory.ufgui.jwc0)
                self.factory.ufgui.newstree2.Delete(lastitem)
                self.factory.ufgui.Ontips()
            elif information[3]=="15":
                #插入至第一项
                a=self.factory.ufgui.newstree.InsertItemBefore(self.factory.ufgui.xk0, 0,information[2])    
                self.factory.ufgui.newstree.SetItemText(a, information[1], 1)
                #删除最后一项
                lastitem,cookie=self.factory.ufgui.newstree.GetLastChild(self.factory.ufgui.xk0)
                self.factory.ufgui.newstree.Delete(lastitem)
                self.factory.ufgui.Ontips()
            else:
                a=self.factory.ufgui.newstree1.InsertItemBefore(self.factory.ufgui.fac0, 0,information[2])    
                self.factory.ufgui.newstree1.SetItemText(a, information[1], 1)
                #删除最后一项
                lastitem,cookie=self.factory.ufgui.newstree1.GetLastChild(self.factory.ufgui.fac0)
                self.factory.ufgui.newstree1.Delete(lastitem)
                self.factory.ufgui.Ontips()
        #新闻内容
        if information[0]=="newscontent":
            if information[1]=='':
                self.factory.ufgui.cf.html.SetPage(self.newsbuf)
                self.newsbuf=''
            else:
                self.newsbuf=self.newsbuf+information[1]
#            self.setRawMode()
#            self.factory.ufgui.cf.html.SetPage(information[1])
        #表格形式的课程
        if information[0]=="term":
            self.factory.ufgui.authors.append(information[1])
            self.factory.ufgui.semester.AppendItems([information[1]])
#        if information[0]=="termend":
            
        if information[0]=="coursetable":
#            self.factory.ufgui.semester.SetStringSelection(information[1])
            if information[2]=="0":
#                print information
#                self.setRawMode()
                if information[3]=='':
                    self.factory.ufgui.courselist.SetPage(self.coursebuf)
#                    print self.coursebuf
                    self.coursebuf=''
                    self.factory.ufgui.semester.SetStringSelection(information[1])
                else:
                    self.coursebuf=self.coursebuf+information[3]
            else:
                if information[3]=='':
                    self.factory.ufgui.coursetable.SetPage(self.coursebuf)
                    self.coursebuf=''
                else:
                    self.coursebuf=self.coursebuf+information[3]
#            self.factory.ufgui.coursetable.SetPage(information[3])
#            if information[2]=="0":
#                self.factory.ufgui.courselist.SetPage(information[1])
#            else:
#                self.factory.ufgui.coursetable.SetPage(information[1])

        if information[0]=="friendterm":
            self.factory.ufgui.AddMenu(information[1])
            
        if information[0]=="friendcoursetable":
            if information[3]=='':
                self.factory.ufgui.fc.courselist.SetPage(self.fricoursebuf)
                self.fricoursebuf=''
            else:
                self.fricoursebuf=self.fricoursebuf+information[3]
#            self.setRawMode()
    def rawDataReceived(self,data):
#        information=data.split("|||")
        print data
#        self.setLineMode()
#        if information[0]=="newscontent":
#            self.factory.ufgui.cf.html.SetPage(information[1])
#            self.setLineMode("")
#        if information[0]=="coursetable":
#            self.factory.ufgui.semester.SetStringSelection(information[1])
#            self.factory.ufgui.courselist.SetPage(information[3])
#            length=len(information[0])+len(information[1])+len(information[2])+len(information[3])+12
#            data=data[length:]
#            print data
#            #print str
#            self.setLineMode(extra=data)
#            self.factory.ufgui.coursetable.SetPage(information[3])
#            self.setLineMode("")
#        if information[0]=="friendcoursetable":
#            self.factory.ufgui.fc.courselist.SetPage(information[3])
#            self.setLineMode("")
        self.factory.ufgui.courselist.SetPage(data)
        self.setLineMode()
                    
#----------------                
    def Login(self):
        login="login|||"+self.factory.logingui.UserName.GetValue()+"|||"+self.factory.logingui.Password.GetValue()
        self.sendLine(str(login))
    def Logout(self):
        #增加注销返回登录页面时间
        self.connectionLost("注销")
    def setOption(self):
        if not self.factory.opgui==None:
            self.factory.opgui.cb1.SetValue(self.options[0])
            self.factory.opgui.cb2.SetValue(self.options[1])
            self.factory.opgui.cb3.SetValue(self.options[2])
    #搜索好友        
    def searchFriendbyname(self,name):
        information="friends|||search|||"+name
        self.sendLine(information.encode("UTF-8"))
    #从搜索结果中添加好友（按照学号）
    def addFriend(self,number):
        information="friends|||add|||"+number+"|||"+self.number+"|||"+"4"
        self.sendLine(information.encode("UTF-8"))
    def sendresponsefriend(self,number,response):
        information="friends|||add|||"+number+"|||"+self.number+"|||"+response
        self.sendLine(str(information))
    #拉取好友
    def getFriends(self):
        self.sendLine("getfriends")
    def deleteFriend(self,number):
        self.sendLine("friends|||delete|||"+str(number)+"|||"+str(self.number))
    def getCourse(self,term):
        self.sendLine("getcourses|||"+str(term))
    def getTerm(self):
        self.sendLine("getterm")
    def getFriendTerm(self,number):
        self.sendLine("getfriendterm|||"+str(number))
    def getFriendCourse(self,number,term):
        self.sendLine("getfriendcourses|||"+str(number)+"|||"+str(term))
    def initPage(self):
        #初始化页面,得到页数后请求第一页新闻,此处factory.ufgui=None；得到学期后，获取最新学期课表
        self.sendLine("getnewspage|||16")
        self.sendLine("getnewspage|||15")
        self.sendLine("getnewspage|||1")
        self.getFriends()
        self.getTerm()
        self.sendLine("startlistening")
    def get10News(self,page,newsclass):
        self.sendLine("get10news|||"+page+"|||"+newsclass)
    def getNewsContent(self,id,newsclass):
        self.sendLine("getnewscontent|||"+id+"|||"+newsclass)
##------------
#    def getMsgandNews(self):
#        self.sendLine("message")
#        if self.factory.ufgui.pindex2==1:
#            item,cookie=self.factory.ufgui.newstree2.GetFirstChild(self.factory.ufgui.jwc0)
#            jwcid=self.factory.ufgui.newstree2.GetItemText(item,1)
#            if  jwcid != "":
#                self.sendLine("getnewsbyid|||"+str(jwcid)+"|||5")
#        xkid=self.factory.ufgui.newtree2.GetItemText(self.tree.GetFirstChild(self.factory.ufgui.jwc0))
#        self.sendLine("getnewsbyid|||"+jwcid+"|||5")
#        jwcid=self.factory.ufgui.newtree2.GetItemText(self.tree.GetFirstChild(self.factory.ufgui.jwc0))
#        self.sendLine("getnewsbyid|||"+jwcid+"|||5")
#        reactor.callLater(5,self.getMsgandNews)
        
class FactoryofClient(ClientFactory):
    def __init__(self,logingui):
        #将登录窗口嵌入协议
        self.logingui=logingui
        self.protocol=ProtocolofClient
        self.opgui=None
        self.ufgui=None
    def clientConnectionFailed(self, transport, reason):
        #添加连接失败处理
        self.logingui.waitdlg.Destroy()
        self.logingui.LoginError("连接失败,请检查网络。")
        print "连接失败！"


