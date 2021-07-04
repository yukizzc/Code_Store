'''
1、期权平价公式：C+ Ke^-r(T-t)=P+S。
2、公式含义：认购期权价格C与行权价K的现值之和等于认沽期权的价格P加上标的证券现价S。
3、符号解释：T-t：还有多少天合约到期；e的-r(T-t)次方是连续复利的折现系数；Ke^-r(T-t)：K乘以e的-r(T-t)次方,也就是K的现值。到期天数要除以365作为日收益率
4、推导过程：
构造两个投资组合：
组合A: 一份欧式看涨期权C,行权价K，距离到期时间T-t。现金账户Ke^-r(T-t)，利率r，期权到期时恰好变成行权价K。
组合B: 一份有效期和行权价格与看涨期权相同的欧式看跌期权P，加上一单位标的物股票S。
根据无套利原则推导：看到期时这两个投资组合的情况。
期权到期时，若股价ST大于K，投资组合A，将行使看涨期权C，花掉现金账户K，买入标的物股票，股价为ST。投资组合B，放弃行使看跌期权，持有股票，股价为ST。
'''

from PythonApi import *
import numpy as np 
import pandas as pd
def cal(month):
    # 分别保存认购代码、认沽代码、行权价
    call_list = optionlabel_book('510050','QQ',str(month), 1)
    put_list = optionlabel_book('510050','QQ',str(month), 2)
    K_list = [float(format(get_option_info(i,5), '.2f')) for i in call_list]
    
    
    
    # 平价公式 C + K*e^-rt = S + P 
    # 期权到期天数到期天数
    t = get_option_info(call_list[0],4)
    data = []
    for i in range(len(call_list)):
        a = get_dynainf(call_list[i],7) + K_list[i]*np.e**(-0.04*t/365)
        b = get_dynainf('510050',7) + get_dynainf(put_list[i],7)
        data.append([K_list[i],a,b])
        
    df = pd.DataFrame(data,columns=['strick_price','left','right'])
    df['left-right'] = df['left'] - df['right']
    df.sort_values(by='strick_price',inplace=True)
    return df
    
    

# 通过传入年月，2011表示20年的11月
a = cal(2011)
b = cal(2012)
c = cal(2103)
d = cal(2106)
print(a)
print(b)
print(c)
print(d)
