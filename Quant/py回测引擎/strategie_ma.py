import read_data
import test_engine
import os

# 当前文件名
name = os.path.split(__file__)[-1][:-3]
# 加载历史数据
file = read_data.file
# 品种代码
trade_code = read_data.code


class Test(test_engine.BackTest):
    def __init__(self, data):
        super().__init__(data)
        self.trade_code = trade_code

    def handle_bar(self, close, code):
        super().handle_bar(close, code=self.trade_code)

    def buy(self, close, num, code):
        super().buy(close, num, code=self.trade_code)

    def sell(self, close, num, code):
        super().sell(close, num, code=self.trade_code)

    # 策略实现部分
    def start(self):
        cal_length = 60
        for i in range(self.data_length):
            if i > cal_length:
                close = self.data.loc[i-cal_length:i, 'C_']
                ma5_last = close[-5-1:-1].mean()
                ma5 = close[-5:].mean()
                ma60_last = close[-60-1:-1].mean()
                ma60 = close[-60:].mean()
                if ma5 > ma60 and ma5_last < ma60_last and self.holding == 0:
                    self.buy(self.data.loc[i, 'C_'], 1, code=self.trade_code)
                if ma5 < ma60 and ma5_last > ma60_last and self.holding > 0:
                    self.sell(self.data.loc[i, 'C_'], 1, code=self.trade_code)
            self.handle_bar(close=self.data.loc[i, 'C_'], code=self.trade_code)

    def after(self):
        self.log.to_csv(name+'_log.csv')
        self.handle_log.to_csv(name+'_handle_log.csv')


aa = Test(file)
aa.start()
aa.after()
print('over')

