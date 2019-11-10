#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            )
        for (x, y, w, h) in faces:
            if x < w/3: x = 0
            if y < h/3: y = 0                
            print(x, y, w, h)
        
        
        
except KeyboardInterrupt:
    print('Ctrl-c pressed')
