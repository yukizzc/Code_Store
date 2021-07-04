import json
from multiprocessing import Process 
import time   
import pandas as pd
import gloal_name

area_name = gloal_name.area_name    
df = pd.read_excel('ft.xls',header=None)
temp = df.values
temp2 = temp.flatten()
with open(area_name+'2'+'.json','w',encoding='utf-8') as f:   
    json.dump(list(temp2),f,ensure_ascii=False,indent=4)
