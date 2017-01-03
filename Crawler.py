# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests as rq

import PIL
from PIL import Image
from StringIO import StringIO
import bs4
from bs4 import BeautifulSoup as bs
import re
import os
import codecs

Dir = os.path.join(os.path.abspath('.'), 'ShuCodeDir')
os.mkdir(Dir)
print "创建文件夹中....."
Username = raw_input('输入用户名:\n')
Password = raw_input('输入密码:\n')


hostUrl = "http://202.121.199.212/JudgeOnline"
loginUrl = hostUrl+"/login.php"
captchaUrl = hostUrl+"/vcode.php"
session = rq.Session()
Image.open(StringIO(session.get(captchaUrl).content)).show()
VerifyCode  = raw_input("输入验证码:\n")
header = {
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.6",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
"Content-Type":"application/x-www-form-urlencoded",
"Host":"202.121.199.212",
"Origin":"http://202.121.199.212",
"Referer":"http://202.121.199.212/JudgeOnline/loginpage.php",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36"
}



session.get(loginUrl,headers=header)
formData = {
"user_id":Username,
"password":Password,
"vcode":VerifyCode,
"submit":"Submit"}
print "模拟登陆中......"
session.post(loginUrl,data=formData,headers=header)
print "模拟登陆成功"

# Req =  session.get("http://202.121.199.212/JudgeOnline/status.php?problem_id=&user_id="+Username+"&language=1&jresult=4")
# Soup = bs(Req.text,"html.parser")
# tagArr = Soup.find_all('a',href=re.compile("showsource\.php\?id=*"))
# List = []
# for tag in tagArr:
#     List.append(tag['href'])

# NextPage = Soup.find('a',text="Next Page")
# NextUrl = NextPage['href']
# prePageUrl = ""

# Count = 0
# while(cmp(NextUrl,prePageUrl) != 0):
#     Count = Count+1
#     Req = session.get("http://202.121.199.212/JudgeOnline/"+NextUrl)
#     prePageUrl = NextUrl
#     Soup = bs(Req.text,"html.parser")
#     tagArr = Soup.find_all('a',href=re.compile("showsource\.php\?id=*"))
#     for tag in tagArr:
#         List.append(tag['href'])
#     NextPage = Soup.find('a',text="Next Page")
#     NextUrl = NextPage['href']

print "获取Status题目列表中....."
List2 = []
Req = session.get("http://202.121.199.212/JudgeOnline/userinfo.php?user="+Username)
Req.encoding = "utf-8"
Soup = bs(Req.text,"html.parser")
Text = " "
tagArr = Soup.find_all('script',text=re.compile(".*problem\.php\?id=.*"))
for tag in tagArr:
    Text = tag.text
TextArr = Text.split('\n')
for text in TextArr[2].split(';'):
    List2.append(text[2:-1])
CodeUrl = "http://202.121.199.212/JudgeOnline/showsource.php?id="
ListUrl =[]
for ID in List2:
    Req = session.get("http://202.121.199.212/JudgeOnline/status.php?problem_id="+ID+"&user_id="+Username+"&language=-1&jresult=4")
    Soup = bs(Req.text,"html.parser")
    tagArr = Soup.find_all('a',href=re.compile(".*showsource\.php\?id=.*"))
    Tmp = ""
    for tag in tagArr:
        Tmp = tag['href']
    if(cmp(Tmp,"")!=0):
        ListUrl.append(Tmp)

print "获取成功"

print "获取Contest题目列表中"
EndCid = 1176
StartCid = 1118
while (StartCid <= EndCid):
    Cid = str(StartCid)
    Req = session.get("http://202.121.199.212/JudgeOnline/status.php?problem_id=&user_id="+Username+"&cid="+Cid+"&language=-1&jresult=4")
    Soup = bs(Req.text, "html.parser")
    tagArr = Soup.find_all('a', href=re.compile(".*showsource\.php\?id=.*"))
    Tmp = ""
    for tag in tagArr:
        Tmp = tag['href']
        if (cmp(Tmp, "") != 0):
            ListUrl.append(Tmp)
    StartCid = StartCid + 1

print "获取成功"

print "生成键值对中....."
ListPid = []
Count = 0
ListUrlWeNeed = []
Pid_Url = {}
for Url in ListUrl:
    IsOk = False
    Req = session.get(hostUrl+'/'+Url)
    Soup = bs(Req.text,"html.parser")
    tag = Soup.find('pre')
    Text = tag
    Text = str(Text)
    Pid = ""
    if(cmp(Text," ")!=0):
        textArr = Text.split('\n')
        Pid = textArr[-9][-4:]
        if Pid not in ListPid:
            ListPid.append(textArr[-9][-4:])
            IsOk = True
    if IsOk == True:
        ListUrlWeNeed.append(Url)
        Pid_Url[Pid] = Url

print "生成键值对成功"

print "开始获取源码并生成cpp文件中"
Count = 0
for key in Pid_Url:
    Req = session.get(hostUrl+'/'+Pid_Url[key])
    Req.encoding = 'utf-8'
    Soup = bs(Req.text,"html.parser")
    tag = Soup.find('pre')
    Text = str(tag).split('\n')
    pattern1 = re.compile(r'&lt;')
    pattern2 = re.compile(r'&gt;')
    pattern3 = re.compile(r'&amp;')
    fileName = Dir+'/Shu'+key+'.cpp'
    with codecs.open(fileName, 'a', 'utf-8') as file:
        for line in Text[1:-10]:
            line = pattern1.sub('<',line)
            line = pattern2.sub('>',line)
            line = pattern3.sub('&',line)
            file.write(line)
            file.write('\n')
        file.close()
    Count = Count +1

print "生成文件完成"
    # fileName = Dir+'/test1.cpp'
    # f = open(fileName,'w')
        # pattern = re.compile(r".*pre class=.*")
        # match = pattern.match(Text)
        # if match:
        #     print match.group()
        # else:
        #     print "No"
# print session.get(hostUrl+'/'+ListUrl[0]).text



#http://202.121.199.212/JudgeOnline/status.php?problem_id=1615&user_id=14122245&language=1&jresult=4
#http://202.121.199.212/JudgeOnline/showsource.php?id=384492
#http://202.121.199.212/JudgeOnline/status.php?&top=386112&prevtop=386137
#http://202.121.199.212/JudgeOnline/status.php?problem_id=&user_id=14122245&cid=1176&language=-1&jresult=-1


#