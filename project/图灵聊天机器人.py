# -*- coding: utf-8 -*-
import requests
message = '你好'
code = [100000,200000,302000,308000]
url = 'http://www.tuling123.com/openapi/api'
values = {
        "key": "b2e4a6f674774a22ba2258d0b068e808",
        "info": message,
        "userid": "123456"
    }

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(527, 430)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(50, 60, 301, 61))
        self.lineEdit.setObjectName("lineEdit")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(50, 240, 301, 161))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(370, 60, 93, 61))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(self.send)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def send(self):
        message = self.lineEdit.text()
        values['info'] = message
        resp = requests.post(url, values)
        resp = resp.json()
        self.receive(resp)
    def receive(self,resp):
        # 聊天
        if resp['code'] == code[0]:
            self.textEdit.append(resp['text'])
        # 链接类
        if resp['code'] == code[1]:
            self.textEdit.append(resp['url'])
        # 新闻类
        if resp['code'] == code[2]:
            for i in resp['list']:
                self.textEdit.append(i['article'])
                self.textEdit.append(i['detailurl']+'\n')
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "PushButton"))

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
ui = Ui_Form()
ui.setupUi(window)
window.show()
sys.exit(app.exec_())



