from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.request import urlopen
import json
from threading import Thread
import time  
import gloal_name
import queue

q = queue.Queue()
area_name = gloal_name.area_name                                                                                       
f = open(area_name+'1'+'.json',encoding='utf-8')
url_list = json.load(f)
f.close()
url1 = url_list[500*0:500*1]
url2 = url_list[500*1:500*2]
url3 = url_list[500*2:500*3]
url4 = url_list[500*3:500*4]
url5 = url_list[500*4:500*5]
url6 = url_list[500*5:500*6]
url7 = url_list[500*6:]

# 数据库
import mysql.connector
coon = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database='liu'
)

def get_data(url_list_input):
    result = []
    for i in url_list_input:
        try:
            url = i
            r = requests.get(url,timeout=200)
            html = r.text
        except:
            print('出错链接',i,'序号',url_list.index(i))
            q.put(i)
            continue
        try:
            soup = BeautifulSoup(html,"html.parser")
            # 名称
            div = soup.find_all('a',class_="info no_resblock_a")
            soup2 = BeautifulSoup(str(div),"html.parser")
            name = div[0].string
            # 区域
            div = soup.find_all('span',class_="info")
            soup2 = BeautifulSoup(str(div),"html.parser")
            div2 = soup2.find_all('a',target="_blank")
            location = div2[1].string
            # 总价
            div = soup.find_all('span',class_="total")
            soup2 = BeautifulSoup(str(div),"html.parser")
            total_price = div[0].string
            # 单价
            div = soup.find_all('span',class_="unitPriceValue")
            soup2 = BeautifulSoup(str(div),"html.parser")
            per_price = div[0].string
            # 面积
            area = ''
            soup = BeautifulSoup(html,"html.parser")
            div = soup.find_all('div',class_="mainInfo")
            soup2 = BeautifulSoup(str(div),"html.parser")
            for j in div:
                area = j.string+'_'+area
            area = area[:-1]
            # 建筑年代
            div = soup.find_all('div',class_="subInfo noHidden")
            soup2 = BeautifulSoup(str(div),"html.parser")
            house_date = div[0].string
            # 插入数据库
            cursor = coon.cursor(buffered=True)
            code = area_name
            temp = ' (url,location,name,date,per_price,total_price,area) values(%s,%s,%s,%s,%s,%s,%s)'
            sql = 'insert into ' + code  + temp
            val = (i,str(location),str(name),str(house_date).replace('\n',''),float(per_price),float(total_price),str(area))
            cursor.execute(sql, val)
            # 提交事务，数据表内容有更新，必须使用到该语句
            coon.commit()
            cursor.close()
        except:
            print('该链接抓取数据有错误',i)
            continue           

# df = pd.DataFrame(result,columns=['url','name','date','per_price','total_price','area'])
ur1 = Thread(target=get_data,args=(url1,))
ur2 = Thread(target=get_data,args=(url2,))
ur3 = Thread(target=get_data,args=(url3,))
ur4 = Thread(target=get_data,args=(url4,))
ur5 = Thread(target=get_data,args=(url5,))
ur6 = Thread(target=get_data,args=(url6,))
ur7 = Thread(target=get_data,args=(url7,))
if __name__ == '__main__':
    ur1.start()
    ur2.start()
    ur3.start()
    ur4.start()
    ur5.start()
    ur6.start()
    ur7.start()

    ur1.join()
    ur2.join()
    ur3.join()
    ur4.join()
    ur5.join()
    ur6.join()
    ur7.join()
    coon.close()
    print('over1')
    err = []
    while True:
        if not(q.empty()):
            err.append(q.get())
        else:
            break
    with open(area_name+'2'+'.json','w',encoding='utf-8') as f:   
        json.dump(err,f,ensure_ascii=False,indent=4)
    print('over2')


