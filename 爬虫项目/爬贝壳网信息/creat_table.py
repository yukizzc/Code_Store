import mysql.connector
import gloal_name
area_name = gloal_name.area_name    
coon = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database='liu'
)

cursor = coon.cursor()
code = area_name
temp = ' (url VARCHAR(150),location VARCHAR(150),name VARCHAR(150),date VARCHAR(150),per_price FLOAT(20,2),total_price FLOAT(10,1),area VARCHAR(150))'
sql = 'create table ' + code + temp
cursor.execute(sql)
cursor.close()
coon.close()