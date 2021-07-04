import datetime, time
a = time.time()
b = time.mktime(datetime.datetime(2020,12,15,14,36,56).timetuple())
print(a,int(a))
