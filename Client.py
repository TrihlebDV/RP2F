#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import socket
import time

import cv2
import numpy as np

class Client():
    def __init__(self, ip = '10.42.0.1', port = 8000):
        self._ip = ip
        self._port = port
        self.max_size = 65536 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('///debug client inited')

    def client_stop(self):
        self.sock.close()
        print("debug Client closed")

    def drawCvFrame(self, frame):
        #print(frame.shape[:2])
        jpg_quality = 80
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality]
        result, encoded_img = cv2.imencode('.jpg', frame, encode_param)
        #print(encoded_img.nbytes)
        while encoded_img.nbytes > self.max_size:
            jpg_quality -= 5
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality]
            result, encoded_img = cv2.imencode('.jpg', frame, encode_param)
        #print(encoded_img.nbytes)
        if result:
            #print(encoded_img.nbytes)
            data = encoded_img.tobytes() 
            self.sock.sendto(data, (self._ip, self._port))
