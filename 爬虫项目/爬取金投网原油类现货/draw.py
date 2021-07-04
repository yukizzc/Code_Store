import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker



df = pd.read_csv('a.csv')
figure,ax = plt.subplots(figsize=(10,5))
ax.plot(df.iloc[:,0],df.iloc[:,1])
plt.xticks(df.iloc[:,0],color='blue',rotation=45)
ax.xaxis.set_major_locator(ticker.MultipleLocator(60))
plt.show()