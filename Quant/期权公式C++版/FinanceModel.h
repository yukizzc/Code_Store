#ifndef	__FINANCEMODEL_H__
#define __FINANCEMODEL_H__

typedef enum
{
	OPTION_STOCK=0,
	OPTION_INDEX,
	OPTION_FUTURE,
} OPTION_TYPE;

typedef enum
{
	OPTION_CALL=0,
	OPTION_PUT,
} OPTION_DIRECT;

typedef enum
{
	OPTION_AMERICA=0,
	OPTION_EURO,
} OPTION_ATTR;

class COptionBinominalTree
{
public:
	COptionBinominalTree(int direct, int type, int attr, double strikeprice, double stockprice, double t, double volatility, double r, int steps=1);
	COptionBinominalTree();
	~COptionBinominalTree();
	double GetOptionPrice( double *pCalcCount, void *pvoid );
	int GetLastError();
	int GetStatus();
	void SetParaEx(int direct, int type, int attr, double strikeprice, double stockprice, double t, double volatility, double r, int steps);
	static void Stop( BOOL bStop = TRUE ) { m_Stop = bStop; };
protected:
	int m_Direct, m_Type, m_Attr, m_Steps;
	double m_StockPrice, m_StrikePrice;
	double m_Volatility, m_RiskfreeRate;
	double m_TimeStep;//时间步长
	int m_Status;
	int m_ErrorCode;
	static int m_CalcCount;
	static BOOL	m_Stop;
	COptionBinominalTree *m_UpperTree, *m_DownTree;
protected:
	
	void SetPara(int direct, int type, int attr, double strikeprice, double stockprice, double t, double volatility, double r, int steps);
	bool Free();
	double CalcNPOptionPrice(int direct, double stockprice, double strikeprice);
};

//计算两个日期之间的天数
//y1=开始年份YYYY
int TimeDruation2Days(int y1, int m1, int d1, int y2, int m2, int d2);

//计算两个日期之间的年数,只计算工作日
//y1=开始年份YYYY
double TimeDruation2Years(int y1, int m1, int d1, int y2, int m2, int d2);

//计算正态分布密度函数值N'(x)
double NormsDistDensity(double x);

//计算正态分布函数值N(x)
double NormsDistValue(double x);

//计算历史波动率
double GetVolatility(double *list, int count);

//计算隐含波动率
//direct=权证方向，0-CALL,1-PUT,type=权证类型0-股票期权，1-股指期权，2-期货期权
//stockprice=当前标的物价格，strikeprice=权证行权价格，
//volatility=标的物历史波动率，r=无风险利率，t=期权期限，以年为单位
//optionprive=当前期权价格
//返回值：期权隐含波动率，<0表示计算失败
double GetImpliedVolatility(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t, double optionprice);

//用B-S模型计算一个欧式期权的理论价格，股票期权和股指期权的计算中都不考虑股息影响
//direct=权证方向，0-CALL,1-PUT,type=权证类型0-股票期权，1-股指期权，2-期货期权
//stockprice=当前标的物价格，strikeprice=权证行权价格，
//volatility=标的物历史波动率，r=无风险利率，t=期权期限，以年为单位
//返回值：期权理论价格，<0表示计算失败
double GetOptionBSPrice(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t);

//计算一个欧式期权的Delta值
//direct=权证方向，0-CALL,1-PUT,type=权证类型0-股票期权，1-股指期权，2-期货期权
//stockprice=当前标的物价格，strikeprice=权证行权价格，
//volatility=标的物历史波动率，r=无风险利率，t=期权期限，以年为单位
//返回值：期权Delta
double GetOptionDelta(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t);

//计算一个欧式期权的Theta值，股票期权和股指期权的计算中都不考虑股息影响
//direct=权证方向，0-CALL,1-PUT,type=权证类型0-股票期权，1-股指期权，2-期货期权
//stockprice=当前标的物价格，strikeprice=权证行权价格，
//volatility=标的物历史波动率，r=无风险利率，t=期权期限，以年为单位
//返回值：Theta值
double GetOptionTheta(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t);

//计算一个欧式期权的Gamma值，股票期权和股指期权的计算中都不考虑股息影响
//direct=权证方向，0-CALL,1-PUT,type=权证类型0-股票期权，1-股指期权，2-期货期权
//stockprice=当前标的物价格，strikeprice=权证行权价格，
//volatility=标的物历史波动率，r=无风险利率，t=期权期限，以年为单位
//返回值：Gamma值
double GetOptionGamma(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t);

//计算一个欧式期权的Vega值，股票期权和股指期权的计算中都不考虑股息影响
//direct=权证方向，0-CALL,1-PUT,type=权证类型0-股票期权，1-股指期权，2-期货期权
//stockprice=当前标的物价格，strikeprice=权证行权价格，
//volatility=标的物历史波动率，r=无风险利率，t=期权期限，以年为单位
//返回值：Vega值
double GetOptionVega(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t);

//计算一个欧式期权的Rho值，股票期权和股指期权的计算中都不考虑股息影响
//direct=权证方向，0-CALL,1-PUT,type=权证类型0-股票期权，1-股指期权，2-期货期权
//stockprice=当前标的物价格，strikeprice=权证行权价格，
//volatility=标的物历史波动率，r=无风险利率，t=期权期限，以年为单位
//返回值：Rho值
double GetOptionRho(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t);

//计算在特定波动率下一个从一个价格变化到另外一个价格之外的概率
//direct=权证方向，0-CALL,1-PUT,type=权证类型0-股票期权，1-股指期权，2-期货期权
//price_from=标的初始价格,price_to=标的最终价格,strikeprice权证行权价格
//volatility=价格波动率，t=过程所经历的时间,按年计算
//返回值：这种情况出现的概率
double GetPOLProbability(int direct,int type, double price_from, double price_to, double strikeprice, double volatility, double r, double t);

//计算在特定波动率下一个从一个价格变化到一个价格范围之内的概率
//type=权证类型0-股票期权，1-股指期权，2-期货期权
//price_from=标的初始价格,price_up=标的最终价格上限,price_down=标的最终价格下限
//volatility=价格波动率，t=过程所经历的时间,按年计算
//返回值：这种情况出现的概率
double GetPIRProbability(int type, double price_from, double price_up, double price_down, double volatility, double r, double t);

#endif
