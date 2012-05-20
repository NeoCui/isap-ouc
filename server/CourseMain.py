# -*- coding: UTF-8 -*-
'''
Created on 2012-2-29

@author: hlq
'''
import urllib,MySQLdb,actiontojwc2,re,SQLHelper,string
from BeautifulSoup import BeautifulSoup
import time,traceback
def InsertMajorClass(Account,Password,Term):
    atry=actiontojwc2.Tojwc()
    get=atry.trytoconnect(Account,Password,Term)
    if get==0:
        atry.getContents()  
        parser=atry.GetMajorHTML( "http://jwc.ouc.edu.cn:8080/ouc/SS010.do")
        content=actiontojwc2.GrabAllCourse(parser)
        #对有条件的查询等操作，要注意字符串中含有数字等情况，
        select="select * from CourseClass where ParentID='1' "
        result=SQLHelper.GetData(select)           
        actiontojwc2.InsertClass(result, content)
        atry.logout()
    else :
            print get       
#专业课
def GetAllMajorCourse(Account,Password,Term):
    InsertMajorClass(Account,Password,Term);
    atry=actiontojwc2.Tojwc()
    academic=""
    department=""
    sepicalty=""
    get=atry.trytoconnect(Account,Password,Term)
    if get==0:
        print time.ctime()+"\t"+"抓取所有专业课---学期:"+Term
        try:
            atry.getContents()   
            #获得专业课下的学院分类
            select="select * from CourseClass where ParentID=1"
            result=SQLHelper.GetData(select)
            
            for i in range(len(result)):
                academic=result[i][0]
                #获得学院下的系分类
                select1="select * from CourseClass where ParentID='"+result[i][0]+"'"
                result1=SQLHelper.GetData(select1)
                for j in range(len(result1)):
                    department=result1[j][0]
                    #获得系下的专业课分类
                    select2="select * from CourseClass where ParentID='"+result1[j][0]+"'"
                    result2=SQLHelper.GetData(select2)
                    for k in range(len(result2)):
                        se=str(result2[k][0])#专业课分类号
                        major=str(result2[k][1])#专业课名称
                        sepicalty=str(se[4:5])#获取selSepicalty_select 传递字段
                        #print sepicalty+"--"+se
                        #调用GetCourseGrade获取该专业课下的年级序列
                        grade=atry.GetCourseGrade(academic, department, sepicalty, "http://jwc.ouc.edu.cn:8080/ouc/SS010.do")
                        if len(grade)>0:
                            #print len(grade)                 
                            for m in range(len(grade)):
                                course=[];
                                html="";
                                #获取当前年级下的html内容
                                html=atry.GetMajorCourseContont(academic, department, sepicalty, str(grade[m]), "http://jwc.ouc.edu.cn:8080/ouc/SS010.do")
                                #抓取课程信息
                                course=actiontojwc2.GrabMajorCourse(html)
                                #判断课程信息序列是否为空序列，如果不为空的话就继续操作
                                if len(course)>0: 
                                    #print len(course)  
                                    #print "专业"+str(major)+str(grade[m])                        
                                    for h in range(len(course)):
                                        #for t in range(len(course[h])):
                                        #print str(len(course[h]))  
                                        #print str(course[h][t])
                                        #判断课程是否已经存在于数据库中
                                        ask=["CourseNumber","Grade"]
                                        answer=[str(course[h][0]),grade[m]]
                                        count=SQLHelper.GetCountMore("MajorCourse", ask,answer)
                                        if count==1:
                                            continue;
                                        else:       
                                            #如果不存在的话进行插入数据操作                                                                
                                            field=["CourseName","CourseNumber","ChooseNumber","TeacherName","CourseTime","XueShi","CourseScore","Money","SchoolHouse","PeopleNumber","Remark","Grade","Term","Academic"]
                                            value=[str(course[h][10]),str(course[h][0]),str(course[h][1]),str(course[h][2]),str(course[h][3]),str(course[h][4]),str(course[h][5]),str(course[h][6]),str(course[h][7]),str(course[h][8]),str(course[h][9]),str(grade[m]),Term,str(major)]                                     
                                            insert=SQLHelper.Insert("MajorCourse",field ,value)
                                            if insert==1:
                                                print time.ctime()+"\t"+"ok"
                                                continue
                                            else:
                                                print time.ctime()+"\t"+"wrong"     
            print time.ctime()+"\t"+"专业课抓取完成。"  
            atry.logout()
        except Exception:
            atry.logout()
            print traceback.print_exc()
            return 3
    else :
            print get
