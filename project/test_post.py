if __name__ == '__main__':
    import socket,json


host1 = '61.135.155.81'
host2 = '222.73.7.161'
host3 = '210.14.65.73'
host4 = '121.40.223.213'
#port1 = [5160,5105,5106,5107]
#port2 = [5160,5106,5107]
#port3 = [5160,5106,5107]
#port4 = [5170,5106,5107,5108]

port1 = [135,139,445]
port2 = port1
port3 = port1
port4 = port1
import tkinter as tk
import threading
import tkinter.messagebox as ms
def date_post_test(host,port):
    for i in port:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host,i))
            t.insert('insert', 'IP:'+host + ' port: ' + str(i) + '   正常'+'\n')
        except:
            t.insert('insert', 'IP:'+host + ' port: ' + str(i) + '   不通'+'\n')

t1 = threading.Thread(target=date_post_test,args=(host1,port1))
t2 = threading.Thread(target=date_post_test,args=(host2,port2))
t3 = threading.Thread(target=date_post_test,args=(host3,port3))
t4 = threading.Thread(target=date_post_test,args=(host4,port4))


def date_post():
    t1.start()
    t2.start()
    t3.start()
    t4.start()


def land_post():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('60.29.239.115', 5118))
        ms.showwarning('桔梗', '网通1服务器登陆正常')
    except:
        ms.showwarning('桔梗','网通1服务器登陆端口不通')
    try:
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2.connect(('222.73.126.58', 5118))
        ms.showwarning('桔梗花', '电信1服务器登陆正常')
    except:
        ms.showwarning('桔梗花', '电信1服务器登陆端口不通')

window = tk.Tk()
window.title('金字塔IP、端口测试')
window.geometry('500x400')
b1 = tk.Button(window, text='行情', width=10, height=2, command=date_post).place(x=10,y=10)
b2 = tk.Button(window, text='登陆', width=10, height=2, command=land_post).place(x=10,y=260)
t = tk.Text(window,height=14,width=40)
t.place(x=130,y=10)

window.mainloop()
