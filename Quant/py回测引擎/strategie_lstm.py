import pandas as pd
import numpy as np
from sklearn import preprocessing
import read_data
import test_engine
import os
import torch
import torch.nn as nn

# 当前文件名
name = os.path.split(__file__)[-1][:-3]
# 加载历史数据
file = read_data.file
# 品种代码
trade_code = read_data.code

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols = list()
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
    for i in range(0, n_out):
        cols.append(df.shift(-i))
    agg = pd.concat(cols, axis=1)
    if dropnan:
        agg.dropna(inplace=True)
    return agg.values


values = file.loc[:, 'C_'].values
values = values.reshape(-1, 1)
scale = preprocessing.MinMaxScaler().fit(values)
values = scale.transform(values)



# input_size 输入特征的大小
# hidden_size 神经元模块额数量
# num_layer 几层隐藏层
# lstm默认输入的维度是 (seq_len,batch,feature)
class LSTM(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = torch.nn.LSTM(
            input_size = 1,
            hidden_size = 64,
            num_layers = 1,
            batch_first = True
        )
        self.out = nn.Linear(in_features = 64,out_features = 1)
    def forward(self, x):
        output,(h_n,c_n) = self.lstm(x)
        out = self.out(output[:,-1,:])
        return out


device = torch.device('cuda')
model = LSTM().to(device)
model.load_state_dict(torch.load('./lst_ft.pth'))

class Test(test_engine.BackTest):
    def __init__(self, data):
        super().__init__(data)
        self.money = 500*10000
        self.multiplier = 300
        self.deposit = 0.2
        self.fee = 200
        # 定义交易的合约代码
        self.trade_code = trade_code

    def handle_bar(self, close, code):
        super().handle_bar(close, code=self.trade_code)

    def buy(self, close, num, code):
        super().buy(close, num, code=self.trade_code)

    def sell(self, close, num, code):
        super().sell(close, num, code=self.trade_code)

    def buy_short(self, close, num, code):
        super().buy_short(close, num, code=self.trade_code)

    def sell_short(self, close, num, code):
        super().sell_short(close, num, code=self.trade_code)

    # 策略实现部分
    def start(self):
        cal_length = 29
        for i in range(self.data_length):
            if i >= cal_length:
                close = self.data.loc[i-29:i, 'C_'].values
                close = scale.transform(close.reshape(-1,1))
                predicted = model(torch.FloatTensor(close.reshape(-1, 30, 1)).to(device))
                if predicted.cpu().detach().numpy() > close[-1] * (1+1/100):
                    if self.sell_holding > 0:
                        self.sell_short(self.data.loc[i, 'C_'], self.sell_holding, code=self.trade_code)
                    if self.holding <= 10:
                        self.buy(self.data.loc[i, 'C_'], 5, code=self.trade_code)
                if predicted.cpu().detach().numpy() < close[-1] * (1-1/100):
                    if self.holding > 0:
                        self.sell(self.data.loc[i, 'C_'], self.holding, code=self.trade_code)
                    if self.sell_holding <= 10:
                        self.buy_short(self.data.loc[i, 'C_'], 5, code=self.trade_code)
            self.handle_bar(close=self.data.loc[i, 'C_'], code=self.trade_code)

    def after(self):
        self.log.to_csv(name+'_log.csv')
        self.handle_log.to_csv(name+'_handle_log.csv')


aa = Test(file)
aa.start()
aa.after()
print('over')




