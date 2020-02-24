#!/usr/bin/python3
# -*- coding: utf-8 -*-

#GUI libraries
from PyQt5 import QtWidgets, QtGui, QtCore

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
import mouseEvent

from PostHandl import Spawer

#for testing
import math


class Implement(QtWidgets.QWidget, mouseEvent.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.draw = False
        self.mode = {"mode":404, "assert":False}
        self.default = cv2.imread("img.jpg")
        self.frame = None
        self.send_request = False #tell us about write or rwad mode
        self.texts = ["geting ready for writing mode", "geting ready for reading mode",  "put finger on the sensor",
                      "remove finger from sensor", "put the same finger again",
                      "stored!", "read out", "look at the camera", "match", "Unexpected ERROR"] 
        self.Ready_for_update = threading.Event()
        self.Ready_for_update.set()
        self.set(self.default)
        self.pos = []
        self.start = None
        self.finished = True #predict twise requesting
        self.thread = QThread()
        self.thread.start()
        self.server = SimpleXMLRPCServer(("10.42.0.1", 60002))
        self.server.logRequests = False
        self.server.register_function(self.comReceiver)
        self.serverControlThread = threading.Thread(target = self.server.serve_forever)
        self.serverControlThread.daemon = True
        self.serverControlThread.start()
        self.robot = xmlrpc.client.ServerProxy('http://%s:%d' % ("10.42.0.69", 60001))
        self.spawer = Spawer(self.on_recive)#, self.write_msg)
        self.spawer.start()

    def on_recive(self, frame):
        self.frame = frame
        self.set(self.frame)

    def comReceiver(self, msg):
        t = threading.Thread(target=self.comHandler, args=(msg,))
        t.start()
        return 0

    def comHandler(self, msg):
        self.mode = {"mode":404, "assert":0}
        if   msg == "error":         self.mode["mode"] = 8 #msg = self.texts[8]
        elif msg == "put finger":    self.mode["mode"] = 2 #msg = self.texts[2]
        elif msg == "remove finger": self.mode["mode"] = 3 #msg = self.texts[3]
        elif msg == "same finger":   self.mode["mode"] = 4 #msg = self.texts[4]
        elif msg == "stored":        self.mode["mode"] = 5 #msg = self.texts[5]
        elif msg == "read":          self.mode["mode"] = 6 #msg = self.texts[5]
        elif msg == "camera":        self.mode["mode"] = 7 #msg = self.texts[6]
        elif msg == "match":         self.mode["mode"] = 8 #msg = self.texts[7]
        elif msg == "unstored":      self.mode = {"mode":5, "assert":1} #msg = "Un" + self.texts[5]
        elif msg == "unread":        self.mode = {"mode":6, "assert":1} #msg = "Un" + self.texts[5]
        elif msg == "No match":       self.mode = {"mode":8, "assert":1} #msg = "No " + self.texts[7]
        elif msg == "square face":   self.mode["mode"] = 9
        elif msg == "return":
            time.sleep(2)
            self.mode = {"mode":404, "assert":False}
        self.set(self.frame)

    def set(self, img, check=False, msg=""):
        if self.Ready_for_update.is_set():
            self.update(img, check, msg)

    def update(self, img, check=False, msg=""):
        self.Ready_for_update.clear()
        if self.mode["assert"]: msg = "not "
        if img is None: img = self.default
        img = img.copy()
        if self.draw:
            x0, y0 = self.pos[0]
            x1, y1 = self.pos[1]
            angle = math.atan2(x1-x0, y1-y0)
            angle = angle * 180 / 3.14
            if angle > -97 and angle < -83:
                color = (0,255,0)
                if check:
                    self.start = True
            elif angle >  83 and angle <  97:
                color = (0,255,0)
                if check: self.start = False
            else: color = (0,0,255)
            cv2.line(img, self.pos[0], self.pos[1], color, 2)
            cv2.putText(img, str(int(angle)),
                        (300,300),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        color,
                        2)
        elif self.mode["mode"] < 2:
            msg += self.texts[ self.mode["mode"] ]
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray_image = cv2.equalizeHist(gray_image)
            cv2.putText(gray_image, msg,
                        (180,300),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255),
                        2)
            img = cv2.cvtColor(gray_image,cv2.COLOR_GRAY2RGB)
            #if self.mode["mode"]: t = threading.Thread(target=self.fake_robot, args=(True,))
            #else: t = threading.Thread(target=self.fake_robot, args=(False, ))
            if not self.send_request:
                if self.mode["mode"] == 0: _ = self.robot.write_mode()
                elif self.mode["mode"] == 1: _ = self.robot.read_mode()
                self.send_request = True
                #self.finished = False
            
            
        elif self.mode["mode"] < 9:
            msg += self.texts[ self.mode["mode"] ]
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray_image = cv2.equalizeHist(gray_image)
            cv2.putText(gray_image, msg,
                        (180,300),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255),
                        2)
            img = cv2.cvtColor(gray_image,cv2.COLOR_GRAY2RGB)
        elif self.mode["mode"] == 9:
            self.send_request = False
            
        '''if self.flag[1] or self.flag[2]:
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray_image = cv2.equalizeHist(gray_image)
            if self.flag[1]: text = "get ready for writeng mode"
            else:            text = "put finger on the sensor" 
            cv2.putText(gray_image, text,
                        (180,300),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255),
                        2)
            img = cv2.cvtColor(gray_image,cv2.COLOR_GRAY2RGB)
            self.direct = None
            if self.flag[1]: ar = (2, 1, 5)
            else:            ar = (2, 2, 5) 
            t = threading.Thread(target=self.waiter, args=ar)
            t.start()'''
  
        height, width, colors = img.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage
        image = QImage(img.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)
        image = image.rgbSwapped()
        pixmap = QtGui.QPixmap(image)
        self.label.setPixmap(pixmap)
        self.Ready_for_update.set()

    def keyPressEvent(self, e):
        if e.key()   ==  Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            _ = self.robot.stop()
            event.accept()
        else:
            event.ignore()

    def mousePressEvent(self, ev):
        if not self.send_request:
            if ev.button() == Qt.LeftButton:
                print("Pressed")
                self.draw = True
                self.pos.append((ev.x(),ev.y()))
                self.pos.append((ev.x(),ev.y()))
                self.set(self.frame)

    def mouseReleaseEvent(self, ev):
        if not self.send_request:
            if ev.button() == Qt.LeftButton:
                print("Released")
                self.set(self.frame, check=True)
                self.draw = False
                if not self.start is None:
                    if self.start: self.mode["mode"] = 0
                    else: self.mode["mode"] = 1
            #    t = threading.Thread(target=self.waiter, args=(1, 0))
            #    t.start()
            #print("HERE")
                self.set(self.frame)
                self.pos=[]
            

    def mouseMoveEvent(self, ev):
        if not self.send_request:
            self.pos[1] = (ev.x(), ev.y())
            self.set(self.frame)


def main():
    app = QtWidgets.QApplication(sys.argv)
    imp = Implement()
    imp.show()
    app.exec_()

if __name__ == '__main__':
    main()
