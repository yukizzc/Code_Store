from sympy import *
import tkinter as tk



window = tk.Tk()
window.geometry('400x400')
t = tk.Text(window, height=2,width=30)
t2 = tk.Text(window, height=2,width=30)
def get_result():
    #return diff()
    model = t.get('0.0','end')
    y = model[0:-3]
    x = model[-2:-1]
    t2.delete(1.0, tk.END)
    t2.insert('end',diff(y,x))


b = tk.Button(window,text='求导',command=get_result)

t.place(x=10,y=10)
b.place(x=50,y=60)
t2.place(x=10,y=100)

note = tk.Label(window,text='请写成  5*x**2+4*x+5:x  这种形式',bg='red')
note2 = tk.Label(window,text='其中分号后面表示求导对象，*表示乘法，**表示乘方',bg='red')
note.place(x=10,y=150)
note2.place(x=10,y=180)
# 循环窗体
window.mainloop()
