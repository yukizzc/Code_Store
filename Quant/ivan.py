import tushare as ts
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
data = ts.get_k_data('510050',start='2008-01-01',end='2018-01-01',ktype='D',index=False)
li =np.array(data['close'].values)
t1 = np.diff(li)
result = []
temp = 0
for i in range(len(t1)):
    if t1[i]>0:
        temp+=1
        continue
    if t1[i]<0:
        result.append(temp)
        temp = 0
result = np.array(result)
result = result[result>0]
plt.hist(result)
plt.show()