#!/usr/bin/python3
# -*- coding: utf-8 -*-

#lib for drawing
import numpy as np
import cv2
#import queue

img1 = cv2.imread("start.jpg")
img1 = cv2.resize(img1, (720, 480), interpolation = cv2.INTER_AREA)
img2 = cv2.imread("black_p.jpg")
img2 = cv2.resize(img2, (720, 480), interpolation = cv2.INTER_AREA)
dst = cv2.addWeighted(img1, 0.3, img2, 0.7, 0)
#print(img1.shape)
#print(img2.shape)
cv2.imshow("res", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
