#标准行情api
from pytdx.hq import TdxHq_API
#扩展行情api
from pytdx.exhq import TdxExHq_API
# 我们可以使用 TDXParams.MARKET_SH , TDXParams.MARKET_SZ
from pytdx.params import TDXParams
import pandas as pd
class exhq():
    def __init__(self,market, code, date,start = None ,ip = '140.207.226.39', port = 7722):
        self.market = market
        self.code = code
        self.date = date
        self.start = start
        self.api = TdxExHq_API()
        connect = self.api.connect(ip,port)
    #历史分笔
    def get_history_tick(self):
        data = self.api.get_history_transaction_data(code=self.code,market=self.market,date=self.date,start=self.start)
        df = pd.DataFrame(data)
        return df


if __name__ == '__main__':
    ob = exhq(30, "RB1901", 20181126, 8000, '140.207.226.39',7722)
    get = ob.get_history_tick()
    print(get)

    
    
