from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import gloal_name
import time
area_name = gloal_name.area_name
gloal_total = gloal_name.num 
# 先手工确定网页范围,默认按找松江的
url_start = gloal_name.url
url_list = []
for i in range(1,gloal_total+1):
    temp = url_start[:-4]+'pg'+str(i)+'/'
    url_list.append(temp)

# 根据上面每一页地址获取该页下具体链接地址
url_house_list = []
for i in url_list:
    #第一层解析
    soup = BeautifulSoup(urlopen(i),"html.parser")
    #获取指定ul模块
    div = soup.find_all('li',class_="clear")
    #div要转换str格式然后再塞入soup解析
    soup2 = BeautifulSoup(str(div),"html.parser")
    for j in soup2.find_all(target="_blank"):
        temp = j['href']
        url_house_list.append(temp)
link_li = list(set(url_house_list))
import json                                                                                         
#打开一个名字为‘user_info.json’的空文件
with open(area_name+'1'+'.json','w',encoding='utf-8') as f:   
    json.dump(link_li,f,ensure_ascii=False,indent=4)
print(len(link_li))
print('over')