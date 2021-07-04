# -*- coding:UTF-8 -*-
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pymongo
import datetime
import time
import matplotlib.pyplot as plt
#爬取数据
def get_price():
    url = r'http://index.mysteel.com/price/getChartMultiCity_1_0.html'
    r = requests.get(url)
    demo = r.text

    soup = BeautifulSoup(demo, 'html.parser')
    links = soup.find_all('span')
    price = links[2].get_text()

    price_date = soup.find(id='sStartTime1')['value']
    return price,price_date


#date = datetime.datetime.now().strftime('%Y-%m-%d')
#mongodb数据库链接
conn = pymongo.MongoClient('localhost',27017)

def insert(my_set,dic,date):
    #集合对象（sql中的表）
    num = my_set.find({'date':date}).count()
    if num>0:
        print('你已经有数据了,现在进行更新')
        my_set.update({'date': date}, {'$set': {'price': dic['price']}})
    else:
        my_set.insert(dic)

def find(my_set):
    out = my_set.find()
    result = []
    for i in out:
        result.append(i)
    return result

#db是数据库对象,如果有新品种，修改这里的数据库名以及set名就好了，mongodb会自动建立
db = conn.rb
my_set = db.rb_set

def to_pd(result):
    df = pd.DataFrame(result)
    data = df.ix[:,['date','price']]
    print(data)

if __name__ == '__main__':
    price,date = get_price()
    # 字典文件，日期:价格
    dic = {'date':date,'price': price}
    insert(my_set,dic,date)
    time.sleep(2)
    #print(find(my_set))
    to_pd(find(my_set))
conn.close()
