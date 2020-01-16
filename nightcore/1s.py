#!/usr/bin/env python3
# -*- coding: utf-8

import cv2
import zmq
import base64
import numpy as np

context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.bind('tcp://10.42.0.1:80000')
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

while True:
    try:
        buff = footage_socket.recv_string()
        ind = buff.rindex("/")
        msg = buff[ind:]
        if msg == "/":
            print("there is no msg")
        else:
            print(msg)
        frame = buff[:ind]
        img = base64.b64decode(frame)
        npimg = np.fromstring(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        cv2.imshow("Stream", source)
        cv2.waitKey(1)

    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        break

