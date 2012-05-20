#-*- coding:utf-8 -*-
'''
Created on 2011-11-17

@author: hlq
'''
import urllib,MySQLdb,re
from BeautifulSoup import BeautifulSoup
def GetHtml(url):
    html=urllib.urlopen(url).read();
    if "gb2312" in html:
        html=html.decode("gb2312","ignore");
    elif "GB2312" in html:
        html=html.decode("GB2312","ignore"); 
    parser=BeautifulSoup(html);
    return parser
#时间正则表达式，筛选符合的时间条件 
#将一串还有时间的字符串用该函数处理可以得到字符串中完整的时间，根据不同的时间类型           
def ChoiceTime(time):
    time0=re.findall(r'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d',time)
    time1=re.findall(r'\d\d\d\d-\d-\d\d \d\d:\d\d:\d\d',time)
    time2=re.findall(r'\d\d\d\d-\d\d-\d \d\d:\d\d:\d\d',time)
    time3=re.findall(r'\d\d\d\d-\d-\d \d\d:\d\d:\d\d',time)
    time4=re.findall(r'\d\d\d\d-\d\d-\d\d \d:\d\d:\d\d',time)
    time5=re.findall(r'\d\d\d\d-\d-\d\d \d:\d\d:\d\d',time)
    time6=re.findall(r'\d\d\d\d-\d\d-\d \d:\d\d:\d\d',time)
    time7=re.findall(r'\d\d\d\d-\d-\d \d:\d\d:\d\d',time)   
    s=""
    if time0==[]:
        if time1==[]:
            if time2==[]:
                if time3==[]:
                    if time4==[]:
                        if time5==[]:
                            if time6==[]:
                                if time7==[]:
                                    s=""
                                else:
                                    s=time7[0]                
                            else:
                                s=time6[0]
                        else:
                            s=time5[0]
                    else:
                        s=time4[0]
                else:
                    s=time3[0]
            else:
                s=time2[0]
        else:
            s=time1[0]
    else:
        s=time0[0]
        
    return s  
#该函数用于选择制定
def ChoiceTime2(time):
    time0=re.findall(r'\d\d\d\d\/\d\d\/\d\d \d\d:\d\d:\d\d',time)
    time1=re.findall(r'\d\d\d\d\/\d\/\d\d \d\d:\d\d:\d\d',time)
    time2=re.findall(r'\d\d\d\d\/\d\d\/\d \d\d:\d\d:\d\d',time)
    time3=re.findall(r'\d\d\d\d\/\d\/\d \d\d:\d\d:\d\d',time)
    time4=re.findall(r'\d\d\d\d\/\d\d\/\d\d \d:\d\d:\d\d',time)
    time5=re.findall(r'\d\d\d\d\/\d\/\d\d \d:\d\d:\d\d',time)
    time6=re.findall(r'\d\d\d\d\/\d\d\/\d \d:\d\d:\d\d',time)
    time7=re.findall(r'\d\d\d\d\/\d\/\d \d:\d\d:\d\d',time)   
    s=""
    if time0==[]:
        if time1==[]:
            if time2==[]:
                if time3==[]:
                    if time4==[]:
                        if time5==[]:
                            if time6==[]:
                                if time7==[]:
                                    s=""
                                else:
                                    s=time7[0]                
                            else:
                                s=time6[0]
                        else:
                            s=time5[0]
                    else:
                        s=time4[0]
                else:
                    s=time3[0]
            else:
                s=time2[0]
        else:
            s=time1[0]
    else:
        s=time0[0]
        
    return s           
def ChoiceTime3(time):
    time0=re.findall(r'\d\d\d\d-\d\d-\d\d',time)
    time1=re.findall(r'\d\d\d\d-\d-\d\d',time)
    time2=re.findall(r'\d\d\d\d-\d\d-\d',time)
    time3=re.findall(r'\d\d\d\d-\d-\d',time)
    s=""
    if time0==[]:
        if time1==[]:
            if time2==[]:
                if time3==[]:
                                        
                    s=""
                else:
                    s=time3[0]
            else:
                s=time2[0]
        else:
            s=time1[0]
    else:
        s=time0[0]
        
    return s  