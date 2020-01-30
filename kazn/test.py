#!/usr/bin/python3
# -*- coding: utf-8 -*-

#GUI libraries
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QEventLoop, QThread, QObject, pyqtSlot, pyqtSignal

#import xmlrpc.client
#from xmlrpc.server import SimpleXMLRPCServer

#necessary libraries
import sys

import time
import threading

#lib for drawing
#import numpy as np
import cv2
#import queue

#GUI form
#import first_des
import low_way
#from PostHandl import Spawer


imp = None

def set_msg(msg):
    imp.write_msg(msg)
    return 0

class Implement(QtWidgets.QWidget, low_way.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        #self.img = None
        self.infoFlag = False
        self.static = False
        self._onShow = None
        self.text = "you\nare\nso\nstuped (\n"
        self.put_start_img()
        self.setWindowFlags(Qt.FramelessWindowHint)
        #self.thread = QThread()
        #self.thread.start()
        #self.server = SimpleXMLRPCServer(("10.42.0.1", 60002))
        #self.server.logRequests = False
        #self.server.register_function(set_msg)
        #self.serverControlThread = threading.Thread(target = self.server.serve_forever)
        #self.serverControlThread.daemon = True
        #self.serverControlThread.start()
        #self.robot = xmlrpc.client.ServerProxy('http://%s:%d' % ("10.42.0.69", 60001))
        #self.spawer = Spawer(self.on_recive, self.write_msg)
        #self.spawer.start()
        #self.text.setPlaceholderText("   write here   ")
        
        #self.Button.clicked.connect(self.addText)

    def writeModeStart(self, ):
        pass

    def readModeStart(self, ):
        pass
        

    def on_recive(self, img):
        if not self.infoFlag:
            self.imgLabel.setPixmap(QtGui.QPixmap.fromImage(img))
            self.imgLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def write_msg(self, msg):
        self.text += msg + "\n"
        if(self.text.count("\n") > 30):
            ind = self.text.find("\n")
            self.text = self.text[ind+1 : ]
        if self.infoFlag:
            self.label.setText(self.text)
            
    def addText(self):
        if not self.text.text() == "":
            text = self.text.text()
            self.globl += self.text.text() + "\n"
            self.text.setText("")
            if(self.globl.count("\n") > 30):
                ind = self.globl.find("\n")
                self.globl = self.globl[ind+1 : ]
            self.globalLabel.setText(self.globl)
            
        
    def put_start_img(self):
        img = cv2.imread("start.jpg")
        if not img is None:
            res = cv2.resize(img, (720, 480), interpolation = cv2.INTER_AREA)
            self._onShow = QtGui.QImage(res, res.shape[1], res.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.label.setPixmap(QtGui.QPixmap(self._onShow))

    def keyPressEvent(self, e):
        if int(e.modifiers()) == (Qt.ControlModifier):
            if e.key() == Qt.Key_S:
                self.infoFlag = not self.infoFlag
                self.write_msg("INFO:: mode chanched")
            if e.key() == Qt.Key_W:
                if not self.static:
                    #_ = self.robot.write_mode()
                    self.write_msg("INFO::write mode\n      static [OK]")
                    #self.static = True #static mode
            if e.key() == Qt.Key_R:
                if not self.static:
                    #_ = self.robot.write_mode()
                    self.write_msg("INFO::read mode\n      static [OK]")
                    #self.static = True #static mode
    
        if e.key()   ==  Qt.Key_Escape:
            self.close()


    def waiter(self):
        time.sleep(3)
        #self.server.server_close()
        QApplication.instance().quit()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            #_ = self.robot.stop()
            #self.spawer.stop_trigger.emit()
            t1 = threading.Thread(target=self.waiter)
            t1.start()
            event.ignore()
        else:
            event.ignore()
                
                

def main():
    global imp
    app = QtWidgets.QApplication(sys.argv)
    imp = Implement()
    imp.show()
    app.exec_()

if __name__ == '__main__':
    main()
