from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import matplotlib.pyplot as plt

#qt desiger生成的ui代码
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(612, 430)
        Form.setMinimumSize(QtCore.QSize(612, 430))
        Form.setMaximumSize(QtCore.QSize(612, 430))
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(60, 20, 241, 41))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(101, 220, 241, 41))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(60, 270, 321, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(420, 170, 93, 71))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(60, 120, 321, 87))
        self.textEdit.setObjectName("textEdit")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(60, 55, 400, 41))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "+1:call:26500:200"))
        self.label_2.setText(_translate("Form", "50现价及上下限范围"))
        self.lineEdit_2.setText(_translate("Form", "3.0,-1,1"))
        self.pushButton.setText(_translate("Form", "盈亏图"))
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">+1:call:26500:200</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">-1:put:26000:2000</p></body></html>"))
        self.label_3.setText(_translate("Form", "+表示买方-表示卖方,1表示数量，冒号后为行权价格,权利金"))
#定义四种合约的规则
class BuyCall:
    def __init__(self, price, price_xq, x_input,num):
        self.price = price
        self.price_xq = price_xq
        self.x_input = x_input
        self.num = num

    def get_result(self):
        result = []
        for i in self.x_input:
            if i > self.price_xq:
                result.append((i - self.price_xq)  - self.price )
            else:
                result.append(0 - self.price )
        return np.array(result)*self.num
class SellCall:
        def __init__(self, price, price_xq, x_input,num):
            self.price = price
            self.price_xq = price_xq
            self.x_input = x_input
            self.num = num

        def get_result(self):
            result = []
            for i in self.x_input:
                if i > self.price_xq:
                    result.append(-(i - self.price_xq)  + self.price )
                else:
                    result.append(self.price )
            return np.array(result)*self.num
class BuyPut:
    def __init__(self, price, price_xq, x_input,num):
        self.price = price
        self.price_xq = price_xq
        self.x_input = x_input
        self.num = num

    def get_result(self):
        result = []
        for i in self.x_input:
            if i < self.price_xq:
                result.append((self.price_xq - i)  - self.price )
            else:
                result.append(0 - self.price )
        return np.array(result)*self.num
class SellPut:
    def __init__(self, price, price_xq, x_input,num):
        self.price = price
        self.price_xq = price_xq
        self.x_input = x_input
        self.num = num

    def get_result(self):
        result = []
        for i in self.x_input:
            if i < self.price_xq:
                result.append(-(self.price_xq - i)  + self.price )
            else:
                result.append(self.price )
        return np.array(result)*self.num
class Cursor(object):
    def __init__(self, ax):
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line

        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        plt.draw()
class SnaptoCursor(object):
    """
    Like Cursor but the crosshair snaps to the nearest x,y point
    For simplicity, I'm assuming x is sorted
    """
    def __init__(self, ax, x, y):
        self.ax = ax
        self.lx = ax.axhline(color='r')  # the horiz line
        self.ly = ax.axvline(color='r')  # the vert line
        self.x = x
        self.y = y
        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):

        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata

        indx = min(np.searchsorted(self.x, [x])[0], len(self.x) - 1)
        x = self.x[indx]
        y = self.y[indx]
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        #print('x=%1.2f, y=%1.2f' % (x, y))
        plt.draw()
import sys
class MyForm(QtWidgets.QWidget,Ui_Form):
    def __init__(self):
        super(MyForm,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.pbn)
    def pbn(self):
        #记录50价格范围
        temp2 = self.lineEdit_2.text()
        li2 = temp2.split(sep=',')
        x_close = np.arange(float(li2[0]) + float(li2[1]), float(li2[0]) + float(li2[2]), 0.001)*10000

        code = []
        temp = self.textEdit.toPlainText()
        li = temp.split('\n')
        for i in range(len(li)):
            if li[i] == '':
                continue
            #每一行根据冒号切分
            li2 = li[i].split(':')
            if li2[1] == 'call':
                if li[i][0] == '+':
                    t1 = BuyCall(int(li2[3]), int(li2[2]), x_close,int(li2[0][1:]))
                    code.append(t1)
                elif li[i][0] == '-':
                    t1 = SellCall(int(li2[3]), int(li2[2]), x_close,int(li2[0][1:]))
                    code.append(t1)
            elif li2[1] == 'put':
                if li[i][0] == '+':
                    t1 = BuyPut(int(li2[3]), int(li2[2]), x_close,int(li2[0][1:]))
                    code.append(t1)
                elif li[i][0] == '-':
                    t1 = SellPut(int(li2[3]), int(li2[2]), x_close,int(li2[0][1:]))
                    code.append(t1)
            else:
                print('格式有误')

        total = np.zeros((len(x_close)))
        for i in range(len(code)):
            total = np.array(code[i].get_result())+total




        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)



        plt.xlabel('price_50')
        plt.ylabel('Profit')
        plt.xlim((x_close.min()*0.98,x_close.max()*1.02))
        plt.ylim((total.min()*0.98,total.max()*1.02))
        #cursor = Cursor(ax)
        cursor = SnaptoCursor(ax, x_close, total)
        plt.connect('motion_notify_event', cursor.mouse_move)
        ax.plot(x_close, total)
        plt.show()






if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyForm()
    window.show()
    sys.exit(app.exec_())
