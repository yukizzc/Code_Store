import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import joblib
#数据读取
data = pd.read_excel('train_data.xlsx')
data.dropna(axis=0,inplace=True)
data = data.reset_index(drop=True)
x_data = data.iloc[:, 1:-1]
y_data = data.iloc[:, -1]

#模型搭建
def liner():
    model = LinearRegression(normalize=False)
    model.fit(x_data, y_data)
    predict = model.predict(x_data)
    print(mean_squared_error(y_data, predict))
    plt.plot(range(len(y_data)),y_data,label='real')
    plt.plot(range(len(y_data)),predict,label='predict')
    plt.legend(loc='best')
    plt.show()
    # 保存model
    #joblib.dump(model,'b.pkl')

def rf():
    model = RandomForestRegressor(n_estimators=200)
    model.fit(x_data, y_data)
    predict = model.predict(x_data)
    print(mean_squared_error(y_data, predict))
    plt.plot(range(len(y_data)), y_data, label='real')
    plt.plot(range(len(y_data)), predict, label='predict')
    plt.legend(loc='best')
    plt.show()
    #保存model
    #joblib.dump(model,'a.pkl')

if __name__ == '__main__':
    rf()

