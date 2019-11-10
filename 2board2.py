#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import cv2
import numpy as np
import threading
import gi
from gi.repository import GObject, GLib
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
import psutil
import os
import math
import io
import argparse
import datetime

#личная библиотека
import Client

#библиотеки СКТБ
import rpicam

#настройки видеопотока
#FORMAT = rpicam.FORMAT_H264
FORMAT = rpicam.FORMAT_MJPEG
WIDTH, HEIGHT = 640, 360
RESOLUTION = (WIDTH, HEIGHT)
FRAMERATE = 30

#сетевые параметры
#IP = '192.168.42.100'
#IP = '192.168.42.50' #пульт
IP = '10.42.0.1' #пульт
RTP_PORT = 5000 #порт отправки RTP видео
DEBUG_PORT = 8000 #порт отправки отладочных кадров XML-RPC
CONTROL_PORT = 9000 #порт XML-RPC управления роботом

#Чувтвительность алгоритма определения линии
SENSITIVITY = 70


BASE_SPEED = 30

cameraPos = False #False - смотрим прямо, True - смотрим вниз
coefs = (0.85, 0.0, 0.0)

class LineFollow(threading.Thread):
    #камера источник кадров, ширина фрейма в кадре, выстота фрейма в кадре, привязка по нижней границе
    def __init__(self, camera, width, height):#, debugClient):
        threading.Thread.__init__(self)
        self.daemon = True
        self._stopped = threading.Event() #событие для остановки потока
        self.camera = camera
        self._frame = None
        self.width = width
        self.client = Client.Client()
        if width > WIDTH:     # проверить нужно ли вообще
            self.width = WIDTH
        self.height = height
        if height > HEIGHT:
            self.height = HEIGHT
        self._newFrameEvent = threading.Event() #событие для контроля поступления кадров
        #отладочный сервер
        #self.debugClient = debugClient
        self.counter = 0
    
    def run(self):
        print('Line follow started')
        while not self._stopped.is_set():
            self.camera.frameRequest() #отправил запрос на новый кадр
            self._newFrameEvent.wait() #ждем появления нового кадра
            if not (self._frame is None): #если кадр есть
                gray = cv2.cvtColor(self._frame, cv2.COLOR_BGR2GRAY)
                _ , fthresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
                _, contours, _ = cv2.findContours(fthresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                print(self.counter)
                self.counter += 1
                #self.client.drawCvFrame(self._frame)
                #time.sleep(0.1)
            else:
                print("Problem with camera")
                            
            self._newFrameEvent.clear() #сбрасываем событие

        print('Line follow stopped')

    def stop(self): #остановка потока
        self._stopped.set()
        if not self._newFrameEvent.is_set(): #если кадр не обрабатывается
            self._frame = None
            self._newFrameEvent.set() 
        self.join()

    def setFrame(self, frame): #задание нового кадра для обработки
        if not self._newFrameEvent.is_set(): #если обработчик готов принять новый кадр
            self._frame = frame
            self._newFrameEvent.set() #задали событие
        return self._newFrameEvent.is_set()
        
def onFrameCallback(frame): #обработчик события 'получен кадр'
    lineFollow.setFrame(frame) #задали новый кадр


print('Start program')

assert rpicam.checkCamera(), 'Raspberry Pi camera not found'
print('Raspberry Pi camera found')

# Получаем свой IP адрес
ip = rpicam.getIP()
assert ip != '', 'Invalid IP address'
print('Robot IP address: %s' % ip)

print('OpenCV version: %s' % cv2.__version__)


#нужно для корректной работы системы
mainloop = GLib.MainLoop()

#видеопоток с камеры робота    
robotCamStreamer = rpicam.RPiCamStreamer(FORMAT, RESOLUTION, FRAMERATE, (IP, RTP_PORT), onFrameCallback)
#robotCamStreamer = rpicam.RPiCamStreamer(FORMAT, RESOLUTION, FRAMERATE, (IP, RTP_PORT))
#robotCamStreamer.setFlip(False, True)
#robotCamStreamer.setRotation(180)
robotCamStreamer.start()

#XML-RPC клиент для запуска отладочных процедур
#debugClient = xmlrpc.client.ServerProxy('http://%s:%d' % (IP, DEBUG_PORT))

##контроль линии    
#ineFollow = LineFollow(robotCamStreamer, int(WIDTH), int(HEIGHT))#, debugClient)
#lineFollow.debug = False
#lineFollow.start()


try:
    mainloop.run()
except (KeyboardInterrupt, SystemExit):
    print('Ctrl+C pressed')

#останов контроля линии
#lineFollow.stop()

#останов трансляции камеры
robotCamStreamer.stop()    
robotCamStreamer.close()
   
print('End program')


