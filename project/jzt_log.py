import pandas as pd
#debugfile('D:\file.txt','当前a值为%.2f',a)
#原公式文件
path = r'C:\Users\zzc\Desktop\py项目\model.txt'
#debugfile输出的路径文件
outfile = r'D:\file.txt'
li = []
with open(path) as file:
    txt = file.readlines()
    for i in txt:
        index = i.find(':')
        if index>0 and i[0:2]!='//' and i[index+1]!='\\':
            li.append(i[0:index])

li2 = list(set(li))
#程序化运行时候的记录
def run(l=li2):
    for i in l:
        print('debugfile(\''+outfile+'\',\''+i+'的值为%.2f\''+','+i+');')
#回测中使用，添加了日期和时间
def test(l=li2):
    for i in l:
        print('debugfile(\''+outfile+'\',NUMTOSTR(date,0)&\'   \'&NUMTOSTR(time,0)&\'   \'&\''+i+'的值为%.2f\''+','+i+');')
test()
