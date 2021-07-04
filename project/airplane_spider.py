import urllib.request

import time
import datetime


def dateRange(beginDate, endDate):
    dates = []

    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")

    date = beginDate[:]

    while date <= endDate:
        dates.append(date)

        dt = dt + datetime.timedelta(1)

        date = dt.strftime("%Y-%m-%d")

    return dates


'''
在携程机票页面查看源找到这个位置，url后面的就是我们需要的地址 
<body class="gray_body">

        <script type="text/javascript">
    var url =
'''
now = datetime.datetime.now()
delta = datetime.timedelta(days=1)
n_days = now + delta
date = dateRange(n_days.strftime('%Y-%m-%d'), '2018-07-30')
price_list = []

import numpy as np


def get_price(date):
    import json
    url = 'http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=SHA&ACity1=LJG&SearchType=S&DDate1=' + date + '&IsNearAirportRecommond=0&LogToken=2ab81561ee944390a0f50d17ddb3a44d&CK=8B65264CE2C86F100B0E74CF1BFA61B6"'
    headers = {
        "Host": "flights.ctrip.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
        "Referer": "http://flights.ctrip.com/booking/SHA-BJS-day-1.html?DDate1=2017-10-22",
        "Connection": "keep-alive",
    }
    res = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(res).read().decode("gb2312")
    jsonData = json.loads(res)
    for json in jsonData['fis']:
        price = []
        start = json['dpbn']
        stop = json['apbn']
        starteDate = json['dt']
        stopDate = json['at']
        timestart = time.strptime(starteDate, '%Y-%m-%d %H:%M:%S')
        timestop = time.strptime(stopDate, '%Y-%m-%d %H:%M:%S')
        money = json['lp']
        price.append(money)
        print('起飞时间' + str(starteDate) + '到达时间' + str(stopDate) + '价格' + str(money))
    price_list.append(np.array(price).min())


for i in date:
    get_price(i)

print(price_list)

import matplotlib.pyplot as plt
x = range(len(price_list))
y = price_list
plt.plot(x,y)
