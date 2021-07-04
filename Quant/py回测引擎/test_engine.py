import pandas as pd


class BackTest:
    def __init__(self, input_data):
        self.data = input_data
        '''费率设置'''
        # 初始资金
        self.money = 2 * 50000
        # 手续费默认按手
        self.fee = 0
        # 保证金率
        self.deposit = 0.13
        # 品种单位
        self.multiplier = 10
        '''系统参数'''
        # 数据序号，每次更新时候自增1
        self.data_index = 0
        # 历史数据长度
        self.data_length = len(self.data)
        '''交易信息'''
        # 仓位
        self.holding = 0
        self.sell_holding = 0
        # 持仓均价
        self.average_price = 0
        self.sell_average_price = 0
        '''日志记录'''
        # 每次交易动作记录
        self.log = pd.DataFrame(columns=['code', 'date', '开平', '数量', '价格'])
        # 每天盘后账户信息记录
        self.handle_log = pd.DataFrame(columns=['code', 'date', '动态权益', '保证金', '多头仓位',
                                                '多头均价', '多头浮盈', '空头持仓', '空头均价', '空头浮盈'])

    def handle_bar(self, close, code):
        self.handle_log = self.handle_log.append(
            {'date': self.data.loc[self.data_index, '日期'],
             'code': code,
             '多头仓位': self.holding,
             '多头均价': self.average_price,
             '多头浮盈': (close - self.average_price) * self.multiplier * self.holding,
             #######################################################################################
             '空头持仓': self.sell_holding,
             '空头均价': self.sell_average_price,
             '空头浮盈': (self.sell_average_price - close) * self.multiplier * self.sell_holding,
             # 动态权益 = self.money + 浮动盈亏
             # self.money = 可用+保证金
             '动态权益': self.money + (close - self.average_price) * self.multiplier * self.holding +
                     (self.sell_average_price - close) * self.multiplier * self.sell_holding,
             '保证金': close * (self.sell_holding + self.holding) * self.multiplier * self.deposit}, ignore_index=True)
        self.data_index += 1

    def buy(self, close, num, code):
        # 期货浮盈是可以开仓的，所以公式为:浮动盈亏 + self.money - 保证金
        fy = (close * self.holding - self.average_price * self.holding) * self.multiplier
        bzj = self.holding * close * self.deposit * self.multiplier
        if (fy + self.money - bzj) / (close * self.deposit * self.multiplier) > num:
            self.log = self.log.append({'date': self.data.loc[self.data_index, '日期'],
                                        '开平': 'buy',
                                        'code': code,
                                        '数量': num,
                                        '价格': close},
                                       ignore_index=True)
            self.money -= self.fee * num
            self.average_price = (self.average_price * self.holding + num * close) / (self.holding + num)
            self.holding += num

    def sell(self, close, num, code):
        # 非全部平仓
        if self.holding > num:
            self.log = self.log.append({'date': self.data.loc[self.data_index, '日期'],
                                        '开平': 'sell',
                                        'code': code,
                                        '数量': num,
                                        '价格': close},
                                       ignore_index=True)
            # 扣除手续费
            self.money -= self.fee * num
            # 更新成本均价
            self.average_price = (self.average_price * self.holding - num * close) / (self.holding - num)
            # 更新仓位
            self.holding -= num
        #  全部平仓的情况
        elif self.holding == num:
            self.log = self.log.append({'date': self.data.loc[self.data_index, '日期'],
                                        '开平': 'sell',
                                        'code': code,
                                        '数量': num,
                                        '价格': close},
                                       ignore_index=True)
            self.money -= self.fee * num
            self.money += (close * num - self.average_price * self.holding) * self.multiplier
            self.average_price = 0
            self.holding = 0

    def buy_short(self, close, num, code):
        # 期货浮盈是可以开仓的，所以公式为:浮动盈亏 + self.money - 保证金
        fy = (self.sell_average_price * self.sell_holding - close * self.sell_holding) * self.multiplier
        bzj = self.sell_holding * close * self.deposit * self.multiplier
        if (fy + self.money - bzj) / (close * self.deposit * self.multiplier) > num:
            self.log = self.log.append({'date': self.data.loc[self.data_index, '日期'],
                                        '开平': 'buy_short',
                                        'code': code,
                                        '数量': num,
                                        '价格': close},
                                       ignore_index=True)
            self.money -= self.fee * num
            self.sell_average_price = (self.sell_average_price * self.sell_holding + num * close) / (
                    self.sell_holding + num)
            self.sell_holding += num

    def sell_short(self, close, num, code):
        # 非全部平仓
        if self.sell_holding > num:
            self.log = self.log.append({'date': self.data.loc[self.data_index, '日期'],
                                        '开平': 'sell_short',
                                        'code': code,
                                        '数量': num,
                                        '价格': close},
                                       ignore_index=True)
            # 扣除手续费
            self.money -= self.fee * num
            # 更新成本均价
            self.sell_average_price = (self.sell_average_price * self.sell_holding - num * close) / (
                    self.sell_holding - num)
            # 更新仓位
            self.sell_holding -= num
        #  全部平仓的情况
        elif self.sell_holding == num:
            self.log = self.log.append({'date': self.data.loc[self.data_index, '日期'],
                                        '开平': 'sell_short',
                                        'code': code,
                                        '数量': num,
                                        '价格': close},
                                       ignore_index=True)
            self.money -= self.fee * num
            self.money += (self.sell_average_price * self.sell_holding - close * num) * self.multiplier
            self.sell_average_price = 0
            self.sell_holding = 0
