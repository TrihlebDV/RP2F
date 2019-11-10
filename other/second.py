#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys  # sys нужен для передачи argv в QApplication
import os  # Отсюда нам понадобятся методы для отображения содержимого директорий

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QByteArray, QEvent
import numpy as np
from time import sleep
import threading
import whl  # Это наш конвертированный файл дизайна

import receiver
import cv2

import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer

IP = '10.42.0.1'
IP_ROBOT = '10.42.0.68'
RTP_PORT = 5000
CONTROL_PORT = 9000
LOCAL_PORT = 6000

class ExampleApp(QtWidgets.QWidget, whl.Ui_Form):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.img = QtGui.QPixmap("screen.jpg")
        self.img = self.img.scaled(720, 480)
        self.label_2.setPixmap(self.img)
        self.w, self.h  = QtGui.QPixmap.width(self.img), QtGui.QPixmap.height(self.img)
        self.pushButton.clicked.connect(self.setText)
        self.d_w = 0
        self.mainStr = ""
        self.pixmap = None
        self.e1 = threading.Event()
        self.stopped = False
        self.t1 = threading.Thread(target=self.delText, args=(5, self.e1))
        self.daemon = True
        self.t1.start()
        self.btncheck = True
        self.recv = receiver.StreamReceiver(receiver.VIDEO_H264, self.onFrameCallback)
        self.resiverInit()
        self.robot = xmlrpc.client.ServerProxy('http://%s:%d' % (IP_ROBOT, CONTROL_PORT))
        self.serverControl = SimpleXMLRPCServer((IP, LOCAL_PORT))
        self.serverControl.register_function(self.get_statuse)
        self.serverControlThread = threading.Thread(target = self.serverControl.serve_forever)
        self.serverControl.logRequests = False #оключаем логирование
        self.serverControlThread.daemon = True
        self.serverControlThread.start()
        self.check = True
        self.psw = None
        self.psw_check = False

    def get_statuse(self, string):
        self.label.setText(string)
        return 0
        

    def resiverInit(self):
        self.recv.setPort(RTP_PORT)
        self.recv.setHost(IP_ROBOT)
        self.recv.play_pipeline()

    def onFrameCallback(self, data, width, heigh):
        cvimg = np.ndarray((heigh, width, 3), buffer = data, dtype = np.uint8)
        cvimg = cv2.cvtColor(cvimg, cv2.COLOR_RGB2BGR)
        byteValue = 3*width
        self.mQImage = QtGui.QImage(cvimg, width, heigh, byteValue, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(self.mQImage.rgbSwapped())
        self.label_2.setPixmap(pixmap)

    def setText(self):
        self.btncheck = not self.btncheck
        self.mainStr = self.mainStr + "\nButton have pressed!"
        self.label.setText(self.mainStr)
        self.e1.set()
        self.label_2.setPixmap(self.img)

        

    def delText(self, time_for_sleep, event_for_wait):
        while not self.stopped:
            event_for_wait.wait()
            sleep(time_for_sleep)
            self.mainStr = "deleted :)"
            self.label.setText(self.mainStr)
        print("Stopped(")


    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.stopped = True
            print("stop pipeline")
            self.recv.stop_pipeline()
            self.recv.null_pipeline()
            if self.psw_check: self.psw()
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, e):
        if self.check:
            if e.type() == QEvent.KeyPress:
                if e.text() == 'w':
                    self.label.setText("ip 10")
                    #print("PRESSED")
                    _ = self.robot.writeIP(b'10')
                    self.check = not self.check
                    e.accept()
                elif e.text() == 'd':
                    self.label.setText("setmode")
                    #_ = self.robot.setMode(1)
                    #print("PRESSED")
                    self.check = not self.check
                    e.accept()
                elif e.text() == 'a':
                    self.label.setText("finger write")
                    _ = self.robot.finger(1)
                    #print("PRESSED")
                    self.check = not self.check
                    e.accept()
                elif e.text() == 's':
                    self.label.setText("finger read")
                    _ = self.robot.finger(0)
                    #print("PRESSED")
                    self.check = not self.check
                    e.accept()
        if e.key() == Qt.Key_Escape:
            self.close()
                


    def keyReleaseEvent(self, e):
        if e.type() == QEvent.KeyRelease:
            if e.text() in ['w', 'd', 'a' , 's'] and not e.isAutoRepeat():
                #_ = self.robot.setSpeed('stop')
                self.label.setText("released")
                #print("RELEASED")
                self.check = not self.check
                e.accept()
                
            elif e.text() == 'r':
                self.label.setText("r released")
                #_ = self.robot.setSpeed('1UP')
                #print("PRESSED")
                self.check = not self.check
                e.accept()
                
            elif e.text() == 't':
                self.label.setText("t released")
                #_ = self.robot.setSpeed('1DOWN')
                #print("PRESSED")
                self.check = not self.check
                e.accept()
                
            elif e.text() == 'f':
                self.label.setText("f released")
                #_ = self.robot.setSpeed('2UP')
                #print("PRESSED")
                self.check = not self.check
                e.accept()
                
            elif e.text() == 'g':
                self.label.setText("g released")
                #_ = self.robot.setSpeed('2DOWN')
                #print("PRESSED")
                self.check = not self.check
                e.accept()

    def write_pswd(self, psw):
        self.psw = psw
        self.psw_check = True
        
    


def start(psw, wait):
    wait.hide()
    #app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.label.setText(window.mainStr)
    window.label.setPixmap(window.img.copy(0, 0, window.w/2 , window.h/2))
    window.write_pswd(psw)
    window.show()  # Показываем окно
    #app.exec_()  # и запускаем приложение
    
                

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.label.setText(window.mainStr)
    #window.img_laebl.setPixmap(window.img.copy(0, 0, window.w/2 , window.h/2))
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
