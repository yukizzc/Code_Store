from bs4 import BeautifulSoup
import requests
import numpy as np
import re
import pandas as pd

#程序用于六氟磷酸锂的价格,用来买多福多的
a_url = 'http://www.ciaps.org.cn/quote/list-htm-catid-707'

url_list = [a_url + '-page-' + str(x) + '.html' for x in range(1,51)]

son_url_list = []
def web_1():
    #第一层页面
    #global son_url_list
    for url in url_list:
        r = requests.get(url)
        r.encoding = 'gbk2312'
        html = r.text
        #第一层解析
        soup = BeautifulSoup(html,"html.parser")
        #获取指定id的div模块
        div = soup.find_all('li',class_="catlist_li")
        soup2 = BeautifulSoup(str(div),"html.parser")
        for i in soup2.find_all('a'):
            son_url_list.append(i.attrs['href'])

web_1()


dic = {}
def web_2():
    for url in son_url_list:
        r = requests.get(url)
        r.encoding = 'gbk2312'
        html = r.text
        #第一层解析
        soup = BeautifulSoup(html,"html.parser")
        #获取指定id的div模块
        div = soup.find_all('td',bgcolor="#FFFFFF")
        try:
            price = div[-4].string.replace('\n','').replace('\t','').replace('\r','')
            # 把上下价格分成一个列表，然后过滤如果大于10000就取前面数值
            price = price.split('-')
            price =  map(lambda x: x if len(x)<4 else x[:-4],price)
            #日期
            #获取指定id的div模块
            div2 = soup.find_all('div',class_="info")  
            begin = str(div2).find('发布日期')
            date = str(div2)[begin+5:begin+15]
            dic[date] = price
        except:
            print('地址出错',url)


web_2()

df = pd.DataFrame(dic,index=['low','high'])
df = df.T
df.to_csv('c:/ftt.csv')
print('over')
