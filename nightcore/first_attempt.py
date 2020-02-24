#!/usr/bin/python3
# -*- coding: utf-8 -*-

#GUI libraries
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QEventLoop, QThread, QObject, pyqtSlot, pyqtSignal

import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer

#necessary libraries
import sys

import time
import threading

#lib for drawing
import numpy as np
import cv2
import queue

#GUI form
import first_des
from PostHandl import Spawer


imp = None

def set_msg(msg):
    imp.write_msg(msg)
    return 0

class Implement(QtWidgets.QWidget, first_des.Ui_FORM):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.img = None
        self.globl = ""
        self.debug = ""
        self.put_start_img()
        self.thread = QThread()
        self.thread.start()
        self.server = SimpleXMLRPCServer(("10.42.0.1", 60002))
        self.server.logRequests = False
        self.server.register_function(set_msg)
        self.serverControlThread = threading.Thread(target = self.server.serve_forever)
        self.serverControlThread.daemon = True
        self.serverControlThread.start()
        self.robot = xmlrpc.client.ServerProxy('http://%s:%d' % ("10.42.0.69", 60001))
        self.spawer = Spawer(self.on_recive, self.write_msg)
        self.spawer.start()
        self.text.setPlaceholderText("   write here   ")
        
        #self.Button.clicked.connect(self.addText)

    def on_recive(self, img):
        self.imgLabel.setPixmap(QtGui.QPixmap.fromImage(img))
        self.imgLabel.setAlignment(Qt.AlignHCenter    # qtCore    <-> QtCore
                                         | Qt.AlignVCenter)

    def write_msg(self, msg):
        self.globl += msg + "\n"
        self.debug += msg + "\n"
        #print(self.globl.count("\n"))
        if(self.globl.count("\n") > 30):
            ind = self.globl.find("\n")
            self.globl = self.globl[ind+1 : ]
        self.globalLabel.setText(self.globl)
            
    def addText(self):
        if not self.text.text() == "":
            text = self.text.text()
            self.globl += self.text.text() + "\n"
            self.text.setText("")
            if(self.globl.count("\n") > 30):
                ind = self.globl.find("\n")
                self.globl = self.globl[ind+1 : ]
            self.globalLabel.setText(self.globl)
            if text == "write mode":
                _ = self.robot.write_mode()
            if text == "read mode":
                _ = self.robot.read_mode()
            if text.isdigit():
                _ = self.robot.set_req(text)
            
        
    def put_start_img(self):
        self.img = QtGui.QPixmap("img.jpg")
        self.imgLabel.setPixmap(self.img)

    def keyPressEvent(self, e):
        if e.key()   ==  Qt.Key_Escape:
            self.close()
        elif e.key() ==  Qt.Key_Return:
            self.addText()
        elif e.key() ==  Qt.Key_Enter:
            self.addText()

    def waiter(self):
        time.sleep(10)
        self.server.server_close()
        QApplication.instance().quit()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            _ = self.robot.stop()
            self.spawer.stop_trigger.emit()
            t1 = threading.Thread(target=self.waiter)
            t1.start()
            print(self.debug)
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
