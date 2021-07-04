from bs4 import BeautifulSoup
import requests

url_ = r'https://sh.lianjia.com/ershoufang/107101295728.html?fb_expo_id=407651876382240770'

def cal(url):
#原始网页文件
    r = requests.get(url)
    html = r.text
    #第一层解析
    soup = BeautifulSoup(html,"html.parser")
    #获取指定id的div模块
    div = soup.find_all('div',id="infoList")
    #div要转换str格式然后再塞入soup解析
    soup2 = BeautifulSoup(str(div),"html.parser")
    li = soup2.find_all('div',class_="col")
    total = 0
    for i in range(1,len(li),4):
        print(li[i-1].string,li[i].string)
        total+=float(li[i].string[:-2])
    print('总面积:',total)

cal(url_)
