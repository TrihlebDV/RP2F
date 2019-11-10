#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import cv2
import numpy as np
#import threading
#import gi
#from gi.repository import GObject, GLib
#import xmlrpc.client
#from xmlrpc.server import SimpleXMLRPCServer
#import psutil
#import os
#import math
#import io
#import argparse
#import datetime

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


print('Start program')

assert rpicam.checkCamera(), 'Raspberry Pi camera not found'
print('Raspberry Pi camera found')

# Получаем свой IP адрес
ip = rpicam.getIP()
assert ip != '', 'Invalid IP address'
print('Robot IP address: %s' % ip)

print('OpenCV version: %s' % cv2.__version__)


#нужно для корректной работы системы
#mainloop = GLib.MainLoop()

#видеопоток с камеры робота    
#robotCamStreamer = rpicam.RPiCamStreamer(FORMAT, RESOLUTION, FRAMERATE, (IP, RTP_PORT), onFrameCallback)
#robotCamStreamer = rpicam.RPiCamStreamer(FORMAT, RESOLUTION, FRAMERATE, (IP, RTP_PORT))
#robotCamStreamer.setFlip(False, True)
#robotCamStreamer.setRotation(180)
#robotCamStreamer.start()

#XML-RPC клиент для запуска отладочных процедур
#debugClient = xmlrpc.client.ServerProxy('http://%s:%d' % (IP, DEBUG_PORT))

#контроль линии    
#lineFollow = LineFollow(robotCamStreamer, int(WIDTH), int(HEIGHT))#, debugClient)
#lineFollow.debug = False
#lineFollow.start()


try:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    h, w = frame.shape[:2]
    client = Client.Client()
    print(cap.get(cv2.CAP_PROP_FPS))
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    M = cv2.getRotationMatrix2D((h/2, w/2 ), 180, 1.0)
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.warpAffine(frame, M, (h, w))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #faces = face_cascade.detectMultiScale(
        #    gray,
        #    scaleFactor=1.3,
        #    minNeighbors=3,
        #    )
        #for (x, y, w, h) in faces:
        #    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        client.drawCvFrame(frame)
        print(count)
        count += 1
        
        
except (KeyboardInterrupt, SystemExit):
    print('Ctrl+C pressed')

#останов контроля линии
#lineFollow.stop()

#останов трансляции камеры
#robotCamStreamer.stop()    
#robotCamStreamer.close()
   
print('End program')


