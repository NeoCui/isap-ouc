# -*- coding: UTF-8 -*-
'''
Created on 2012-3-20

@author: hlq
'''
import urllib,MySQLdb,re
import SQLHelper
import haihuan,haisheng,ShiPin,gongcheng,guanli,WaiYu,ShuiChan,YiYao,HuanKe,JingJi,WenXin,ShuXue,JiJiao,YiShu
import SystemOfCourse,JwcNews,time
from BeautifulSoup import BeautifulSoup
#海洋环境学院信息插入
def InsertHaiHuan():
    try:
        content=haihuan.GetByHaiHuan("http://www2.ouc.edu.cn/cpeo/index.asp");
        length=len(content);
        if length<=0:
            print time.ctime()+"\t"+"海洋环境学院\t暂无更新"
        else:
            for i in range(length):
                Insert(content[i][0],MySQLdb.escape_string(content[i][1]),content[i][2],"海洋环境学院",1)
            print time.ctime()+"\t海洋环境学院新闻更新数目:"+str(length)
    except :
        print time.ctime()+"\t海洋环境学院更新连接超时。"                  
#将海洋生命学院信息存储到数据库中，引用了srdpPage文档 
def InsertHaiSheng():   
    try:
        update=0;
        url=[["重要通知","http://www2.ouc.edu.cn/hysm/list.asp?class=4"],["院系新闻","http://www2.ouc.edu.cn/hysm/list.asp?class=3"],["学生工作","http://www2.ouc.edu.cn/hysm/list.asp?class=23"] ]
        for i in range(len(url)):
            content=haisheng.GetByHaiSheng(url[i][1]);
            length=len(content);
            #print length
            if length<=0:
                update=update+1;
            else:          
                for j in range(length):
                    #print content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1]
                    Insert(content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1],"海洋生命学院",2)
                print time.ctime()+"\t海洋环境学院新闻更新数目:"+str(length)
        if update==3:
            print time.ctime()+"\t"+"海洋生命学院\t暂无更新"
    except :
        print time.ctime()+"\t海洋生命学院更新连接超时。"  
#将食品科学与工程学院信息存储到数据库中，引用了srdpPage文档 
def InsertShiPin():  
    try: 
        update=0;
        url=[["最新动态","http://www2.ouc.edu.cn/shipin/nylist.asp?id=6&lb1id=5"],["学生工作通知","http://www2.ouc.edu.cn/shipin/nylist.asp?id=6&lb1id=7"],["学生活动集锦","http://www2.ouc.edu.cn/shipin/nylist.asp?id=6&lb1id=8"],["通知公告","http://www2.ouc.edu.cn/shipin/nylist.asp?id=6&lb1id=6"],["就业信息","http://www2.ouc.edu.cn/shipin/nylist.asp?id=6&lb1id=73"] ]
        for i in range(len(url)):
            content=ShiPin.GetByShiPin(url[i][1]);
            length=len(content);
            #print length
            if length<=0:
                update=update+1;
            else:          
                for j in range(length):
                    #print content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1]
                    Insert(content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1],"食品科学与工程学院",3)
                print time.ctime()+"\t食品科学与工程学院新闻更新数目:"+str(length)
        if update==5:
            print time.ctime()+"\t食品科学与工程学院\t暂无更新"      
    except  :
        print time.ctime()+"\t食品学院更新连接超时。"          
#将工程学院信息存储到数据库中,引用了srdpPage文档 
def InsertGongCheng():  
    try: 
        update=0;
        url=[["学院新闻","http://www3.ouc.edu.cn/gongcheng/ShowNoticeList.aspx?id=1"],["学院通知","http://www3.ouc.edu.cn/gongcheng/ShowNoticeList.aspx?id=2"],["学生活动通知","http://www3.ouc.edu.cn/gongcheng/ShowArticleList.aspx?id=32"],["学生活动新闻","http://www3.ouc.edu.cn/gongcheng/ShowArticleList.aspx?id=33"],["毕业生工作通知","http://www3.ouc.edu.cn/gongcheng/ShowArticleList.aspx?id=38"] ,["毕业生招聘信息","http://www3.ouc.edu.cn/gongcheng/ShowArticleList.aspx?id=39"] ,["毕业生就业指导","http://www3.ouc.edu.cn/gongcheng/ShowArticleList.aspx?id=40"] ,["资助公示","http://www3.ouc.edu.cn/gongcheng/ShowArticleList.aspx?id=42"] ,["资助工作通知","http://www3.ouc.edu.cn/gongcheng/ShowArticleList.aspx?id=43"] ]
        for i in range(len(url)):
            if str(url[i][0])=="学院通知":           
                content=gongcheng.GetByGongCheng(url[i][1]);
            else:
                content=gongcheng.GetByGongCheng2(url[i][1]);
            length=len(content);
            #print length
            if length<=0:
                update=update+1;
            else:          
                for j in range(length):
                    #print content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1]
                    Insert(content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1],"工程学院",4)
                print time.ctime()+"\t工程学院新闻更新数目:"+str(length)
        if update==9:
            print time.ctime()+"\t工程学院暂\t无更新"            
    except  :
        print time.ctime()+"\t工程学院更新连接超时。"     