#通识限选课 --1
def GetAllLimitCourse(Account,Password,Term):
    atry=actiontojwc2.Tojwc()
    get=atry.trytoconnect(Account,Password,Term)
    if get==0:
        try:
            print time.ctime()+"\t"+"抓取通识限选课---学期："+Term
            atry.getContents()
    #        Term="20111"
            m=0
            for i in range(2):
                if i==0:
                    m=0
                else:
                    m=2
            #for j in range(len(academic)):      
                #print str(m)      
                CourseOne=atry.GetLimitCourse(str(m), "http://jwc.ouc.edu.cn:8080/ouc/SS011.do")
                #print CourseOne
                coursemore=actiontojwc2.GrabLimitCourse(CourseOne)
                #print str(coursemore[k][0])
                for k in range(len(coursemore)):
                    ask=["CourseNumber","SchoolHouse","Term"]
                    answer=[str(coursemore[k][0]),str(m),Term]   
                    count=SQLHelper.GetCountMore("AllCourse", ask, answer)
                    if count>0:
                        continue;
                    else:
                    #print str(coursemore[k][9])
                        field=["CourseName","CourseNumber","TeacherName","CourseTime","XueShi","CourseScore","Money","PeopleNumber","Remark","SchoolHouse","Term","Academic","CourseType"]
                        value=[str(coursemore[k][9]),str(coursemore[k][0]),str(coursemore[k][1]),str(coursemore[k][2]),str(coursemore[k][3]),str(coursemore[k][4]),str(coursemore[k][7]),str(coursemore[k][6]),str(coursemore[k][8]),str(m),Term,str(coursemore[k][5]),"1"]
                        insert=SQLHelper.Insert("AllCourse",field ,value)
                        if insert==1:
                            continue
                        else:
                            print "通识限选课抓取错误。"
            print time.ctime()+"\t"+"通识限选课抓取完成。"       
            atry.logout()
        except Exception:
            atry.logout()
            print traceback.print_exc()
            return 3
    else :
        if get==1:
            print "登陆失败，请检查用户名、密码是否正确。"
        if get==2:
            print "该用户已经登录，请登出或稍后再试!"
#通识必修课 --0
def GetBiXiuCourse(Account,Password,Term):
    atry=actiontojwc2.Tojwc()
    get=atry.trytoconnect(Account,Password,Term)
    if get==0:
        try:
            print time.ctime()+"\t"+"抓取通识必修课---学期："+Term
            atry.getContents()
            academic=atry.GetAcademic("http://jwc.ouc.edu.cn:8080/ouc/SS013.do")
    #        term="20111"
            number=len(academic[0])
        #print str(academic[0][0]),str(academic[0][2])       
            m=0
            for i in range(2):
                if i==0:
                    m=0
                else:
                    m=2
                for j in range(len(academic)):            
                    CourseOne=atry.GetAllCourse(str(academic[j][0]), str(academic[j][2]), str(m), "http://jwc.ouc.edu.cn:8080/ouc/SS013.do")
                #print CourseOne
                    coursemore=actiontojwc2.GrabCourse(CourseOne)
                    for k in range(len(coursemore)):
                        ask=["CourseNumber","SchoolHouse","Term"]
                        answer=[str(coursemore[k][0]),str(m),Term]   
                        count=SQLHelper.GetCountMore("AllCourse", ask, answer)
                    #count=SQLHelper.GetCountOne("AllCourse", "CourseNumber", str(coursemore[k][0]))
                    #print count
                        if count>0:
                            continue;
                        else:
                            field=["CourseName","CourseNumber","CourseTime","XueShi","CourseScore","Money","TeacherName","PeopleNumber","Remark","SchoolHouse","Term","Academic","CourseType"]
                            value=[str(academic[j][3]),str(coursemore[k][0]),str(coursemore[k][1]),str(coursemore[k][2]),str(coursemore[k][3]),str(coursemore[k][4]),str(coursemore[k][5]),str(coursemore[k][6]),str(coursemore[k][7]),str(m),Term,str(academic[j][1]),"0"]
                            insert=SQLHelper.Insert("AllCourse",field ,value)
                            if insert==1:
                                continue
                            else:
                                print "通识必修课抓取错误。"
            print time.ctime()+"\t"+"通识必修课抓取完成。"
            atry.logout()
        except Exception:
            atry.logout()
            print traceback.print_exc()
            return 3
    else :
        if get==1:
            print "登陆失败，请检查用户名、密码是否正确。"
        if get==2:
            print "该用户已经登录，请登出或稍后再试!"
