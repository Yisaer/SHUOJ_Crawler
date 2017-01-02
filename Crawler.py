# -*- coding: utf-8 -*-
import sys
reload(sys)
import requests as rq

import PIL
from PIL import Image
from StringIO import StringIO
import bs4
from bs4 import BeautifulSoup as bs
import re


hostUrl = "http://202.121.199.212/JudgeOnline"
loginUrl = hostUrl+"/login.php"
captchaUrl = hostUrl+"/vcode.php"

session = rq.Session()

Image.open(StringIO(session.get(captchaUrl).content)).show()
VerifyCode  = raw_input("input verifycode:\n")
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


Username = "14122245"
session.get(loginUrl,headers=header)
formData = {
"user_id":"14122245",
"password":"123456",
"vcode":VerifyCode,
"submit":"Submit"}
session.post(loginUrl,data=formData,headers=header)
Req =  session.get("http://202.121.199.212/JudgeOnline/status.php?problem_id=&user_id="+Username+"&language=1&jresult=4")
Soup = bs(Req.text,"html.parser")
tagArr = Soup.find_all('a',href=re.compile("showsource\.php\?id=*"))
List = []
for tag in tagArr:
    List.append(tag['href'])

NextPage = Soup.find('a',text="Next Page")
NextUrl = NextPage['href']
prePageUrl = ""

Count = 0
while(cmp(NextUrl,prePageUrl) != 0):
    Count = Count+1
    Req = session.get("http://202.121.199.212/JudgeOnline/"+NextUrl)
    prePageUrl = NextUrl
    Soup = bs(Req.text,"html.parser")
    tagArr = Soup.find_all('a',href=re.compile("showsource\.php\?id=*"))
    for tag in tagArr:
        List.append(tag['href'])
    NextPage = Soup.find('a',text="Next Page")
    NextUrl = NextPage['href']
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
    List2.append(text)




#http://202.121.199.212/JudgeOnline/status.php?&top=386112&prevtop=386137