#将管理学院信息存储到数据库中,引用了srdpPage文档 
def InsertGuanLi():   
    try:
        update=0;
        url=[["最新动态左","http://www2.ouc.edu.cn/glxy/Article/zuixindongtai/"],["最新动态右","http://www2.ouc.edu.cn/glxy/Article/zuixindongtai2/"],["学院工作","http://www2.ouc.edu.cn/glxy/Article/ShowClass.asp?ClassID=24"],["学生工作","http://www2.ouc.edu.cn/glxy/Article/ShowClass.asp?ClassID=25"],["本科生教学工作","http://www2.ouc.edu.cn/glxy/Article/ShowClass.asp?ClassID=58"] ,["研究生教学工作","http://www2.ouc.edu.cn/glxy/Article/ShowClass.asp?ClassID=62"] ,["毕业生工作","http://www2.ouc.edu.cn/glxy/Article/deyugongzuo/biyeshenggongzuo/"] ]
        for i in range(len(url)):
            content=guanli.GetByGuanLi(url[i][1]);
            length=len(content);
            #print length
            if length<=0:
                update=update+1;
            else:          
                for j in range(length):
                    #print content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1]
                    Insert(content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1],"管理学院",5)
                print time.ctime()+"\t管理学院新闻更新数目:"+str(length)
        if update==7:
            print time.ctime()+"\t管理学院\t暂无更新";     
    except  :
        print time.ctime()+"\t管理学院更新连接超时。"  
#外语学院信息插入到数据库中              
def InsertWaiYu():    
    try:
        update=0;
        url=[["首页","http://222.195.158.203/index.aspx"],["最新动态","http://222.195.158.203/index.aspx?menuid=8&type=article&lanmuid=303&language=cn"],["工作通知","http://222.195.158.203/index.aspx?menuid=8&type=article&lanmuid=323&language=cn"],["就业信息","http://222.195.158.203/index.aspx?menuid=8&type=article&lanmuid=310&language=cn"] ]
        for i in range(len(url)):
            content=WaiYu.GetByWYShouYe(url[i][1]);
            length=len(content);
            #print length
            if length<=0:
                update=update+1;
            else:          
                for j in range(length):
                    #print content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1]
                    Insert(content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1],"外语学院",6)
                print time.ctime()+"\t外语学院新闻更新数目:"+str(length)
        if update==4:
            print time.ctime()+"\t外语学院\t暂无更新";     
    except  :
        print time.ctime()+"\t外语学院更新连接超时。"  
#法政学院，编号为7，暂时不写    ，信院也没有写，排在之后，海洋地球科学学院 
#水产学院
def InsertShuiChan():
    try:
        update=0;
        url=[["1","学院要闻"],["59","学院通知"],["2","党团工作"],["3","本科生教育"],["63","研究生培养"],["65","就业工作"],["66","学术交流"],["67","水漾年华"],["68","星空"] ]
        for i in range(len(url)):
            content=ShuiChan.GetByShuiChan("http://www2.ouc.edu.cn/shuichan/Article_Class2.asp?ClassID="+url[i][0]);
            length=len(content);
            #print length
            if length<=0:
                update=update+1;
            else:          
                for j in range(length):
                    try:
                    #print content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1]
                        Insert(content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1],"水产学院",7)
                    except  :
                        pass
                print time.ctime()+"\t水产学院新闻更新数目:"+str(length)
        if update==9:
            print time.ctime()+"\t水产学院\t暂无更新"    
    except  :
        print time.ctime()+"\t水产学院更新连接超时。"  
