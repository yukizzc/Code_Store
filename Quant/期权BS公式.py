from math import log,sqrt,exp
from scipy import stats


class option():
    #参数分别表示
    #标的价，行权价，无风险利率，到期天数，波动率，期权最新价，call_put为0表示认购，为1表示认沽
    def __init__(self,s,k,r,t,sigma,close,call_put='call'):
        self.s = s
        self.k = k
        self.r = r
        self.T = t/365
        self.sigma = sigma
        self.close = close
        self.call_put = call_put.lower()
        self.d1 = (log(self.s / self.k) + (self.r + 1 / 2 * self.sigma ** 2) * self.T) / (self.sigma * sqrt(self.T))
    #BS定价公式，返回期权理论价
    def call(self):
        '''
        st,k,r,T,sigma(T以年为单位，天数应该除以365)
        '''
        d1 = self.d1
        d2 = d1 - self.sigma * sqrt(self.T)
        call = self.s * stats.norm.cdf(d1, 0.0, 1.0) - self.k * exp(-self.r * self.T) * stats.norm.cdf(d2, 0.0, 1.0)
        return call
    def put(self):
        '''
        st,k,r,T,sigma(T以年为单位，天数应该除以365)
        '''
        d1 = self.d1
        d2 = d1 - self.sigma * sqrt(self.T)
        put = self.k * exp(-self.r * self.T) * stats.norm.cdf(-1 * d2) - 1 * self.s * stats.norm.cdf(-1 * d1)
        return put
    #获得delta
    def delta(self):
        '''
        n默认为1看涨期权的delta
        n为-1为看跌期权的delta
        '''
        if self.call_put == 'call':
            n = 1
        else:
            n = -1
        d1 = self.d1
        delta = n * stats.norm.cdf(n * d1)
        return delta

    # 获得gamma
    def gamma(self):
        d1 = self.d1
        gamma = stats.norm.pdf(d1) / (self.s * self.sigma * sqrt(self.T))
        return gamma

    # 获得theta
    def theta(self):
        '''
        n默认为1看涨期权的delta
        n为-1为看跌期权的delta
        '''
        if self.call_put == 'call':
            n = 1
        else:
            n = -1
        d1 = self.d1
        d2 = d1 - self.sigma * sqrt(self.T)
        theta = -1 * (self.s * stats.norm.pdf(d1) * self.sigma) / (2 * sqrt(self.T)) - n * self.r * self.k * exp(-self.r * self.T) * stats.norm.cdf(n * d2)
        return theta

    # 获得veag
    def vega(self):
        d1 = self.d1
        vega = self.s * sqrt(self.T) * stats.norm.pdf(d1)
        return vega
    #牛顿法迭代求隐含波动率
    def imp_vol_newton(self, sigma_est=1, it=100):


        if self.call_put == 'call':
            for i in range(it):
                d1 = (log(self.s / self.k) + (self.r + 1 / 2 * sigma_est ** 2) * self.T) / (sigma_est * sqrt(self.T))
                d2 = d1 - sigma_est * sqrt(self.T)
                call = self.s * stats.norm.cdf(d1, 0.0, 1.0) - self.k * exp(-self.r * self.T) * stats.norm.cdf(d2, 0.0,1.0)
                vega = self.s * sqrt(self.T) * stats.norm.pdf(d1)
                sigma_est -= (call - self.close) /vega
            return sigma_est
        else:
            for i in range(it):
                d1 = (log(self.s / self.k) + (self.r + 1 / 2 * sigma_est ** 2) * self.T) / (sigma_est * sqrt(self.T))
                d2 = d1 - sigma_est * sqrt(self.T)
                put = self.k * exp(-self.r * self.T) * stats.norm.cdf(-1 * d2) - 1 * self.s * stats.norm.cdf(-1 * d1)
                vega = self.s * sqrt(self.T) * stats.norm.pdf(d1)
                sigma_est -= (put - self.close) /vega
            return sigma_est

    # 二分法求隐含波动率
    def imp_vol_dichotomy(self):
        c_est = 0
        top = 3  # 波动率上限
        floor = 0  # 波动率下限
        sigma = (floor + top) / 2  # 波动率初始值
        if self.call_put == 'call':
            while abs(self.close - c_est) > 1e-8:
                d1 = (log(self.s / self.k) + (self.r + 1 / 2 * sigma ** 2) * self.T) / (sigma * sqrt(self.T))
                d2 = d1 - sigma * sqrt(self.T)
                call = self.s * stats.norm.cdf(d1, 0.0, 1.0) - self.k * exp(-self.r * self.T) * stats.norm.cdf(d2, 0.0,1.0)
                c_est = call
                # 根据价格判断波动率是被低估还是高估，并对波动率做修正
                if self.close - c_est > 0:  # f(x)>0
                    floor = sigma
                    sigma = (sigma + top) / 2
                else:
                    top = sigma
                    sigma = (sigma + floor) / 2
            return sigma
        else:
            while abs(self.close - c_est) > 1e-8:
                d1 = (log(self.s / self.k) + (self.r + 1 / 2 * sigma ** 2) * self.T) / (sigma * sqrt(self.T))
                d2 = d1 - sigma * sqrt(self.T)
                put = self.k * exp(-self.r * self.T) * stats.norm.cdf(-1 * d2) - 1 * self.s * stats.norm.cdf(-1 * d1)
                c_est = put
                # 根据价格判断波动率是被低估还是高估，并对波动率做修正
                if self.close - c_est > 0:  # f(x)>0
                    floor = sigma
                    sigma = (sigma + top) / 2
                else:
                    top = sigma
                    sigma = (sigma + floor) / 2
            return sigma
parameter = {}
parameter['标的价格'] = 2.724
parameter['行权价'] = 2.7
parameter['无风险利率'] = 0.044
parameter['到期天数'] = 218
parameter['历史波动率'] = 0.2668
parameter['期权最新价'] = 0.2236
parameter['call_put'] = 'call'


p1 = option(parameter['标的价格'],parameter['行权价'],parameter['无风险利率'],parameter['到期天数'],parameter['历史波动率'],parameter['期权最新价'],parameter['call_put'])
print(p1.imp_vol_newton(),p1.imp_vol_dichotomy())