#include "stdafx.h"
#include "FinanceModel.h"
#include <math.h>

#define MAX_BTREE_STEPS	30

int dayofwk(int yy, int mm, int dd)
{
	mm -= 2;
	if( mm<=0 )	
	{ 
		mm += 12;	
		yy--; 
	}
	int temp = yy/100;
	yy %= 100;
	return (((13*mm-1)/5+dd+yy+yy/4+temp/4-temp-temp)%7+7)%7;
}

//计算两个日期之间的天数
//y1=开始年份YYYY
int TimeDruation2Days(int y1, int m1, int d1, int y2, int m2, int d2) //忽略2月29日,不倒数日期
{
	int mds[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
	
	if (y1<1900 || y2<1900 || m1<1 || m2<1 || m1>12 || m2>12 || d1<1 || d2<1)
		return 0;
	if (m1==2 && d1==29)
		d1 = 28;
	if (m2==2 && d2==29)
		d2 = 28;
	if (mds[m1-1]<d1 || mds[m2-1]<d2)
		return 0;

	int days1=(y1-1900)*365+d1;
	int days2=(y2-1900)*365+d2;
	int i;
	for (i=1; i<m1; i++)
		days1 += mds[i-1];
	for (i=1; i<m2; i++)
		days2 += mds[i-1];

	return ((days2>days1) ? (days2-days1) : 0);
}

//计算两个日期之间的年数
//y1=开始年份YYYY
double TimeDruation2Years(int y1, int m1, int d1, int y2, int m2, int d2)
{
	int dif=TimeDruation2Days(y1, m1, d1, y2, m2, d2);

	//日历日差值要转化为工作日差值
	if (dif>0)
	{
		int wk1=dayofwk(y1, m1, d1);
		int wk2=dayofwk(y2, m2, d2);
		int wks=dif/7;
		if (wk2>=wk1)
			dif = wks*5 + wk2 - wk1;
		else
			dif = wks*5 + wk2 - wk1 + 5;
	}

	return ((double)dif / 260.0);
}

//计算正态分布密度函数值N'(x)
double NormsDistDensity(double x)
{
	return exp(-x*x/2)/sqrt(2*3.141592653589);
}

//计算正态分布函数值N(x)
double NormsDistValue(double x)
{
	if (x<0)
		return (1.0 - NormsDistValue(-x));

	double a1=0.319381530;
	double a2=-0.356563782;
	double a3=1.781477937;
	double a4=-1.821255978;
	double a5=1.330274429;
	double k=1.0/(1.0+0.2316419*x);

	return (1.0 - exp(-x*x/2)/sqrt(2*3.141592653589)*(a1*k+a2*k*k+a3*pow(k,3)+a4*pow(k,4)+a5*pow(k,5)));
}

//计算数学期望
double GetAverage(double *list, int count)
{
	double sum=0.0;
	for (int i=0; i<count; i++)
		sum += list[i];
	return (count>0 ? sum/count : 0);
}

//计算历史波动率
double GetVolatility(double *p, int count)
{
	if (count<5) //数据太少不值得计算
		return 0;

	int i;
	double m=0.0;
	double y1=0.0, y2=0.0;

	for (i=1; i<count; i++)
	{
		m = p[i-1]>0 ? log(p[i]/p[i-1]) : 0;
		y1 += m;
		y2 += m*m;
	}

	count--;
	double d1_2 = y2/(count-1) - y1*y1/count/(count-1);

	//按一年250个交易日计算
	return sqrt(d1_2 * 250);
}

//用B-S模型计算一个欧式期权的理论价格，股票期权和股指期权的计算中都不考虑股息影响
//direct=权证方向，0-CALL,1-PUT,type=权证类型0-股票期权，1-股指期权，2-期货期权
//stockprice=当前标的物价格，strikeprice=权证行权价格，
//volatility=标的物历史波动率，r=无风险利率，t=期权期限，以年为单位
//返回值：期权理论价格，<0表示计算失败
double GetOptionBSPrice(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t)
{
	double sp=-1.0;
	double d1,d2;

	if (stockprice<=0 || strikeprice<=0 || t<=0 || volatility<=0)
		return -1.0;

	if (type!=OPTION_STOCK) //股指期权和期货期权模型相同
	{
		d1 = (log(stockprice/strikeprice) + volatility*volatility*t/2) / (volatility*sqrt(t));
		d2 = d1 -volatility*sqrt(t);
		if (direct!=OPTION_CALL) //认沽期权
		{
			sp = exp(-r*t)*(strikeprice*NormsDistValue(-d2) - stockprice*NormsDistValue(-d1));
		}
		else //认购期权
		{
			sp = exp(-r*t)*(stockprice*NormsDistValue(d1) - strikeprice*NormsDistValue(d2));
		}
	}
	else
	{
		d1 = (log(stockprice/strikeprice) + (r+volatility*volatility/2)*t) / (volatility*sqrt(t));
		d2 = d1 -volatility*sqrt(t);
		if (direct!=OPTION_CALL) //认沽期权
		{
			sp = exp(-r*t)*strikeprice*NormsDistValue(-d2) - stockprice*NormsDistValue(-d1);
		}
		else //认购期权
		{
			sp = stockprice*NormsDistValue(d1) - exp(-r*t)*strikeprice*NormsDistValue(d2);
		}
	}

	return sp;
}


//计算隐含波动率
//direct=权证方向，0-CALL,1-PUT,type=权证类型0-股票期权，1-股指期权，2-期货期权
//stockprice=当前标的物价格，strikeprice=权证行权价格，
//volatility=标的物历史波动率，r=无风险利率，t=期权期限，以年为单位
//optionprive=当前期权价格
//返回值：期权隐含波动率，<0表示计算失败
double GetImpliedVolatility(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t, double optionprice)
{
	double v1=volatility;
	double v2=volatility;
	double vr=volatility;
	double op=GetOptionBSPrice(direct, type, stockprice, strikeprice, volatility, r, t);
	int count = 0;

	//确定一个寻找范围
	if (op>optionprice) //隐含波动率较历史波动率低
	{
		v1 = 0.0001;
	}
	else if (op<optionprice) //隐含波动率较历史波动率高
	{
		do 
		{
			v2 = v2*2+0.0001;
			op=GetOptionBSPrice(direct, type, stockprice, strikeprice, v2, r, t);
			count++;
		} while(op<optionprice && count<=30);
	}
	else
		return volatility;

	double dif = 1.0;
	count = 0;

	while ( dif>0.0001 && count<1000 )
	{
		count++;
		vr = (v1+v2)/2;
		op=GetOptionBSPrice(direct, type, stockprice, strikeprice, vr, r, t);
		dif = fabs(op - optionprice);
		if ( op<optionprice )
		{
			v1 = vr;	
		}
		else
		{
			v2 = vr;
		}
	}

	return vr;
}

//计算一个欧式期权的Delta值
//direct=权证方向，0-CALL,1-PUT,type=权证类型0-股票期权，1-股指期权，2-期货期权
//stockprice=当前标的物价格，strikeprice=权证行权价格，
//volatility=标的物历史波动率，r=无风险利率，t=期权期限，以年为单位
//返回值：期权Delta
double GetOptionDelta(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t)
{
	double delta=1.0;
	double d1;

	if (stockprice<=0 || strikeprice<=0 || t<=0 || volatility<=0)
		return 1.0;

	if (type!=OPTION_STOCK) //股指期权和期货期权模型相同
	{
		d1 = (log(stockprice/strikeprice) + volatility*volatility*t/2) / (volatility*sqrt(t));
		if (direct!=OPTION_CALL) //认沽期权
		{
			delta = exp(-r*t)*(NormsDistValue(d1)-1);
		}
		else //认购期权
		{
			delta = exp(-r*t)*NormsDistValue(d1);
		}
	}
	else
	{
		d1 = (log(stockprice/strikeprice) + (r+volatility*volatility/2)*t) / (volatility*sqrt(t));
		if (direct!=OPTION_CALL) //认沽期权
		{
			delta = NormsDistValue(d1)-1;
		}
		else //认购期权
		{
			delta = NormsDistValue(d1);
		}
	}

	return delta;
}

//计算一个欧式期权的Theta值，股票期权和股指期权的计算中都不考虑股息影响
//direct=权证方向，0-CALL,1-PUT,type=权证类型0-股票期权，1-股指期权，2-期货期权
//stockprice=当前标的物价格，strikeprice=权证行权价格，
//volatility=标的物历史波动率，r=无风险利率，t=期权期限，以年为单位
//返回值：Theta值
double GetOptionTheta(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t)
{
	double theta=0.0;
	double d1,d2;

	if (stockprice<=0 || strikeprice<=0 || t<=0 || volatility<=0)
		return 0;

	if (type!=OPTION_STOCK) //股指期权和期货期权模型相同
	{
		d1 = (log(stockprice/strikeprice) + volatility*volatility*t/2) / (volatility*sqrt(t));
		d2 = d1 -volatility*sqrt(t);
		if (direct!=OPTION_CALL) //认沽期权
		{
			theta = (-stockprice*NormsDistDensity(d1)*volatility*exp(-r*t))/2.0/sqrt(t)
					- r*stockprice*NormsDistValue(d1)*exp(-r*t)
					+ r*strikeprice*exp(-r*t)*NormsDistValue(d2);
		}
		else //认购期权
		{
			theta = (-stockprice*NormsDistDensity(d1)*volatility*exp(-r*t))/2.0/sqrt(t)
					+ r*stockprice*NormsDistValue(d1)*exp(-r*t)
					- r*strikeprice*exp(-r*t)*NormsDistValue(d2);
		}
	}
	else
	{
		d1 = (log(stockprice/strikeprice) + (r+volatility*volatility/2)*t) / (volatility*sqrt(t));
		d2 = d1 -volatility*sqrt(t);
		if (direct!=OPTION_CALL) //认沽期权
		{
			theta = (-stockprice*NormsDistDensity(d1)*volatility)/2.0/sqrt(t)
					+ r*strikeprice*exp(-r*t)*NormsDistValue(d2);
		}
		else //认购期权
		{
			theta = (-stockprice*NormsDistDensity(d1)*volatility)/2.0/sqrt(t)
					- r*strikeprice*exp(-r*t)*NormsDistValue(d2);
		}
	}

	return theta;
}

//计算一个欧式期权的Gamma值，股票期权和股指期权的计算中都不考虑股息影响
//direct=权证方向，0-CALL,1-PUT,type=权证类型0-股票期权，1-股指期权，2-期货期权
//stockprice=当前标的物价格，strikeprice=权证行权价格，
//volatility=标的物历史波动率，r=无风险利率，t=期权期限，以年为单位
//返回值：Gamma值
double GetOptionGamma(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t)
{
	double gamma=0.0;
	double d1;

	if (stockprice<=0 || strikeprice<=0 || t<=0 || volatility<=0)
		return 0;

	if (type!=OPTION_STOCK) //股指期权和期货期权模型相同
	{
		d1 = (log(stockprice/strikeprice) + volatility*volatility*t/2) / (volatility*sqrt(t));
		gamma = NormsDistDensity(d1)*exp(-r*t)/stockprice/volatility/sqrt(t);
	}
	else
	{
		d1 = (log(stockprice/strikeprice) + (r+volatility*volatility/2)*t) / (volatility*sqrt(t));
		gamma = NormsDistDensity(d1)/stockprice/volatility/sqrt(t);
	}

	return gamma;
}

//计算一个欧式期权的Vega值，股票期权和股指期权的计算中都不考虑股息影响
//direct=权证方向，0-CALL,1-PUT,type=权证类型0-股票期权，1-股指期权，2-期货期权
//stockprice=当前标的物价格，strikeprice=权证行权价格，
//volatility=标的物历史波动率，r=无风险利率，t=期权期限，以年为单位
//返回值：Vega值
double GetOptionVega(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t)
{
	double vega=0.0;
	double d1;

	if (stockprice<=0 || strikeprice<=0 || t<=0 || volatility<=0)
		return 0;

	if (type!=OPTION_STOCK) //股指期权和期货期权模型相同
	{
		d1 = (log(stockprice/strikeprice) + volatility*volatility*t/2) / (volatility*sqrt(t));
		vega = stockprice * sqrt(t) * NormsDistDensity(d1) * exp(-r*t);
	}
	else
	{
		d1 = (log(stockprice/strikeprice) + (r+volatility*volatility/2)*t) / (volatility*sqrt(t));
		vega = stockprice * sqrt(t) * NormsDistDensity(d1);
	}

	return vega;
}

//计算一个欧式期权的Rho值，股票期权和股指期权的计算中都不考虑股息影响
//direct=权证方向，0-CALL,1-PUT,type=权证类型0-股票期权，1-股指期权，2-期货期权
//stockprice=当前标的物价格，strikeprice=权证行权价格，
//volatility=标的物历史波动率，r=无风险利率，t=期权期限，以年为单位
//返回值：Rho值
double GetOptionRho(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t)
{
	double rho=0.0;
	double d1,d2;

	if (stockprice<=0 || strikeprice<=0 || t<=0 || volatility<=0)
		return 0;

	if (type!=OPTION_STOCK) //股指期权和期货期权模型相同
	{
		d1 = (log(stockprice/strikeprice) + volatility*volatility*t/2) / (volatility*sqrt(t));
		d2 = d1 -volatility*sqrt(t);
	}
	else
	{
		d1 = (log(stockprice/strikeprice) + (r+volatility*volatility/2)*t) / (volatility*sqrt(t));
		d2 = d1 -volatility*sqrt(t);
	}
	if (direct!=OPTION_CALL) //认沽期权
		rho	 = -strikeprice * t * exp(-r*t) * NormsDistValue(-d2);
	else //认购期权
		rho	 = strikeprice * t * exp(-r*t) * NormsDistValue(d2);

	return rho;
}

//计算在特定波动率下一个从一个价格变化到另外一个价格之外的概率
//direct=权证方向，0-CALL,1-PUT,type=权证类型0-股票期权，1-股指期权，2-期货期权
//price_from=标的初始价格,price_to=标的最终价格,strikeprice权证行权价格
//volatility=价格波动率，t=过程所经历的时间,按年计算
//返回值：这种情况出现的概率
double GetPOLProbability(int direct,int type, double price_from, double price_to, double strikeprice, double volatility, double r, double t)
{
	double p=0.0;

	if (price_from<=0 || price_to<=0 || t<=0 || volatility<=0)
		return 0.0;
//	double delta = GetOptionDelta(direct, type, price_from, price_to, volatility, r, t);
	double delta = GetOptionDelta((price_to>=price_from)?OPTION_CALL:OPTION_PUT, type, price_from, price_to, volatility, r, t);
	p = fabs(delta);

	return p;
}


//计算在特定波动率下一个从一个价格变化到一个价格范围之内的概率
//type=权证类型0-股票期权，1-股指期权，2-期货期权
//price_from=标的初始价格,price_up=标的最终价格上限,标的最终价格下限
//volatility=价格波动率，t=过程所经历的时间,按年计算
//返回值：这种情况出现的概率
double GetPIRProbability(int type, double price_from, double price_up, double price_down, double volatility, double r, double t)
{
	double p=0.0;

	if (price_from<=0 || price_up<=0 || price_down<=0 || t<=0 || volatility<=0)
		return 0.0;

	double p1 = GetOptionDelta(OPTION_CALL, type, price_from, price_down, volatility, r, t);
	double p2 = GetOptionDelta(OPTION_PUT, type, price_from, price_up, volatility, r, t);
	p = fabs(p1) + fabs(p2) - 1.0;
	return max(p , 0.0);
}

//----------------------------------------------------------------------------------------------------
int COptionBinominalTree::m_CalcCount = 0;
BOOL	COptionBinominalTree::m_Stop = FALSE;
COptionBinominalTree::COptionBinominalTree(int direct, int type, int attr, double strikeprice, double stockprice, double t, double volatility, double r, int steps)
{
	m_Status		= 0;
	m_Direct		= direct;
	m_Type			= type;
	m_Attr			= attr;
	m_StockPrice	= stockprice;
	m_StrikePrice	= strikeprice;
	m_Volatility	= max(volatility, 0.0001);
	m_RiskfreeRate	= r;
	m_ErrorCode		= 0;
	m_UpperTree		= NULL;
	m_DownTree		= NULL;
	m_Steps			= steps>1 ? steps : 1;
	if (m_Steps>MAX_BTREE_STEPS)
		m_Steps	= MAX_BTREE_STEPS;

	m_TimeStep		= t/m_Steps;

	m_Stop = FALSE;
}


COptionBinominalTree::COptionBinominalTree()
{
	m_Status		= 0;
	m_ErrorCode		= 0;
	m_UpperTree		= NULL;
	m_DownTree		= NULL;


}

void COptionBinominalTree::SetPara(int direct, int type, int attr, double strikeprice, double stockprice, double t, double volatility, double r, int steps)
{
	m_Direct		= direct;
	m_Type			= type;
	m_Attr			= attr;
	m_StockPrice	= stockprice;
	m_StrikePrice	= strikeprice;
	m_Volatility	= max(volatility, 0.0001);
	m_RiskfreeRate	= r;
	m_Steps			= steps;
	m_TimeStep		= t;

	
}

void COptionBinominalTree::SetParaEx(int direct, int type, int attr, double strikeprice, double stockprice, double t, double volatility, double r, int steps)
{
	m_Status		= 0;
	m_Direct		= direct;
	m_Type			= type;
	m_Attr			= attr;
	m_StockPrice	= stockprice;
	m_StrikePrice	= strikeprice;
	m_Volatility	= max(volatility, 0.0001);
	m_RiskfreeRate	= r;
	m_ErrorCode		= 0;
	m_UpperTree		= NULL;
	m_DownTree		= NULL;
	m_Steps			= steps>1 ? steps : 1;
	if (m_Steps>MAX_BTREE_STEPS)
		m_Steps	= MAX_BTREE_STEPS;

	m_TimeStep		= t/m_Steps;


}

COptionBinominalTree::~COptionBinominalTree()
{
	Free();
}

double COptionBinominalTree::GetOptionPrice( double *pCalcCount, void *pvoid )
{
	if( m_Stop ) return 0;
	
//	MSG msg;
//	while(::PeekMessage(&msg,NULL,0,0,PM_REMOVE)) 
//	{
//		::TranslateMessage(&msg);
//		::DispatchMessage(&msg);
//	}

	double npp  = CalcNPOptionPrice(m_Direct, m_StockPrice, m_StrikePrice);
	double price= 0;
	
	if (m_Steps<=0)//最底层叶子，直接计算期权价格
	{
		return npp;
	}
	else
	{
		m_CalcCount++;
		(*pCalcCount) ++;
		if (m_CalcCount>10000)
		{
			m_CalcCount = 0;

		}
		m_Status = 1;
		double u = exp(m_Volatility*sqrt(m_TimeStep));
		double d = 1.0/u;
		double upperprice = m_StockPrice*u;
		double downprice  = m_StockPrice*d;
		double p = 1.0;
		if (m_Type!=OPTION_STOCK)
			p = (1-d) / (u-d);
		else
			p = (exp(m_RiskfreeRate*m_TimeStep)-d) / (u-d);

		//先构造上涨子树，并计算出期权费用
		m_UpperTree = new COptionBinominalTree();
		if (m_UpperTree!=NULL)
		{
			m_UpperTree->SetPara(m_Direct, m_Type, m_Attr, m_StrikePrice, upperprice, m_TimeStep, m_Volatility, m_RiskfreeRate, m_Steps-1);
			upperprice = m_UpperTree->GetOptionPrice( pCalcCount, pvoid);
			//计算好了就释放内存
			m_UpperTree->Free();
		}
		else
			upperprice = 0;
		//然后构造下跌子树，并计算期权费
		m_DownTree  = new COptionBinominalTree();
		if (m_DownTree!=NULL)
		{
			m_DownTree->SetPara(m_Direct, m_Type, m_Attr, m_StrikePrice, downprice, m_TimeStep, m_Volatility, m_RiskfreeRate, m_Steps-1);
			downprice = m_DownTree->GetOptionPrice( pCalcCount, pvoid );
			//计算好了就释放内存
			m_DownTree->Free();
		}
		else
			downprice = 0;

		price = exp(-m_RiskfreeRate*m_TimeStep)*(p*upperprice + (1.0-p)*downprice);

		if (m_Attr==OPTION_AMERICA) //对于美式期权，有行权价值的期权必然马上行权，期权费会变得更贵
		{
			price = max(price, npp);
		}

		m_Status = 0;
		return price;
	}
}

int COptionBinominalTree::GetLastError()
{
	return m_ErrorCode;
}


bool COptionBinominalTree::Free()
{
	if (m_UpperTree!=NULL)
	{
		m_UpperTree->Free();
		delete m_UpperTree;
		m_UpperTree = NULL;
	}
	if (m_DownTree!=NULL)
	{
		m_DownTree->Free();
		delete m_DownTree;
		m_DownTree = NULL;
	}

	return true;
}

double COptionBinominalTree::CalcNPOptionPrice(int direct, double stockprice, double strikeprice)
{
	if (direct==OPTION_PUT) //认沽
		return max(strikeprice-stockprice, 0);
	else//认购
		return max(stockprice-strikeprice, 0);
}

