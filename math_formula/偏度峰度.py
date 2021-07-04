import pandas as pd
import numpy as np
#pandas里面计算方式和excel这些一致
x = np.array([3302,3367,3392,3439,3452,3452,3464,3464,3445,3464])
s = pd.Series(x)
print(s.skew())
print(s.kurt())

#https://www.cnblogs.com/jiaxin359/p/8977333.html
length = len(x)
#第一种偏度计算方式
a1 = x - x.sum()/(length)
a1 = (a1**3).sum()/(length)

b1 = x - x.sum()/(length)
b1 = (b1**2).sum()/(length-1)
b1 = (np.sqrt(b1))**3
c1 = a1/b1
print(c1)

#第二种偏度计算方式
a2 = x - x.sum()/(length)
a2 = (a2**3).sum()/(length)

b2 = x - x.sum()/(length)
b2 = (b2**2).sum()/(length)
b2 = (np.sqrt(b2))**3

temp = np.sqrt(length*(length-1))/(length-2)
c2 = temp*a2/b2
print(c2)


######################################################################################################################################
#峰度计算公式，软件常用的那种
aa1 = (length+1)*length*(length-1)/((length-2)*(length-3))
bb1_1 = ((x - x.sum()/(length))**4).sum()
bb1_2 = (((x - x.sum()/(length))**2).sum())**2
bb1 = bb1_1/bb1_2
cc1 = 3*(length-1)**2/((length-2)*(length-3))
out = aa1*bb1-cc1
print(out)

