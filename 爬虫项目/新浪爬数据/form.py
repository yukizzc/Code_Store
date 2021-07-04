# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
import sys
import time
import requests
from PyQt5.QtWidgets import QMessageBox

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(829, 752)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 30, 181, 590))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.textEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.textEdit_2 = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.textEdit_2.setObjectName("textEdit_2")
        self.verticalLayout.addWidget(self.textEdit_2)
        self.textEdit_3 = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.textEdit_3.setObjectName("textEdit_3")
        self.verticalLayout.addWidget(self.textEdit_3)
        self.textEdit_4 = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.textEdit_4.setObjectName("textEdit_4")
        self.verticalLayout.addWidget(self.textEdit_4)
        self.textEdit_5 = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.textEdit_5.setObjectName("textEdit_5")
        self.verticalLayout.addWidget(self.textEdit_5)
        self.textEdit_6 = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.textEdit_6.setObjectName("textEdit_6")
        self.verticalLayout.addWidget(self.textEdit_6)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(250, 30, 181, 590))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.textEdit_7 = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.textEdit_7.setObjectName("textEdit_7")
        self.verticalLayout_2.addWidget(self.textEdit_7)
        self.textEdit_8 = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.textEdit_8.setObjectName("textEdit_8")
        self.verticalLayout_2.addWidget(self.textEdit_8)
        self.textEdit_9 = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.textEdit_9.setObjectName("textEdit_9")
        self.verticalLayout_2.addWidget(self.textEdit_9)
        self.textEdit_10 = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.textEdit_10.setObjectName("textEdit_10")
        self.verticalLayout_2.addWidget(self.textEdit_10)
        self.textEdit_11 = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.textEdit_11.setObjectName("textEdit_11")
        self.verticalLayout_2.addWidget(self.textEdit_11)
        self.textEdit_12 = QtWidgets.QTextEdit(self.verticalLayoutWidget_2)
        self.textEdit_12.setObjectName("textEdit_12")
        self.verticalLayout_2.addWidget(self.textEdit_12)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(490, 30, 181, 590))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.textEdit_13 = QtWidgets.QTextEdit(self.verticalLayoutWidget_3)
        self.textEdit_13.setObjectName("textEdit_13")
        self.verticalLayout_3.addWidget(self.textEdit_13)
        self.textEdit_14 = QtWidgets.QTextEdit(self.verticalLayoutWidget_3)
        self.textEdit_14.setObjectName("textEdit_14")
        self.verticalLayout_3.addWidget(self.textEdit_14)
        self.textEdit_15 = QtWidgets.QTextEdit(self.verticalLayoutWidget_3)
        self.textEdit_15.setObjectName("textEdit_15")
        self.verticalLayout_3.addWidget(self.textEdit_15)
        self.textEdit_16 = QtWidgets.QTextEdit(self.verticalLayoutWidget_3)
        self.textEdit_16.setObjectName("textEdit_16")
        self.verticalLayout_3.addWidget(self.textEdit_16)
        self.textEdit_17 = QtWidgets.QTextEdit(self.verticalLayoutWidget_3)
        self.textEdit_17.setObjectName("textEdit_17")
        self.verticalLayout_3.addWidget(self.textEdit_17)
        self.textEdit_18 = QtWidgets.QTextEdit(self.verticalLayoutWidget_3)
        self.textEdit_18.setObjectName("textEdit_18")
        self.verticalLayout_3.addWidget(self.textEdit_18)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(150, 650, 401, 101))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.retranslateUi(Form)
        #self.pushButton.clicked.connect(self.pushButton.click)
        #self.pushButton_2.clicked.connect(self.pushButton_2.click)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "监控"))
        self.label.setText(_translate("Form", "品种"))
        self.label_2.setText(_translate("Form", "成本"))
        self.label_3.setText(_translate("Form", "现价"))
        self.pushButton.setText(_translate("Form", "start"))
        self.pushButton_2.setText(_translate("Form", "stop"))


