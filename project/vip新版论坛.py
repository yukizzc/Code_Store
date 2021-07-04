
# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import tkinter as tk
from tkinter.messagebox import *
import time
import threading
import webbrowser
import requests
import pandas as pd

#爬去可转债当日申购
def get_stock():
    url = r'http://bond.jrj.com.cn/data/kzz.shtml'
    r = requests.get(url)
    demo = r.text
    today = time.strftime("%Y-%m-%d", time.localtime())
    soup = BeautifulSoup(demo, 'html.parser')
    links = soup.find_all('td',title=today)
    stock_num = len(links)
    if stock_num > 0:
        showwarning('今日可转债', '数量为'+str(stock_num))
    t2.insert('end', '今日可转债'+str(stock_num)+'\n')
    t2.focus_force()
#输出持仓股票的上市日期
def get_stock_market_time():
    stock = []
    with open('.\stock.txt') as f:
        stock = f.read().splitlines()
    url = r'http://bond.jrj.com.cn/data/kzz.shtml'
    r = requests.get(url)
    demo = r.text
    soup = BeautifulSoup(demo, 'html.parser')
    links = soup.find_all('tr')
    links2 = BeautifulSoup(str(links), 'html.parser')
    child = links2.children
    x = None
    for i in child:
        soup2 = BeautifulSoup(str(i), 'html.parser')
        for j in stock:
            bb = soup2.find('a', text=j)
            if bb != None:
                x = i
                date = x.find_all('td')
                t2.insert('end', j + '上市日期' + str(date[10].contents)[2:-2] + '\n')
                t2.focus_force()

web_url = 'https://www.weistock.com/bbs/forum.php'


#用来更新num值
def start():
    global num
    url = web_url
    r = requests.get(url)  
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find_all('dt')
    num_0 = spider(div[0])
    num_1 = spider(div[1])
    num_2 = spider(div[2])
    num = num_0 + num_1 + num_2

# 爬取今日发帖数
def spider(html):
    soup = BeautifulSoup(str(html), 'html.parser')
    div = soup.find_all('em')
    if len(div) == 0:
        return 0
    else:
        return int(soup.find_all('em')[0].string[2:-1])
use = True
window = tk.Tk()
window.geometry('400x800')
t = tk.Text(window, height=18)
t2 = tk.Text(window, height=18)

#定时扫描num2是否大于num了
def message():
    global use
    global num
    while True:
        time.sleep(60)
        url2 = web_url
        r = requests.get(url2)  
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find_all('dt')
        num_0 = spider(div[0])
        num_1 = spider(div[1])
        num_2 = spider(div[2])
        num2 = num_0 + num_1 + num_2
        if num2 > num:
            ask = askquestion('喜欢郭丽', '您是否已经回帖好了?')
            t.insert('end', '软件区:' + str(num_0) + '帖    ' + '公式区:' + str(num_1)
                     + '帖    ' + '高级区:' + str(num_2) + '帖' + '\n')
            if ask == 'yes':
                start()
            else:
                pass
        if not(use == True):
            break
#定时新帖输出数量
def debugout():
    global use
    while True:
        url2 = web_url
        r = requests.get(url2)  
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find_all('dt')
        num_0 = spider(div[0])
        num_1 = spider(div[1])
        num_2 = spider(div[2])
        now = time.strftime('%H:%M', time.localtime(time.time()))
        t2.insert('end', str(now) + '软件区:' + str(num_0) + '帖    ' + '公式区:'
                  + str(num_1) + '帖    ' + '高级区:' + str(num_2) + '帖' + '\n')
        t2.focus_force()
        time.sleep(300)
        if not(use == True):
            break





t1 = threading.Thread(target=message)
t3 = threading.Thread(target=debugout)

def start_time():
    global use
    use = True
    get_stock()
    get_stock_market_time()
    t1.start()
    t3.start()
    start()
    #启动论坛用户检索
    #t_mail.start()

    

def stop_time():
    global use
    use = False

def open_page():
    webbrowser.open(web_url)



def del_text():
    t2.delete(1.0,tk.END)


b1 = tk.Button(window, text='start', width=15, height=2, command=start_time)
b2 = tk.Button(window, text='stop', width=15, height=2, command=stop_time)
page = tk.Button(window, text='vip论坛', width=15, height=2, command=open_page)


delete_text = tk.Button(window, text='Delete', width=15, height=2, command=del_text)
b1.pack()
b2.pack()
t.pack()
page.pack()
t2.pack()
delete_text.pack()

# 循环窗体
window.mainloop()

#window.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0));

