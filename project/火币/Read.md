火币官网：https://huobiapi.github.io/docs/dm/v1/cn/#5ea2e0cde2

==**交割合约**==：用的symbol这个字段加上本周次周这种。如"BTC_CW"表示BTC当周合约，"BTC_NW"表示BTC次周合约，"BTC_CQ"表示BTC当季合约 , "BTC_NQ"表示次季度合约

**==币本位永续合约==**：用的是contract_code，比如BTC-USDT

**==USDT本位永续合约==**：用的是contract_code参数名，比如BTC-USDT



工程文件说明：

**原始的火币程序**

ft.py、ft2.py、ft3.py分别对应开头三种市场里币的数据获取，主要用来检验用

get_code.py 是用来获取合约信息的



**python程序**

这里面主要是用来存入数据库的，先执行creat_tables.py建立表（数据库自己手工创建）

然后get_data.py接受数据并入库（同时sub的币种不能太多，可能要分成多个进程去执行）



**金字塔的python程序**

在金字塔中利用py去读取mysql数据，（前面入库时候用的update方式只保留最新的数据）

之所以这么设计还是在于金字塔自己的python遇到网络问题就直接报错弹出了，自动重连有bug

这个读取数据会去调用vba程序



**vba工程**

首先creat_code要在软件中建立合约信息，手工添加市场

然后自定义的function是由上面的金字塔python程序去调用