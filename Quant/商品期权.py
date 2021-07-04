zq = ['白糖','棉花','PTA','甲醇','菜粕']
dq = ['豆粕','玉米','铁矿','液化气']
sq = ['沪铜','沪金','橡胶']
zq_mu = [10,1,1,1,1]
dq_mu = [10,10,100,20]
sq_mu = [5,1000,10]

import pandas as pd
data = pd.DataFrame(columns=['标的','单位'])
data['单位'] = zq_mu+dq_mu+sq_mu
data['标的'] = zq+dq+sq
print(data)
