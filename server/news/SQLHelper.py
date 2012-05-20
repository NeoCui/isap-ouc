#-*- coding:utf-8 -*-
'''
Created on 2011-11-8
数据库操作类
@author: hlq
'''
import MySQLdb
#验证数据库中是否包含该条信息，返回是一个int型的行数，TnablName，ask，answer都为字符串类型
#多线程操作不能共用一个数据库连接，所以在import的时候连接数据库，而应该在每次调用的时候打开连接，调用结束关闭连接
connectionstring="'localhost','root','1234','isapouc'"
def GetCountOne(TableName,ask,answer):
    #数据库链接字符串
    db=MySQLdb.connect(host='localhost',user='root',passwd='1234',db='isapouc',charset="utf8")
    cur=db.cursor()#使用连接对象获得一个cursor对象
    #先判断数据是否为空，如果为空的话，打印出相应的信息，防止程序抛出相应的异常
    if TableName=="":
        print "参数数据表名称为空"
        return 0
    elif ask=="":
        print "传递条件参数为空，程序错误"
        return 0
    elif answer=="":
        print "传递条件参数为空，程序错误"
        return 0
    else:
        #执行相应的查询命令
        #print "select * from "+TableName+" where "+ask+"='"+answer+"'" #测试是使用的
        #补充一点，在这里=号后面必须加单引号，单引号解析为字符串值，双引号解析为字段名称，切记切记
        count=cur.execute("select * from "+TableName+" where "+ask+"='"+answer+"'")
        #count=cur.execute("select * from "+TableName+" where Name='hlq'")
    #cur.close()
    #db.close()
    return count
#验证数据库中是否包含该条信息，返回是一个int型的行数（查询条件为多项，由and连接）
#TableName为字符串类型，ask，answer，为list类型
def GetCountMore(TableName,ask,answer):
    #数据库链接字符串
    db=MySQLdb.connect(host='localhost',user='root',passwd='1234',db='isapouc',charset="utf8")
    cur=db.cursor()
    n=len(ask)
    m=len(answer)
    result=""
    if TableName=="":
        print "参数数据表名称为空"
        return 0
    else:
        if n==0:
            print "传递条件参数为空，程序错误"
            return 0
        elif m==0:
            print "传递条件参数为空，程序错误"
            return 0
        else:
            if n==m:#n和m必须相等，否则对应的条件无法成立
                for i in range(n):
                    if i==n-1:#迭代到最后一项，不能添加and链接
                        result=result+" "+str(ask[i])+"="+"'"+str(answer[i])+"'"
                        #print result
                    else:
                        result=result+" "+str(ask[i])+"='"+str(answer[i])+"' and"  
                        #print result         
                count=cur.execute("select * from "+TableName+" where "+result+"")
                #print "select * from "+TableName+" where "+result+""
            else:
                print "传递条件参数无法互相对应，程序错误"
                return 0
    #cur.close()
    #db.close()
    return count
#插入数据库函数，表名，插入的表中字段名，插入的数据，
#Field和Values都是list类型，TableName为字符串类型
def Insert(TableName,Field,Values):   
    #数据库链接字符串
    db=MySQLdb.connect(host='localhost',user='root',passwd='1234',db='isapouc',charset="utf8")
    f=""
    t="" 
    k=0
    n=len(Field)    
    m=len(Values)
    if TableName=="":
        print "参数数据表名称为空"
        return 0
    elif n==0:
        print "传递条件参数为空，程序错误"
        return 0
    elif m==0:
        print "传递条件参数为空，程序错误"        
        return 0
    elif n==m:
        for j in range(n):
            if j==n-1:#迭代到最后一项，不能添加逗号
                f=f+Field[j]#将表中字段名链接起来
                type1=type(Values[j])
                if str(type1)=="<type 'str'>":#判断来自Values的数据类型，好写出插入的数据类型字符串
                    t=t+"%s"
                else:
                    t=t+"%d"
            
            else:
                f=f+Field[j]+","
                type2=type(Values[j])#同上解释，这个是需要加逗号的
                if str(type2)=="<type 'str'>":
                    t=t+"%s"+","
                else:
                    t=t+"%d"+","    
            #print t,j,type2                                              
            #print len(MySQLdb.escape_string(information[i][2]))
        cur=db.cursor()
            #执行插入语句
        #print "insert into "+TableName+"("+f+") values("+t+")"
            
        count=cur.execute("insert into "+TableName+"("+f+") values("+t+")", Values)
        #        count=cur.execute("insert into CourseAnalysis(RealNumber,Account,Term,PeopleNumber,MajorID) values(%s,%s,%s,%s,%d)",["1","2","3","4",5])
        #print "OK"    
        if count==1:
            k=1
        else:
            k=0
        cur.close()
        db.commit()
        return k
    else:
        print "传递条件参数无法互相对应，程序错误"
        return 0
    #提交时间，没有这个函数，数据无法正常提交
    db.close()