#医药学院      
def InsertYiYao():
    try:
        update=0;
        url=[["more3.htm","学院要闻"],["more4.htm","学院通知"],["more6.htm","学院工作"],["more7.htm","本科生教育"],["more8.htm","研究生教育"],["more9.htm","科学研究"],["more10.htm","学术交流"],["more11.htm","学生工作"],["more2.htm","党团工作"],["more3.htm","党团工作"],["more4.htm","党团工作"],["more18.htm","行政工作"],["more19.htm","行政工作"],["more20.htm","行政工作"] ]
        for i in range(len(url)):
            if str(url[i][1])=="党团工作":
                content=YiYao.GetByYiYaoDangTuan("http://222.195.158.131/yiyaodtgz/"+url[i][0]);
            elif str(url[i][1])=="行政工作":
                content=YiYao.GetByYiYaoXingZheng("http://222.195.158.131/xydw/"+url[i][0]);
            else:
                content=YiYao.GetByYiYao("http://222.195.158.131/yiyao/"+url[i][0]);
            length=len(content);
            #print length
            if length<=0:
                update=update+1;
            else:          
                for j in range(length):
                    #print content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1]
                    Insert(content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1],"医药学院",8)
                print time.ctime()+"\t医药学院新闻更新数目:"+str(length)
        if update==len(url):
            print time.ctime()+"\t医药学院\t暂无更新"   
    except  :
        print time.ctime()+"\t医药学院更新连接超时。"  
#环境科学与工程学院      
def InsertHuanKe():
    try:
        update=0;
        url=[["more1.htm","学院要闻"],["more2.htm","就业信息"],["more4.htm","教学工作"],["more5.htm","学生风采"],["more6.htm","规章制度"]]
        for i in range(len(url)):
            content=HuanKe.GetByHuanKe("http://222.195.158.131/huanjing/"+url[i][0]);
            length=len(content);
            #print length
            if length<=0:
                update=update+1;
            else:          
                for j in range(length):
                    #print content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1]
                    Insert(content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1],"环境科学与工程学院",9)
                print time.ctime()+"\t环境科学与工程学院新闻更新数目:"+str(length)
        if update==len(url):
            print time.ctime()+"\t环境科学与工程学院\t暂无更新"    
    except  :
        print time.ctime()+"\t环境科学与工程学院更新连接超时。"  
#经济学院      
def InsertJingJi():
    try:
        update=0;
        url=[["news.asp?cId=58","最新公告"],["news.asp?cId=62","最新动态"],["news.asp?itemId=36&cId=37","学术讲座"],["student/news.asp?cid=61","学生工作：最新动态"],["student/news.asp?cid=66","学生工作：工作通知"],["student/jiuye-news.asp?cid=44","招聘信息"],["student/jiuye-news.asp?cid=43","招聘：工作通知"],["student/jiuye-news.asp?itemid=63&cId=67","就业指导：公务员"],["student/jiuye-news.asp?itemid=63&cId=68","金融系统"],["student/jiuye-news.asp?itemid=63&cId=69","贸易物流"],["student/jiuye-news.asp?itemid=63&cId=70","外企其他"],["student/jiuye-news.asp?itemid=63&cId=71","行业经验"],["student/jiuye-news.asp?itemid=63&cId=72","就业讲座"],["student/jiuye-news.asp?itemid=63&cId=73","考研经验"]]
        for i in range(len(url)):
            #print url[i][1]
            if i<=3:
                
                content=JingJi.GetByJingJi ("http://www2.ouc.edu.cn/jingji/"+url[i][0]);
            else:
                content=JingJi.GetByJingJiStudent("http://www2.ouc.edu.cn/jingji/"+url[i][0]);
            length=len(content);
            #print length
            if length<=0:
                update=update+1;
            else:          
                for j in range(length):
                    #print content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1]
                    Insert(content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1],"经济学院",10)
                print time.ctime()+"\t经济学院新闻更新数目:"+str(length)
        if update==len(url):
            print time.ctime()+"\t\t暂无更新";       
    except  :
        print time.ctime()+"\t经济学院更新连接超时。"   
#文新学院      
def InsertWenXin():
    try:
        update=0;
        url=[["CollegeNews.aspx?news=1","学院新闻"],["CollegeNews.aspx","工作通知"]]
        for i in range(len(url)):
            #print url[i][1]        
            content=WenXin.GetByWenXin ("http://www3.ouc.edu.cn/artcollege/"+url[i][0]);
            length=len(content);
            #print length
            if length<=0:
                update=update+1;
            else:          
                for j in range(length):
                    #print content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1]
                    Insert(content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1],"文新学院",11)
                print time.ctime()+"\t文新学院新闻更新数目:"+str(length)
        if update==len(url):
            print time.ctime()+"\t\t暂无更新"; 
    except  :
        print time.ctime()+"\t文新学院更新连接超时。"  
