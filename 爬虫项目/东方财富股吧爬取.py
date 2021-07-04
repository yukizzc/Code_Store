from bs4 import BeautifulSoup
import requests
import numpy as np
import re
import pandas as pd
import pymongo


def article(url_):
    #帖子链接
    url = url_
    r = requests.get(url)
    r.encoding = 'gbk2312'
    html = r.text
    #第一层解析
    soup = BeautifulSoup(html,"html.parser")
    #获取指定的div模块
    div = soup.find_all('div',class_="stockcodec .xeditor")
    """过滤符号"""
    flag = 0
    text = ''
    for i in str(div):
        if i=='>':
            flag = 0
            continue
        if  i=='<' or i=='['or flag==1:
            flag = 1
            continue
        if flag==0:
            text+=i

    return text


def to_mongodb(i,j,k):
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient["runoobdb"]
    mycol = mydb["sites"]
    mydict = { "title": i, "url": j, "text": k}
    x = mycol.insert_one(mydict) 



url = 'http://guba.eastmoney.com/list,002163.html?from=BaiduAladdin'
r = requests.get(url)
r.encoding = 'gbk2312'
html = r.text

#第一层解析
soup = BeautifulSoup(html,"html.parser")
#获取指定的div模块
div = soup.find_all('div',class_="articleh normal_post")

soup2 = BeautifulSoup(str(div),"html.parser")
dic = {}
for i in soup2.find_all('a'):
    if 'em class' in str(i):
        continue
    if 'title' in str(i):
        if str(i.attrs['href'])[:4]!='http':
            dic[i.attrs['title']] = 'http://guba.eastmoney.com'+i.attrs['href']
for i in dic.keys():
    to_mongodb(i,dic[i],article(dic[i]))
    #print(i,dic[i])
    #print(article(dic[i]))
    #print('-'*20)
    #print('-'*20)


