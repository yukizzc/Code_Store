'''
对于读取文件有要求，excel中如下表示，三列如下
日期	        DATE_ARRAY	PRICE
2005/2/23	20050223	0.696
2005/2/24	20050224	0.696
2005/2/25	20050225	0.699
2005/2/28	20050228	0.693
2005/3/1	20050301	0.689
2005/3/2	20050302	0.682
2005/3/3	20050303	0.682

'''
#分割数量,用户填写
num = 50
#相关性排名前num
sort_num = 10
import numpy as np
a = np.array([1,2,3,4])
#[0,1,2,3]分成01,12,23这种模式，k是分割数量
def slip(a,k):
    li = []
    for i in range(len(a)):
        if i<=k-1:
            continue
        else:
            li.append(a[i-k:i])
    return np.array(li)

import pandas as pd
#打开数据文件，金字塔中输出
file = pd.read_excel(r'C:\Users\yukizzc\PycharmProjects\Maching_Learning\test\tt.xlsx')
df = file.iloc[:,1:3]

#最新待测试数据
test_data = df[-num:]['PRICE'].values
#历史所有数据，不包含今天
train_data = df[:]
#进行数据分割
data = slip(train_data['PRICE'].values, num)

pd_data = pd.DataFrame(data.T)
pd_data.insert(0,'now',test_data)
corr = pd_data.corr()
#right是正相关排序，now是最新数据
right_corr = corr.sort_values(['now'],ascending=False)
left_corr = corr.sort_values(['now'],ascending=True)
#将结果输出文件
def to_file():
    filename = r'C:\Users\yukizzc\PycharmProjects\Maching_Learning\test\result.csv'
    with open(filename,'a+') as f:
        right_corr.to_csv(filename)
to_file()
#输出排名前几的index，再根据index返回相应日期,注意日期是数据起点不是终点，所以在今天的num周期内相似度是无意义的
sort_index = right_corr['now'][1:sort_num].index
print(train_data.loc[sort_index]['DATE_ARRAY'])