class MyForm(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyForm, self).__init__()
        self.setupUi(self)
        # 从文本读取配置信息
        with open('code.txt', encoding='utf-8') as f:
            code = f.read().splitlines()
        self.textEdit.setText(code[0].split(',')[0])
        self.textEdit_2.setText(code[1].split(',')[0])
        self.textEdit_3.setText(code[2].split(',')[0])
        self.textEdit_4.setText(code[3].split(',')[0])
        self.textEdit_5.setText(code[4].split(',')[0])
        self.textEdit_6.setText(code[5].split(',')[0])

        self.textEdit_7.setText(code[0].split(',')[1])
        self.textEdit_8.setText(code[1].split(',')[1])
        self.textEdit_9.setText(code[2].split(',')[1])
        self.textEdit_10.setText(code[3].split(',')[1])
        self.textEdit_11.setText(code[4].split(',')[1])
        self.textEdit_12.setText(code[5].split(',')[1])

        self.pushButton.clicked.connect(self.click)
        self.pushButton_2.clicked.connect(self.click2)

    # 启动计时器
    def click(self):
        if self.textEdit.toPlainText() != "None":
            self.timer1 = QTimer(self)
            self.timer1.timeout.connect(self.operate1)
            self.timer1.start(timer_ti)
            self.textEdit.setEnabled(False)

        if self.textEdit_2.toPlainText() != "None":
            self.timer2 = QTimer(self)
            self.timer2.timeout.connect(self.operate2)
            self.timer2.start(timer_ti)
            self.textEdit_2.setEnabled(False)
        if self.textEdit_3.toPlainText() != "None":
            self.timer3 = QTimer(self)
            self.timer3.timeout.connect(self.operate3)
            self.timer3.start(timer_ti)
            self.textEdit_3.setEnabled(False)
        if self.textEdit_4.toPlainText() != "None":
            self.timer4 = QTimer(self)
            self.timer4.timeout.connect(self.operate4)
            self.timer4.start(timer_ti)
            self.textEdit_4.setEnabled(False)
        if self.textEdit_5.toPlainText() != "None":
            self.timer5 = QTimer(self)
            self.timer5.timeout.connect(self.operate5)
            self.timer5.start(timer_ti)
            self.textEdit_5.setEnabled(False)
        if self.textEdit_6.toPlainText() != "None":
            self.timer6 = QTimer(self)
            self.timer6.timeout.connect(self.operate6)
            self.timer6.start(timer_ti)
            self.textEdit_6.setEnabled(False)
    # 停止计时器
    def click2(self):
        if self.textEdit.toPlainText() != "None":
            self.timer1.stop()

        if self.textEdit_2.toPlainText() != "None":
            self.timer2.stop()

        if self.textEdit_3.toPlainText() != "None":
            self.timer3.stop()

        if self.textEdit_4.toPlainText() != "None":
            self.timer4.stop()

        if self.textEdit_5.toPlainText() != "None":
            self.timer5.stop()

        if self.textEdit_6.toPlainText() != "None":
            self.timer6.stop()

    def operate1(self):
        a = Future(url_1)
        a.cal()
        a_close = a.close
        self.textEdit_13.setText(str(a_close))
        if float(a_close)>float(self.textEdit_7.toPlainText())+100 or float(a_close)<float(self.textEdit_7.toPlainText())-100:
            QMessageBox(QMessageBox.Warning, '警告', self.textEdit.toPlainText()+'出现异常')

    def operate2(self):
        a = Stock(url_2)
        a.cal()
        a_close = a.close
        self.textEdit_14.setText(a_close)
        if float(a_close)>float(self.textEdit_8.toPlainText())+0.5 or float(a_close)<float(self.textEdit_8.toPlainText())-0.5:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', self.textEdit_2.toPlainText()+'出现异常')
            msg_box.exec_()
    def operate3(self):
        a = Future(url_3)
        a.cal()
        a_close = a.close
        self.textEdit_15.setText(a_close)
        if float(a_close)>float(self.textEdit_9.toPlainText())+10 or float(a_close)<float(self.textEdit_9.toPlainText())-10:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', self.textEdit_3.toPlainText()+'出现异常')
            msg_box.exec_()

    def operate4(self):
        a = Stock(url_4)
        a.cal()
        a_close = a.close
        self.textEdit_16.setText(a_close)
        if float(a_close)>float(self.textEdit_10.toPlainText())+5 or float(a_close)<float(self.textEdit_10.toPlainText())-5:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', self.textEdit_4.toPlainText()+'出现异常')
            msg_box.exec_()
    def operate5(self):
        a = Future(url_5)
        a.cal()
        a_close = a.close
        self.textEdit_17.setText(a_close)
        if float(a_close)>float(self.textEdit_11.toPlainText())+100 or float(a_close)<float(self.textEdit_11.toPlainText())-100:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', self.textEdit_5.toPlainText()+'出现异常')
            msg_box.exec_()
    def operate6(self):
        a = A50(url_6)
        a.cal()
        a_close = a.close
        self.textEdit_18.setText(a_close)
        if float(a_close)>float(self.textEdit_12.toPlainText())+100 or float(a_close)<float(self.textEdit_12.toPlainText())-100:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', self.textEdit_6.toPlainText()+'出现异常')
            msg_box.exec_()
# 期货的爬取数据
class Future:
    def __init__(self, url):
        self.url = url

    def cal(self):
        self.r = requests.get(self.url)
        self.demo = self.r.text
        self.close = self.demo.split(',')[8]


class Stock:
    def __init__(self, url):
        self.url = url

    def cal(self):
        self.r = requests.get(self.url)
        self.demo = self.r.text
        self.close = self.demo.split(',')[3]

class A50:
    def __init__(self, url):
        self.url = url
    def cal(self):
        self.r = requests.get(self.url)
        self.demo = self.r.text
        self.close = self.demo.split(',')[0][-9:]


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyForm()
    window.show()
    timer_ti = 1000*5
    # 期货
    url_1 = "https://hq.sinajs.cn/?list=nf_JD0"
    # 股票
    url_2 = "https://hq.sinajs.cn/?list=sh510050"
    # 期货
    url_3 = "https://hq.sinajs.cn/?list=nf_C0"
    # 股票
    url_4 = "https://hq.sinajs.cn/?list=sh600051"
    # 期货
    url_5 = ""
    # a50
    url_6 = "https://hq.sinajs.cn/?list=hf_CHA50CFD"

sys.exit(app.exec_())