#插入数据库函数，表名，插入的表中字段名，插入的数据，
#Field和Values都是list类型，TableName为字符串类型，Values里中含有多项list，即多条插入
#多项list插入
def InsertMore(TableName,Field,Values):
    #数据库链接字符串
    db=MySQLdb.connect(host='localhost',user='root',passwd='1234',db='isapouc',charset="utf8")
    n=len(Field)    
    m=len(Values)
    f=""
    t=""
    if TableName=="":
        print "参数数据表名称为空"
        return 0
    elif n==0:
        print "传递条件参数为空，程序错误"
        return 0
    elif m==0:
        print "传递条件参数为空，程序错误"
        return 0        
    
    else:
        for j in range(n):
            type0="<type 'str'>"
            if j==n-1:
                f=f+Field[j]
                type1=type(Values[0][j])
                if str(type1)==type0:
                    t=t+"%s"
                    
                else:
                    t=t+"%d"
            
            else:
                f=f+Field[j]+","
                type2=type(Values[0][j])
                if str(type2)==type0:
                    t=t+"%s"+","                    
                else:
                    t=t+"%d"+","                            
        #print t,f
            
        for i in range(m):
            
            #print len(MySQLdb.escape_string(information[i][2]))
            cur=db.cursor()
            cur.execute("insert into "+TableName+"("+f+") values("+t+")", Values[i])
            #print "OK"
            
            cur.close()
            db.commit()
        return 1    
    
    db.close()
def  Delete(TableName,ask,answer):
    #数据库链接字符串
    db=MySQLdb.connect(host='localhost',user='root',passwd='1234',db='isapouc',charset="utf8")
    m=0
    cur=db.cursor()#使用连接对象获得一个cursor对象
    #先判断数据是否为空，如果为空的话，打印出相应的信息，防止程序抛出相应的异常
    if TableName=="":
        print "参数数据表名称为空"
        return 0#"0"代表失败
    elif ask=="":
        print "传递条件参数为空，程序错误"
        return 0
    elif answer=="":
        print "传递条件参数为空，程序错误"
        return 0
    else:
        #执行相应的删除命令
       
        #补充一点，在这里=号后面必须加单引号，单引号解析为字符串值，双引号解析为字段名称，切记切记
        #print "delete * from "+TableName+" where "+ask+"='"+answer+"'"
        n=cur.execute("delete from "+TableName+" where "+ask+"='"+answer+"'")
        if n==1:
            m=1;
        else:
            m=0
        #count=cur.execute("select * from "+TableName+" where Name='hlq'")
        db.commit()
        return m
    cur.close()
    
    db.close()
    
def Update(TableName,Field,Values,ask,answer):
    #数据库链接字符串
    db=MySQLdb.connect(host='localhost',user='root',passwd='1234',db='isapouc',charset="utf8")
    f=""
     
    n=len(Field)    
    m=len(Values)
    if TableName=="":
        print "参数数据表名称为空"
        return 0
    elif n==0:
        print "传递条件参数为空，程序错误"
        return 0
    elif m==0:
        print "传递条件参数为空，程序错误"
        return 0        
    elif len(ask)==0:
        print "传递条件参数为空，程序错误"
        return 0
    elif len(answer)==0:
        print "传递条件参数为空，程序错误"
        return 0
    elif n==m:
        for j in range(n):
            if j==n-1:#迭代到最后一项，不能添加逗号
                f=f+Field[j]+"="+"'"+Values[j]+"'"#将表中字段名链接起来                           
            else:
                f=f+Field[j]+"="+"'"+Values[j]+"'"+","                                
                                                        
        #print f
        cur=db.cursor()
            #执行插入语句
        
        cur.execute("update "+TableName+" set "+f+" where "+ask+"='"+answer+"'")
        #print "OK"    
        cur.close()
        db.commit() #提交时间，没有这个函数，数据无法正常提交
        return 1
    else:
        print "传递条件参数无法互相对应，程序错误"
        return 0
   
    db.close()
