import requests
from PIL import Image
from StringIO import StringIO

Username = '14122245'
Password = '123456'


url = 'http://202.121.199.212/JudgeOnline/'
url_login = url+'loginpage.php'
url_verify = url+'vcode.php'
session = requests.session()
page = session.get(url_login)
page.encoding ='utf-8'
Image.open(StringIO(session.get(url_verify).content)).show()
VerifyCode  = raw_input()
Submit = 'Submit'
LoginData = {
        'user_id': Username,
        'passcode': Password,
        'vcode': VerifyCode,
        'submit': Submit
    }
ReqLogin = session.post(url_login, LoginData)
urlref = 'status.php?problem_id=&user_id='+ Username+'&language=1&jresult=4'
page = session.post(url+urlref)
page.encoding = 'utf-8'
print(page.text)