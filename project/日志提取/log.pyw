#将批量处理文件放到filepath路径下，通过for循环进行逻辑判断

import shutil
import os
#a是包括,b是不包括的字符
inline = open("setting.txt",encoding='gbk')
lines = inline.readlines()
a = lines[0].rstrip("\n")
b = lines[1]


filepath = r".\file\\"
pathDir =  os.listdir(filepath)
#print(pathDir)
n = open('out.txt','w',encoding='gbk')
for allDir in pathDir:
    child = os.path.join('%s%s' % (filepath, allDir))

    #o是读取的文件,n是过滤字段后的文件
    o = open(child,encoding='gbk')

    for line in o.readlines():

        if a in line and not(b in line):
            #print(line)
            n.write(line)
    o.close()

n.close()



