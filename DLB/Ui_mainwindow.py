#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from PyQt5 import QtCore, QtGui, QtWidgets
import sys
#from database import DB
import Ui_registration, Ui_graphic
import matplotlibrary
from xmlrpc.server import SimpleXMLRPCServer
import threading


id_registered = []

class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()

        self.window = QtWidgets.QMainWindow()
        self.setupUi(self.window)
        self.window.show()
        self.serverControl = SimpleXMLRPCServer(('10.42.0.1', 3000)) #запуск XMLRPC сервера
        self.serverControl.logRequests = False #оключаем логирование
        self.serverControl.register_function(self.rewrite)
        self.buff = []
        self.counter = 0
        self.serverControlThread = threading.Thread(target = self.serverControl.serve_forever)
        self.serverControlThread.daemon = True
        self.serverControlThread.start()
        #datebase = DB()

    def rewrite(self, ip):
        if not ip in self.buff:
            self.buff.append(ip)
            self.counter += 1
            self.window_to_open.label_9.setText(str(self.counter))
        return 0


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(596, 150)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.register_btn = QtWidgets.QPushButton(self.centralwidget)
        self.register_btn.setGeometry(QtCore.QRect(30, 90, 93, 28))
        self.register_btn.setObjectName("register_btn")
        self.analyse_btn = QtWidgets.QPushButton(self.centralwidget)
        self.analyse_btn.setGeometry(QtCore.QRect(140, 90, 93, 28))
        self.analyse_btn.setObjectName("analyse_btn")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 551, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.register_btn.clicked.connect(self.open_registration)
        self.analyse_btn.clicked.connect(self.open_analyse)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Система автоматизации сбора информации"))
        self.register_btn.setText(_translate("MainWindow", "Регистрация"))
        self.analyse_btn.setText(_translate("MainWindow", "Аналитика"))
        self.label.setText(_translate("MainWindow", "Система автоматизации сбора информации"))

    def open_registration(self):
        self.window_to_open = Ui_registration.Ui_Form()
    
    def open_analyse(self):
        self.window_to_open = Ui_graphic.Ui_Form()
        self.window_to_open.label_9.setText(str(self.counter))
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_MainWindow()
    sys.exit(app.exec_())
    # инициализация сервера
    # повторяющиеся callback запросы к RPi?