def UpdateMore(TableName,Field,Values,ask,answer):
    #数据库链接字符串
    db=MySQLdb.connect(host='localhost',user='root',passwd='1234',db='isapouc',charset="utf8")
    f=""    
    result=""
    n=len(Field)    
    m=len(Values)
    nn=len(ask)
    mm=len(answer)
    if TableName=="":
        print "参数数据表名称为空"
        return 0
    elif n==0:
        print "传递条件参数为空，程序错误"
        return 0
    elif m==0:
        print "传递条件参数为空，程序错误"
        return 0        
    elif len(ask)==0:
        print "传递条件参数为空，程序错误"
        return 0
    elif len(answer)==0:
        print "传递条件参数为空，程序错误"
        return 0
    elif n==m:
        if nn==mm:            
            for j in range(n):
                if j==n-1:#迭代到最后一项，不能添加逗号
                    f=f+Field[j]+"="+"'"+Values[j]+"'"#将表中字段名链接起来                           
                else:
                    f=f+Field[j]+"="+"'"+Values[j]+"'"+","                                
            for i in range(n):
                    if i==nn-1:#迭代到最后一项，不能添加and链接
                        result=result+" "+str(ask[i])+"="+"'"+str(answer[i])+"'"
                        #print result
                    else:
                        result=result+" "+str(ask[i])+"='"+str(answer[i])+"' and"   
        else:
            print "传递条件参数无法互相对应，程序错误"                                                       
        #print f
        cur=db.cursor()
            #执行插入语句       
        cur.execute("update "+TableName+" set "+f+" where "+result+"")
        #print "OK"    
        cur.close()
        db.commit() #提交时间，没有这个函数，数据无法正常提交
        return 1
    else:
        print "传递条件参数无法互相对应，程序错误"
        return 0
   
    db.close()
#ask 为所要获取信息的select语句，GetData()函数返回的是一个元组类型
def GetData(ask):   
    #数据库链接字符串
    db=MySQLdb.connect(host='localhost',user='root',passwd='1234',db='isapouc',charset="utf8")
    cur=db.cursor()
    cur.execute(ask)
    result=cur.fetchall()
#    cur.close()
#
#    cur.close()
    #db.close()
    return result
def GetDataByMore(TableName,ask,answer):
    #数据库链接字符串
    db=MySQLdb.connect('localhost','root','1234','isapouc')
    cur=db.cursor()
    n=len(ask)
    m=len(answer)
    result=""
    if TableName=="":
        print "参数数据表名称为空"
        return 0
    else:
        if n==0:
            print "传递条件参数为空，程序错误"
            return 0
        elif m==0:
            print "传递条件参数为空，程序错误"
            return 0
        else:
            if n==m:#n和m必须相等，否则对应的条件无法成立
                for i in range(n):
                    if i==n-1:#迭代到最后一项，不能添加and链接
                        result=result+" "+str(ask[i])+"="+"'"+str(answer[i])+"'"
                        #print result
                    else:
                        result=result+" "+str(ask[i])+"='"+str(answer[i])+"' and"  
                        #print result         
                cur.execute("select * from "+TableName+" where "+result+"")
                count=cur.fetchall()
                return count
                #print "select * from "+TableName+" where "+result+""
            else:
                print "传递条件参数无法互相对应，程序错误"
def InsertAboutNumber(number):    
    #数据库链接字符串
    db=MySQLdb.connect(host='localhost',user='root',passwd='1234',db='isapouc',charset="utf8")
    cur=db.cursor()                         
    count=cur.execute(number)
       
    if count==1:
        k=1
    else:
        k=0
    cur.close()
    db.commit()
    return k
    db.close()
    
