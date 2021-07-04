from bs4 import BeautifulSoup
import requests
import numpy as np
import re
import pandas as pd
#程序用于爬取金投网原油类现货的价格
def web_1():
    #第一层页面
    url = "https://www.cngold.org/yehq/index.html"
    r = requests.get(url)
    r.encoding = 'gbk2312'
    html = r.text
    #第一层解析
    soup = BeautifulSoup(html,"html.parser")
    #获取指定id的div模块
    div = soup.find_all('div',class_="show_info_page")
    soup2 = BeautifulSoup(str(div),"html.parser")
    li = []
    for i in soup2.find_all('a'):
        li.append(i.attrs['href'])
    li.insert(0,url)
    return li
#得到每一个下一页的地址

#####################################################################################################
a = web_1()
def web_2():
    #保存每一个现货价格地址
    gloable_web = []
    for i in a:
        r = requests.get(i)
        r.encoding = 'gbk2312'
        html = r.text
        #第一层解析
        soup = BeautifulSoup(html,"html.parser")
        #获取指定id的div模块
        div = soup.find_all('div',class_="fl w490 border_eee")
        soup2 = BeautifulSoup(str(div),"html.parser")
        li = []
        for i in soup2.find_all('a'):
            li.append(i.attrs['href'])
        li2 = [i for i in li if len(i)>45]
        gloable_web+=li2
    return gloable_web

########################################################################################################
#得到每一个日期价格的页面
b = web_2()
dic = {}
def web3():
    for i in b:
        url = i
        date_ = url.split('/')[4]
        r = requests.get(url)
        r.encoding = 'gbk2312'
        html = r.text
        #第一层解析
        soup = BeautifulSoup(html,"html.parser")
        #获取指定id的div模块
        div = soup.find('table').find_all('tr')
        price = []
        for tr in div:
            for td in tr.find_all('td')[2:3]:
                m = re.findall("\d+", td.getText())
                price.append(float(m[0]))
        price_mean = np.array(price).flatten().mean()
        dic[date_] = price_mean
web3()
df = pd.DataFrame({'close':dic})
df.to_csv('a.csv')