def GetStudentScore(Account,Password,Term):
    atry=actiontojwc2.Tojwc()
#    zhanghao="020252009012";
    get=atry.trytoconnect(Account,Password,Term)
    if get==0:
        try:
            print time.ctime()+"\t"+"抓取学生成绩---学号:"+Account
            atry.getContents()
            parser=atry.GetScore("http://jwc.ouc.edu.cn:8080/ouc/SS018.do")
            #name=parser.findAll('p')#border  属性唯一
            number=parser.findAll('font')#number[3]为个人及格分数
            chengji=parser.findAll('table',align="center")#center属性唯一
            count=SQLHelper.GetCountOne("Mark", "UserID", Account);
            if count==0:
                field=["UserID","PassScore","MarkContent"]
                #MySQLdb.escape_string()参数必须是string类型的
                value=[Account,MySQLdb.escape_string(str(number[3])),MySQLdb.escape_string(str(chengji[0]))]
                insert=SQLHelper.Insert("Mark", field, value)
                if insert==1:
                    print time.ctime()+"\t成绩---"+Account+"---Insert OK"
                else:
                    print "插入个人成绩出现程序上的错误，请检查！！"
            else:
                fields=["PassScore","MarkContent"]
                values=[MySQLdb.escape_string(str(number[3])),MySQLdb.escape_string(str(chengji[0]))]
                update=SQLHelper.Update("Mark", fields, values, "UserID", Account)
                if update==1:
                    print time.ctime()+"\t成绩---"+Account+"---Update OK"
                else:
                    print "插入个人成绩出现程序上的错误，请检查！！"
            atry.logout() 
            print time.ctime()+"\t"+"学生成绩更新完成。"   
        except Exception:
            atry.logout()
            print traceback.print_exc()
            return 3
    else :
        if get==1:
            print time.ctime()+"\t成绩---"+Account+"登陆失败，请检查用户名、密码是否正确。"
        if get==2:
            print time.ctime()+"\t成绩---"+Account+"该用户已经登录，请登出或稍后再试!"
def GetCourseOfAready(Account,Password,Term):
    atry=actiontojwc2.Tojwc()
