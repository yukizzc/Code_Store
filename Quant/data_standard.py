import numpy as np

def filter_extreme_MAD(series,n): #MAD:中位数去极值
  median = series.quantile(0.5)
  new_median = ((series - median).abs()).quantile(0.50)
  max_range = median + n*new_median
  min_range = median - n*new_median
  return np.clip(series,min_range,max_range)

def filter_extreme_3sigma(series,n=3): #3 sigma
  mean = series.mean()
  std = series.std()
  max_range = mean + n*std
  min_range = mean - n*std
  return np.clip(series,min_range,max_range)

def filter_extreme_percentile(series,min = 0.025,max = 0.975): #百分位法
  series = series.sort_values()
  q = series.quantile([min,max])
  return np.clip(series,q.iloc[0],q.iloc[1])
  
  
#标准化
def standardize_series(series):
  std = series.std()
  mean = series.mean()
  return (series-mean)/std
