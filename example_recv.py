#!/usr/bin/env python3
# - *- coding: utf-8 -*-

import time
import receiver
from multiprocessing import Queue

from gi.repository import GObject, GLib

import cv2
import numpy as np
from xmlrpc.server import SimpleXMLRPCServer
import Server

IP_ROBOT = '10.42.0.135'
RTP_PORT = 5000
frame = None

#сетевые параметры
IP_SERVER = '10.42.0.1' #IP адрес сервера
DEBUG_PORT = 8000 #порт отправки отладочных кадров XML-RPC

q = Queue()

#server = Server.Client(queue = q)
#server.start()

recv = receiver.StreamReceiver(receiver.FORMAT_MJPEG, (IP_ROBOT, RTP_PORT))
recv.play_pipeline()

#нужно для корректной работы системы
mainloop = GLib.MainLoop()

#главный цикл программы    
try:
    mainloop.run()
#    while True:
#        if not q.empty():
#            cv2.imshow("hall", q.get())
#            cv2.waitKey(1)
        
except (KeyboardInterrupt, SystemExit):
    print('Ctrl+C pressed')

#cv2.destroyAllWindows()

#server.server_stop()

recv.stop_pipeline()
recv.null_pipeline()
