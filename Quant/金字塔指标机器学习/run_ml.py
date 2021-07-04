import pandas as pd
import joblib
import numpy as np
model = joblib.load('a.pkl')
#数据读取
data = pd.read_excel('test_data.xlsx')
x_data = np.array(data.iloc[-1, 1:].values).reshape(1, -1)
print(x_data)
#测试读取后的Model
print(model.predict(x_data))
