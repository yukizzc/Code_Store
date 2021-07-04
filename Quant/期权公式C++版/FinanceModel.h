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
	double m_TimeStep;//ʱ�䲽��
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

//������������֮�������
//y1=��ʼ���YYYY
int TimeDruation2Days(int y1, int m1, int d1, int y2, int m2, int d2);

//������������֮�������,ֻ���㹤����
//y1=��ʼ���YYYY
double TimeDruation2Years(int y1, int m1, int d1, int y2, int m2, int d2);

//������̬�ֲ��ܶȺ���ֵN'(x)
double NormsDistDensity(double x);

//������̬�ֲ�����ֵN(x)
double NormsDistValue(double x);

//������ʷ������
double GetVolatility(double *list, int count);

//��������������
//direct=Ȩ֤����0-CALL,1-PUT,type=Ȩ֤����0-��Ʊ��Ȩ��1-��ָ��Ȩ��2-�ڻ���Ȩ
//stockprice=��ǰ�����۸�strikeprice=Ȩ֤��Ȩ�۸�
//volatility=�������ʷ�����ʣ�r=�޷������ʣ�t=��Ȩ���ޣ�����Ϊ��λ
//optionprive=��ǰ��Ȩ�۸�
//����ֵ����Ȩ���������ʣ�<0��ʾ����ʧ��
double GetImpliedVolatility(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t, double optionprice);

//��B-Sģ�ͼ���һ��ŷʽ��Ȩ�����ۼ۸񣬹�Ʊ��Ȩ�͹�ָ��Ȩ�ļ����ж������ǹ�ϢӰ��
//direct=Ȩ֤����0-CALL,1-PUT,type=Ȩ֤����0-��Ʊ��Ȩ��1-��ָ��Ȩ��2-�ڻ���Ȩ
//stockprice=��ǰ�����۸�strikeprice=Ȩ֤��Ȩ�۸�
//volatility=�������ʷ�����ʣ�r=�޷������ʣ�t=��Ȩ���ޣ�����Ϊ��λ
//����ֵ����Ȩ���ۼ۸�<0��ʾ����ʧ��
double GetOptionBSPrice(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t);

//����һ��ŷʽ��Ȩ��Deltaֵ
//direct=Ȩ֤����0-CALL,1-PUT,type=Ȩ֤����0-��Ʊ��Ȩ��1-��ָ��Ȩ��2-�ڻ���Ȩ
//stockprice=��ǰ�����۸�strikeprice=Ȩ֤��Ȩ�۸�
//volatility=�������ʷ�����ʣ�r=�޷������ʣ�t=��Ȩ���ޣ�����Ϊ��λ
//����ֵ����ȨDelta
double GetOptionDelta(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t);

//����һ��ŷʽ��Ȩ��Thetaֵ����Ʊ��Ȩ�͹�ָ��Ȩ�ļ����ж������ǹ�ϢӰ��
//direct=Ȩ֤����0-CALL,1-PUT,type=Ȩ֤����0-��Ʊ��Ȩ��1-��ָ��Ȩ��2-�ڻ���Ȩ
//stockprice=��ǰ�����۸�strikeprice=Ȩ֤��Ȩ�۸�
//volatility=�������ʷ�����ʣ�r=�޷������ʣ�t=��Ȩ���ޣ�����Ϊ��λ
//����ֵ��Thetaֵ
double GetOptionTheta(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t);

//����һ��ŷʽ��Ȩ��Gammaֵ����Ʊ��Ȩ�͹�ָ��Ȩ�ļ����ж������ǹ�ϢӰ��
//direct=Ȩ֤����0-CALL,1-PUT,type=Ȩ֤����0-��Ʊ��Ȩ��1-��ָ��Ȩ��2-�ڻ���Ȩ
//stockprice=��ǰ�����۸�strikeprice=Ȩ֤��Ȩ�۸�
//volatility=�������ʷ�����ʣ�r=�޷������ʣ�t=��Ȩ���ޣ�����Ϊ��λ
//����ֵ��Gammaֵ
double GetOptionGamma(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t);

//����һ��ŷʽ��Ȩ��Vegaֵ����Ʊ��Ȩ�͹�ָ��Ȩ�ļ����ж������ǹ�ϢӰ��
//direct=Ȩ֤����0-CALL,1-PUT,type=Ȩ֤����0-��Ʊ��Ȩ��1-��ָ��Ȩ��2-�ڻ���Ȩ
//stockprice=��ǰ�����۸�strikeprice=Ȩ֤��Ȩ�۸�
//volatility=�������ʷ�����ʣ�r=�޷������ʣ�t=��Ȩ���ޣ�����Ϊ��λ
//����ֵ��Vegaֵ
double GetOptionVega(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t);

//����һ��ŷʽ��Ȩ��Rhoֵ����Ʊ��Ȩ�͹�ָ��Ȩ�ļ����ж������ǹ�ϢӰ��
//direct=Ȩ֤����0-CALL,1-PUT,type=Ȩ֤����0-��Ʊ��Ȩ��1-��ָ��Ȩ��2-�ڻ���Ȩ
//stockprice=��ǰ�����۸�strikeprice=Ȩ֤��Ȩ�۸�
//volatility=�������ʷ�����ʣ�r=�޷������ʣ�t=��Ȩ���ޣ�����Ϊ��λ
//����ֵ��Rhoֵ
double GetOptionRho(int direct,int type, double stockprice, double strikeprice, double volatility, double r, double t);

//�������ض���������һ����һ���۸�仯������һ���۸�֮��ĸ���
//direct=Ȩ֤����0-CALL,1-PUT,type=Ȩ֤����0-��Ʊ��Ȩ��1-��ָ��Ȩ��2-�ڻ���Ȩ
//price_from=��ĳ�ʼ�۸�,price_to=������ռ۸�,strikepriceȨ֤��Ȩ�۸�
//volatility=�۸񲨶��ʣ�t=������������ʱ��,�������
//����ֵ������������ֵĸ���
double GetPOLProbability(int direct,int type, double price_from, double price_to, double strikeprice, double volatility, double r, double t);

//�������ض���������һ����һ���۸�仯��һ���۸�Χ֮�ڵĸ���
//type=Ȩ֤����0-��Ʊ��Ȩ��1-��ָ��Ȩ��2-�ڻ���Ȩ
//price_from=��ĳ�ʼ�۸�,price_up=������ռ۸�����,price_down=������ռ۸�����
//volatility=�۸񲨶��ʣ�t=������������ʱ��,�������
//����ֵ������������ֵĸ���
double GetPIRProbability(int type, double price_from, double price_up, double price_down, double volatility, double r, double t);

#endif
