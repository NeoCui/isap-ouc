# -*- coding: UTF-8 -*-
#import GrabNews as grab
import CourseMain as cs
#import SQLHelper as sql
#import time
#while True:    
#    grab.InsertDB("http://jwc.ouc.edu.cn:8080/jwwz/index.jsp")
#    time.sleep(10)
#grab.InsertDB("http://jwc.ouc.edu.cn:8080/jwwz/index.jsp")
#cs.GetCourseOfAready("020252009013", "901221", "20112")
#a=[]
#a=sql.GetData("SELECT * FROM News where NewsClassID=5 order by id desc LIMIT 0,10 ")
##b=sorted(a, key=lambda a:a[3])
#for one in a:
#    print one[1]
#sql.Insert("Friend", ["UserNumber","FriendNumber"], ["2","3"])
#print sql.GetData("SELECT Term FROM Course where UserNumber=020252009012")
from twisted.internet import  reactor,defer,threads
import time
#    
def run():
    d=threads.deferToThread(cs.GetCourseOfAready,"020252009009", "toland1222", "20112")
    print "write"
    time.sleep(2)
    print "fuck"
if __name__=="__main__":
    run()
    reactor.run()
#import traceback,time
#def a():
#    try:
#        print 2+"3"
#    except Exception,data :
#        print data
#        print traceback.print_exc()
#        return 3
#    print "uuu"
#if __name__=="__main__":
#    while a()==3:
#        time.sleep(10)
#def test():
#    print "start"
#    time.sleep(5)
#if __name__=="__main__":
#    test()
#    print "1"
#    reactor.callLater(2,test)
#    reactor.run()