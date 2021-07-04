#!/usr/bin/python3
 
import pymongo
import pandas as pd
import gloal_name
import datetime
area_name = gloal_name.area_name   
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["liu"]
mycol = mydb[area_name]
temp = []
for x in mycol.find():
  temp.append(x)
df = pd.DataFrame(temp)
to_str = datetime.datetime.today().strftime("%Y-%m-%d")
df.to_excel('D:\\'+area_name+to_str+'.xlsx')
print('over')