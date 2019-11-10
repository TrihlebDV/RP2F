# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\gulya\Desktop\DLB\registration_success.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def __init__(self, name):
        super().__init__()

        self.window = QtWidgets.QWidget()
        self.setupUi(self.window, name)
        self.window.show()
        
        #self.name = name

    def setupUi(self, Form, name):
        Form.setObjectName("Form")
        Form.resize(464, 237)
        self.name_label = QtWidgets.QLabel(Form)
        self.name_label.setGeometry(QtCore.QRect(190, 10, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.name_label.setFont(font)
        self.name_label.setObjectName("name_label")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(20, 50, 431, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setTextFormat(QtCore.Qt.AutoText)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.sections_label = QtWidgets.QLabel(Form)
        self.sections_label.setGeometry(QtCore.QRect(20, 100, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sections_label.setFont(font)
        self.sections_label.setObjectName("sections_label")
        self.ok_btn = QtWidgets.QPushButton(Form)
        self.ok_btn.setGeometry(QtCore.QRect(350, 190, 93, 28))
        self.ok_btn.setObjectName("ok_btn")

        self.retranslateUi(Form, name)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.ok_btn.clicked.connect(self.window.close)

    def retranslateUi(self, Form, name):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Регистрация"))
        self.name_label.setText(_translate("Form", name + ","))
        self.label_4.setText(_translate("Form", "<html><head/><body><p>Вы успешно зарегистрированы в системе и записаны на следующие секции:</p></body></html>"))
        self.sections_label.setText(_translate("Form", "DLB"))
        self.ok_btn.setText(_translate("Form", "OK"))