#数学学院
def InsertShuXue():
    try:
        update=0;
        url=[["http://www2.ouc.edu.cn/math/Ch/main.asp","首页"]]
        for i in range(len(url)):
            #print url[i][1]        
            content=ShuXue.GetByShuXue(url[i][0]);
            length=len(content);
            #print length
            if length<=0:
                update=update+1;
            else:          
                for j in range(length):
                    #print content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1]
                    Insert(content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1],"数学学院",12)
                print time.ctime()+"\t数学学院新闻更新数目:"+str(length)
        if update==len(url):
            print time.ctime()+"\t\t暂无更新";    
    except  :
        print time.ctime()+"\t数学学院更新连接超时。"  
# 基础教学中心
def InsertJiJiao():
    try:
        update=0;
        url=[["通知新闻","more1.htm"],["公告栏","more2.htm"],["学生工作","more7.htm"],["就业信息","more8.htm"]]
        for i in range(len(url)):
            print url[i][0]        
            content=JiJiao.GetByJiJiao("http://222.195.158.131/jcjxzx/"+url[i][1]);
            length=len(content);
            #print length
            if length<=0:
                update=update+1;
            else:          
                for j in range(length):
                    #print content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1]
                    Insert(content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1],"基础教学中心",13)
                print time.ctime()+"\t基础教学中心新闻更新数目:"+str(length)
        if update==len(url):
            print time.ctime()+"\t\t暂无更新";
    except  :
        print time.ctime()+"\t基础教学中心更新连接超时。"  
# 艺术系
def InsertYiShu():
    try:
        update=0;
        url=[["最新公告","more11.htm"],["系内动态","more1.htm"],["学术交流","more9.htm"]]
        for i in range(len(url)):
    #        print url[i][0]        
            content=YiShu.GetByYiShu("http://222.195.158.131/wanb/"+url[i][1]);
            length=len(content);
    #        print length
            if length<=0:
                update=update+1;
            else:          
                for j in range(length):
                    #print content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1]
                    Insert(content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1],"艺术系",14)
                print time.ctime()+"\t艺术系新闻更新数目:"+str(length)
        if update==len(url):
            print time.ctime()+"\t\t暂无更新";   
    except  :
        print time.ctime()+"\t艺术系更新连接超时。"  
# 选课系统
def InsertSystemOfCourse():
    try:
        update=0;
        url=[["最新公告","http://jwc.ouc.edu.cn:8080/ouc/index.do"]]
        for i in range(len(url)):
    #        print url[i][0]        
            content=SystemOfCourse.GetByCourse(url[i][1]);
            length=len(content);
    #        print length
            if length<=0:
                update=update+1;
            else:          
                for j in range(length):
                    #print content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1]
                    Insert(content[j][0],MySQLdb.escape_string(str(content[j][2])),content[j][1],"选课系统",15)
                print time.ctime()+"\t选课系统公告更新数目:"+str(length)
        if update==len(url):
            print time.ctime()+"\t选课系统公告\t暂无更新"      
    except  :
        print time.ctime()+"\t选课系统更新连接超时。"     
def InsertJiaoWuChu():
    try:
        JwcNews.InsertDB("http://jwc.ouc.edu.cn:8080/jwwz/index.jsp") 
    except  :
        print time.ctime()+"\t教务处更新连接超时。"                                     
def GetCount(title,newsclassname,time):#验证数据库中是否包含该条信息
    ask=["Title","NewsClassName","Time"]
    answer=[title,newsclassname,time]
    count=SQLHelper.GetCountMore("News", ask, answer)
    return count
def Insert(title,content,time,name,id):#插入到数据库中       
    count=GetCount(title,name,time);
    if count <1:
        number="insert into News(Title,Content,Time,NewsClassName,NewsClassID) values('%s','%s','%s','%s','%d')"% (title,content,time,name,id)
        insert=SQLHelper.InsertAboutNumber(number)        
        if insert==1:
            print "OK"       
        else:
            print "插入新闻出现错误！！"
            #cur.execute("insert into Information(Title,Content,Time,ClassID,ClassName) values('%s','%s','%s','%d','%s')"% (str(information[i][0]),MySQLdb.escape_string(information[i][2]),information[i][3],3,"教务处"))
  
if __name__=="__main__":
    #InsertHaiHuan();  
    #InsertHaiSheng();
    #InsertShiPin();
    #InsertGongCheng();
    #InsertGuanLi();
    #InsertWaiYu();
    #InsertShuiChan();
    #InsertYiYao();
    #InsertHuanKe();
    #InsertJingJi();
    #InsertWenXin();
    #InsertShuXue();
    #InsertJiJiao();
    #InsertYiShu();
    #InsertSystemOfCourse();
    InsertJiaoWuChu();