#    zhanghao="020252009009";
#    Term="20111"
    get=atry.trytoconnect(Account,Password,Term)
    if get==0:
        try:
            print time.ctime()+"\t"+"抓取已选课程---学号："+Account
            atry.getContents()
            parser=atry.GetAlreadyCourse("http://jwc.ouc.edu.cn:8080/ouc/SS020.do") 
            option=parser('option')#抓取option数量
            #判断信息中是否含有
            if len(option)>0:        
                for i in range(len(option)):
                    termChoice=""#课程学期
                    termChoice=str(parser('option')[i]['value'])
                    if termChoice>"2009"+"0":
                        html=atry.GetAreadyCourseContent(termChoice, "http://jwc.ouc.edu.cn:8080/ouc/SS020.do")
                        course=html.findAll('table',width="100%")
                        #print str(course[3]),str(course[4])
                        ask=["UserNumber","Term"]
                        answer=[Account,termChoice]
                        count=SQLHelper.GetCountMore("Course", ask, answer);
                        #count=0代表第一次插入已选课程
                        if count==0:
                            field=["UserNumber","CourseContent","Curriculum","Term"]
                            #MySQLdb.escape_string()参数必须是string类型的
                            # str(course[3])为已选课程的详细信息,str(course[4])为已选课程的表哥形式
                            value=[Account,MySQLdb.escape_string(str(course[3])),MySQLdb.escape_string(str(course[4])),termChoice]
                            insert=SQLHelper.Insert("Course", field, value)
                            if insert==1:
                                print time.ctime()+"\t成绩---"+Account+"---Insert OK"
                            else:
                                print "插入个人课表出现程序上的错误，请检查！！"
                        else:
                            fields=["CourseContent","Curriculum"]
                            values=[MySQLdb.escape_string(str(course[3])),MySQLdb.escape_string(str(course[4]))]
                            ask=["UserNumber","Term"]
                            answer=[Account,termChoice]
                            update=SQLHelper.UpdateMore("Course", fields, values, ask, answer)
                            if update==1:
                                print time.ctime()+"\t课表---"+Account+"---Update OK"
                                
                            else:
                                print "插入个人课表出现程序上的错误，请检查！！"
            atry.logout()
            print   time.ctime()+"\t"+"学生课表更新完成。"
        except Exception:
            atry.logout()
            print traceback.print_exc()
            return 3
    else :
        if get==1:
            print time.ctime()+"\t课表---"+Account+"登陆失败，请检查用户名、密码是否正确。"
        if get==2:
            print time.ctime()+"\t课表---"+Account+"该用户已经登录，请登出或稍后再试!"
def AnalyzeChoiceCourse(Account,Password,Term): 
    atry=actiontojwc2.Tojwc()
    get=atry.trytoconnect(Account,Password,Term)
    if get==0:
        atry.getContents()
        parser=atry.GetStudentChooseCourse("http://jwc.ouc.edu.cn:8080/ouc/SS003.do")
        p=re.compile("\<span\>\d\d\d\d\d\d\d\<br \/>\<\/span\>")
        number=parser('span')
        for i in range(len(number)):
            coursenumber=p.findall(str(number[i]))
            if len(coursenumber)>0:
                courseNumber=str(coursenumber[0])[6:len(coursenumber)-14];
#            data0=SQLHelper.GetData("select * from MajorCourse where ChooseNumber='"+courseNumber+"' and Term='"+Term+"'")
#            print courseNumber
#            
#            majorID=None;
#            pNumber=None;
#            if len(data0)>0:
##                for k in range(len(data0[0])):
##                    print str(data0[0][k])
#                majorID=string.atoi(str(data0[0][0]))
#                pNumber=string.atoi(str(data0[0][10]))
#            else:
#                data1=SQLHelper.GetData("select * from AllCourse where CourseNumber='"+courseNumber+"' and Term='"+Term+"'")
#                if len(data1)>0:
##                    for l in range(len(data1[0])):
##                   
##                        print str(data1[0][l])                   
#                    majorID=string.atoi(str(data1[0][0]))
#                    pNumber=string.atoi(str(data1[0][8]))
#                else:
#                    print "课程号为："+courseNumber+"不存在！！"
##            print majorID,pNumber
                ask=["MajorID","Account","Term"]
                answer=[courseNumber,Account,Term]
                count=SQLHelper.GetCountMore("CourseAnalysis", ask, answer);
            #count=0表中没有该课程的任何信息
                if count==0:
                    field=["MajorID","Account","Term"]
#                #MySQLdb.escape_string()参数必须是string类型的
#                # str(course[3])为已选课程的详细信息,str(course[4])为已选课程的表哥形式
                    value=[courseNumber,Account,Term]
#                for j in range(len(value)):                               
#                    print str(value[j]),type(value[j])               
                    insert=SQLHelper.Insert("CourseAnalysis",field,value)
                    if insert==1:
                        print "OK"
                    else:
                        print "插入选课分析表出现程序上的错误，请检查！！"
                         
        atry.logout()
    else :
        print get
#main函数   
if __name__=="__main__":
    GetAllMajorCourse("020252009009","toland1222","20112");
    #GetAllLimitCourse("020252009009","toland1222","20112")
    #GetBiXiuCourse("020252009009","toland1222","20112")
    #GetStudentScore("020252009009","toland1222","20112")
    #GetCourseOfAready("020252009009","toland1222","20112")
        