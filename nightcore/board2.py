#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import cv2
import numpy as np
import threading

import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer

import os

import base64
import zmq

from serial_test import ArdHandler
import FR

RTP_PORT = 5000 #порт отправки RTP видео

CONTROL_PORT = 60001

worker = None

# проверка доступности камеры, возвращает True, если камера доступна в системе
def checkCamera():
    res = os.popen('vcgencmd get_camera').readline().replace('\n','') #читаем результат, удаляем \n
    dct = {}
    for param in res.split(' '): #разбираем параметры
        tmp = param.split('=')
        dct.update({tmp[0]: tmp[1]}) #помещаем в словарь
    return (dct['supported'] and dct['detected'])

def getIP():
    #cmd = 'hostname -I | cut -d\' \' -f1'
    #ip = subprocess.check_output(cmd, shell = True) #получаем IP
    res = os.popen('hostname -I | cut -d\' \' -f1').readline().replace('\n','') #получаем IP, удаляем \n
    return res

class Worker():
    def __init__(self):
       self.msg = None
       self.pc  = xmlrpc.client.ServerProxy('http://%s:%d' % ("10.42.0.1", 60002))
       self.read_mode = False # false - Read Mode | True - write mode
       self.write_mode = False
       
       self.context = zmq.Context()
       self.footage_socket = self.context.socket(zmq.PUB)
       self.footage_socket.connect('tcp://10.42.0.1:60000')
       self.recv_sock = self.context.socket(zmq.SUB)
       self.recv_sock.bind('tcp://10.42.0.69:6000')
       self.recv_sock.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
       self.pc.set_msg("asasa")
       self.ardHandler = ArdHandler(func=self.func_for_pc)
       self.ardHandler.start()
       self.cap = cv2.VideoCapture(0)
       self.fr = FR.FR(self.func_for_pc)
       
       self.img = cv2.imread("img.jpg")

       self._stopped = False

    def func_for_pc(self, msg):
        _ = self.pc.set_msg(msg)

    def stop(self):
        self.pc.set_msg("RPi: Worker stopped!")
        self._stopped = True
        self.ardHandler.stop()
        return 0
            

def read_mode():
    worker.write_mode = False             
    worker.read_mode  = not worker.read_mode 
    return 0

def write_mode():
    worker.read_mode = False             
    worker.write_mode  = not worker.write_mode
    return 0

def stop():
    ans = worker.stop()
    return ans

def set_req(count):
    worker.ardHandler.req = count #notice!: count should be string
    worker.ardHandler._inReady.set()
    return 0
    
print('Start program')

assert checkCamera(), 'Raspberry Pi camera not found'
print('Raspberry Pi camera found')

# Получаем свой IP адрес
ip = getIP()
assert ip != '', 'Invalid IP address'
print('Robot IP address: %s' % ip)

print('OpenCV version: %s' % cv2.__version__)

print('initiating Serial communication with Arduino')

#initalize main object
worker = Worker()

# XML-RPC сервер управления в отдельном потоке
serverControl = SimpleXMLRPCServer((ip, CONTROL_PORT)) #запуск XMLRPC сервера
serverControl.logRequests = False #оключаем логирование
print('Control XML-RPC server listening on %s:%d' % (ip, CONTROL_PORT))

# register our functions
serverControl.register_function(read_mode)
serverControl.register_function(write_mode)
serverControl.register_function(stop)
serverControl.register_function(set_req)

#запускаем сервер в отдельном потоке
serverControlThread = threading.Thread(target = serverControl.serve_forever)
serverControlThread.daemon = True
serverControlThread.start()

def read(obj):
    # obj.ardHandler.read = True
    iden = obj.ardHandler.read()
    ans = obj.fr.read(iden-1, obj.cap)
    return ans
    
def write(obj):
    obj.ardHandler.write(len(obj.fr.known_face_encodings) + 1)
    obj.fr.write(obj.cap)

#главный цикл программы    
#
try:
    worker.pc.set_msg("RPi: Worker started!")
    while not worker._stopped:
        ret, frame = worker.cap.read()
        
        if worker.read_mode:
            ans = read(worker)
            if ans == -1:
                 worker.pc.set_msg("got a problem")
            else:
                if ans: worker.pc.set_msg("True")
                else:   worker.pc.set_msg("False")
            read_mode()
                
        elif worker.write_mode:
            write(worker)
            write_mode()
        else:
            #frame = cv2.resize(frame, (640, 480))
            encoded, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer)
            worker.footage_socket.send(jpg_as_text)
            #print("BBB")
            _ = worker.recv_sock.recv_string()
            #print("AAA")
        
except (KeyboardInterrupt, SystemExit):
    print('Ctrl+C pressed')


#останов сервера
serverControl.server_close()

   
print('Program over...')


