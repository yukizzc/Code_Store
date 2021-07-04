import numpy as np
import pandas as pd

a = np.array([[6,0,0,  7,5,9,  2,1,3],
              [0,0,0,  0,0,0,  0,0,8],
              [0,7,1,  2,6,8,  0,4,0],
              
              [8,0,0,  0,4,5,  6,0,1],
              [1,0,0,  0,0,0,  3,0,0],
              [2,0,5,  0,0,7,  9,0,0],
              
              [5,0,0,  9,2,3,  0,7,6],
              [4,0,9,  0,0,1,  0,0,0],
              [0,2,3,  4,8,0,  0,0,0]]
            )
df = pd.DataFrame(a)

# 测试看一些的代码作用的
def test():
    num_set = set(range(1,10))
    # 行数据 相比1~9缺少哪些数
    x = num_set- set(df.iloc[0,:].values)
    # 列数据，缺少哪些数据
    y = num_set- set(df.iloc[:,8].values)

# 根据pandas序号来返回其所在区域内所有的数据
def every_block(df,x,y):
    # x,y是dataframe的行列序号，从0到8
    x_ = x//3
    y_ = y//3
    x_start,x_end = x_*3,x_*3+3
    y_start,y_end = y_*3,y_*3+3
    tt = df.iloc[x_start:x_end,y_start:y_end].values
    return tt.flatten()
    
# 横竖排除法，某个空格行取值范围和列取值范围，交集是1的时候就替换
def a1():
    num_set = set(range(1,10))
    flag = 0
    while flag == 0:
        flag = 1
        for i in range(0,9):
            for j in range(0,9):
                if df.iloc[i,j]==0:
                    x = num_set- set(df.iloc[i,:].values)
                    y = num_set- set(df.iloc[:,j].values)
                    # 当前区域数据，缺少哪些数据
                    block = num_set - set(every_block(df,i,j))
                    if len(x&y) == 1 :
                        replace_num = list(x&y)[-1]  
                        if not(replace_num in set(every_block(df,i,j))):
                            df.iloc[i,j] = replace_num
                            flag = 0
                    elif len(x&block) == 1 :
                        replace_num = list(x&block)[-1]
                        if not(replace_num in set(df.iloc[:,j].values)):
                            df.iloc[i,j] = replace_num
                            flag = 0
                    elif len(y&block) == 1 :
                        replace_num = list(block&y)[-1]
                        if not(replace_num in set(df.iloc[i,:].values)):
                            df.iloc[i,j] = replace_num
                            flag = 0




def a2():
    num_set = set(range(1,10))
    for i in range(0,9):
        for j in range(0,9):
            if df.iloc[i,j]==0:
                x = num_set- set(df.iloc[i,:].values)
                y = num_set- set(df.iloc[:,j].values)
                # 当前区域数据，缺少哪些数据
                block = num_set - set(every_block(df,i,j))
                if len(x&y) == 2 :
                    replace_num = list(x&y)[0]  
                    if not(replace_num in set(every_block(df,i,j))):
                        df.iloc[i,j] = replace_num
                elif len(x&block) == 2 :
                    replace_num = list(x&block)[0]
                    if not(replace_num in set(df.iloc[:,j].values)):
                        df.iloc[i,j] = replace_num
                elif len(y&block) == 2 :
                    replace_num = list(block&y)[0]
                    if not(replace_num in set(df.iloc[i,:].values)):
                        df.iloc[i,j] = replace_num







a1()
print('------------------------------------------')
print(df)
