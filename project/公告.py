from bs4 import BeautifulSoup
import requests
#import win32com.client
import time
from datetime import datetime,timedelta


def sq():
    url = r'http://www.shfe.com.cn/news/notice/'
    r = requests.get(url)
    r.encoding = 'utf-8'
    html = r.text

    #第一层解析
    soup = BeautifulSoup(html,"html.parser")
    ul= soup.find_all('ul')
    soup2 = BeautifulSoup(str(ul),"html.parser")
    #li= soup2.find_all('li')
    #speaker = win32com.client.Dispatch("SAPI.SpVoice")
    if datetime.now().isoweekday()==1: ###返回数字1-7代表周一到周日
        offset=-3
    else:
        offset=-1

    date=(datetime.now()+timedelta(days=offset)).strftime("%Y-%m-%d")
    n=0
    for i in soup2.find_all('li'):
        str1=i.span.text
        str2=i.a.attrs['title']
        #print(str1+str2)
        if str1[1:-1]>=date:
            if n==0:
                print('\n上期所公告')
                #speaker.Speak('上期所公告')
                n = 1
            print(str1+str2)
            #speaker.Speak(str1+str2)

def zq():
    url = r'http://app.czce.com.cn/cms/pub/search/searchdt.jsp'
    r= requests.get(url)
    r.encoding = 'utf-8'
    html = r.text

    #第一层解析
    soup = BeautifulSoup(html,"html.parser")
    ul= soup.find_all('tr')
    soup2 = BeautifulSoup(str(ul),"html.parser")
    str1 = soup2.text
    str2=str1.replace("\n", "").replace("]", "").replace("[标题发布日期", "").split(',')
    #print(str2)
    #speaker = win32com.client.Dispatch("SAPI.SpVoice")
    if datetime.now().isoweekday()==1: ###返回数字1-7代表周一到周日
        offset=-3
    else:
        offset=-1

    date=(datetime.now()+timedelta(days=offset)).strftime("%Y-%m-%d")
    n=0
    for i in str2:
        if i[-10:]>=date:
            if n==0:
                print('\n郑商所公告')
                #speaker.Speak('郑商所公告')
                n = 1
            aaa=i[-10:]+i[:-10]
            print(aaa)
            #speaker.Speak(aaa)



def dq():
    url = r'http://www.dce.com.cn/dalianshangpin/yw/fw/jystz/ywtz/index.html'
    r = requests.get(url)
    r.encoding='utf-8'
    html = r.text

    #第一层解析
    soup = BeautifulSoup(html ,"html.parser")
    ul= soup.find_all('ul',class_="list_tpye06" )
    soup2 = BeautifulSoup(str(ul),"html.parser")
    #li= soup2.find_all('li')
    #soup2.li.span.text
    #soup2.li.a.attrs
    #speaker = win32com.client.Dispatch("SAPI.SpVoice")
    if datetime.now().isoweekday()==1: ###返回数字1-7代表周一到周日
        offset=-3
    else:
        offset=-1

    date=(datetime.now()+timedelta(days=offset)).strftime("%Y-%m-%d")
    n=0
    for i in soup2.find_all('li'):
        str1=i.span.text
        str2=i.a.attrs['title']
        #print(str1+str2)
        if str1>=date:
            if n==0:
                print('\n大商所公告')
                #speaker.Speak('大商所公告')
                n = 1
            print(str1+str2)
            #speaker.Speak(str1+str2)


def zj():
    url = r'http://www.cffex.com.cn/jysgg/'
    r = requests.get(url)
    r.encoding='utf-8'
    html = r.text

    #第一层解析
    soup = BeautifulSoup(html,"html.parser")
    ul= soup.find_all('ul',class_="clearFloat" )
    soup2 = BeautifulSoup(str(ul),"html.parser")
    #li= soup2.find_all('li')

    #soup2.li.a.attrs

    #speaker = win32com.client.Dispatch("SAPI.SpVoice")
    if datetime.now().isoweekday() == 1:  ###返回数字1-7代表周一到周日
        offset = -3
    else:
        offset = -1

    date = (datetime.now() + timedelta(days=offset)).strftime("%Y-%m-%d")
    n=0
    for i in soup2.find_all('li'):
        str1 = i.text[-10:]
        str2 = i.a.attrs['title']
        # print(str1+str2)
        if str1 >= date:
            if n==0:
                print('\n中金所公告')
                #speaker.Speak('中金所公告')
                n=1
            print(str1 + str2)
            #speaker.Speak(str2)

sq()
dq()
zq()
zj()
print('\n')
print(datetime.now())
time.sleep( 1800 )
print(datetime.now())
