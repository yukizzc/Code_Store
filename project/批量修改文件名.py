#coding:utf-8
import os
address = r'E:\机器学习\【李沐】动手学深度学习-pytorch 2021版\\'
movie_name = os.listdir(address)
for temp in movie_name:
    #find表示从左往右找第一个
    num = temp.find('(')
    num2 = temp.find(')')
    new_name = temp[:num] + temp[num2+1:]
    os.rename(address+temp,address+new_name)
