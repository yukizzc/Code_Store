#!/usr/bin/env python
import uuid
import mysql.connector


def creat_table(code, typee):
    # 查询表是否存在
    sql = 'show tables'
    mycursor.execute(sql)
    table_list = []
    for i in mycursor:
        table_list.append(i[0])
    if not ((code + '_' + typee).lower() in table_list):
        temp = ' (date INT(10),code VARCHAR(10),open FLOAT(10,2),high FLOAT(10,2),' \
               'low FLOAT(10,2),close FLOAT(10,2),vol INT(20),amount FLOAT(20,2))'
        sql = 'create table ' + code + '_' + typee + temp
        mycursor.execute(sql)
    insert_first_data(0, code, 0, 0, 0, 0, 0, 0, typee)


def insert_first_data(k_time, code, k_open, k_high, k_low, k_close, k_vol, k_amount, typee):
    temp = ' (date,code,open,high,low,close,vol,amount) values(%s,%s,%s,%s,%s,%s,%s,%s)'
    sql = 'insert into ' + code + '_' + typee + temp
    val = (k_time, code, k_open, k_high, k_low, k_close, k_vol, k_amount)
    mycursor.execute(sql, val)
    mydb.commit()



if __name__ == "__main__":
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='', database='交割合约')
    mycursor = mydb.cursor()
    code_ = ['BTC', 'ETH', 'LINK', 'DOT']
    date_ = ['_CW', '_NW', '_CQ', '_NQ']
    type_ = ['1min', '5min', '1day']
    for i in code_:
        for j in date_:
            for k in type_:
                creat_table(i+j, k)
    mycursor.close()
    mydb.close()