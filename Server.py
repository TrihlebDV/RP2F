#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import socket
import time
import threading

import cv2
import numpy as np

class Client(threading.Thread):
    def __init__(self, ip = '10.54.54.1', port = 8000, queue = None):
        threading.Thread.__init__(self)
        self.daemon = True
        self._stopped = threading.Event()
        self._ip = ip
        self._port = port
        self.main = False
        self.buffer_size = 65536
        self.data = b''
        self.window = 'video streaming'
        self._queue = queue
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self._ip, self._port))

    def run(self):
        print('debug server started')
        print('OpenCV version: %s' % cv2.__version__)
        print('Lisening on %s::%d' %(self._ip, self._port))
        #self.sock.listen(10)
        #print('Socket now listening')
        #conn, addr = self.sock.accept()
        cv2.namedWindow(self.window, cv2.WINDOW_NORMAL)
        #cv2.resizeWindow(self.window, 600, 600)
        while not self._stopped.is_set():
            self.data += self.sock.recv(self.buffer_size)
            print("AAA")
            a = self.data.find(b'\xff\xd8')
            b = self.data.find(b'\xff\xd9')
            jpg = self.data[a : b + 2]
            self.data = self.data[b + 2 :]
            if a != -1 and b != -1:
                # decode frame and video time
                frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                if self.main:
                    cv2.imshow("HAL", frame)
                elif not self._queue is None:
                    self._queue.put(frame)
        self.sock.close()
        if self.main:
            cv2.destroyAllWindows()
        print('Server closed')
                
    def server_stop(self):
        self._stopped.set()

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('10.54.54.1', 8000))
    data = b''
    while True:
        #print("AAA")
        data += sock.recv(65536)
        a = data.find(b'\xff\xd8')
        b = data.find(b'\xff\xd9')
        jpg = data[a : b + 2]
        data = data[b + 2 :]
        if a != -1 and b != -1:
            # decode frame and video time
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow("HAL", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    cv2.destroyAllWindows()
        
            
