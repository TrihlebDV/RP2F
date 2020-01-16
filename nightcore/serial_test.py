#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import threading

class ArdHandler(threading.Thread):
    def __init__(self, func=None):
        threading.Thread.__init__(self)
        self.deamon = True
        self._inReady = threading.Event()
        self._stopped = threading.Event()
        self.req = None
        self._setter = func

        self.ser = serial.Serial('/dev/ttyACM0', 9600)
        
    def config(self):
        self._setter("ArdHandler started!")
        buff = self.ser.readline()
        if not 49-buff[0]: self._setter("ARD: sensor ready for work")
        else: self._setter("ARD: can't connect to sensor")
        buff = self.ser.readline()
        buff = buff[:-2]
        count = int(buff)
        self._setter("ARD: Saved {} fingerprints".format(count))

    def read(self):
        self.ser.write(bytes("0", encoding = 'UTF-8'))
        while not self._stopped.is_set():
            buff = self.ser.readline()
            buff = buff[:-2]
            self._setter(str(buff))
            if b'Found ID' in buff:
                sp = buff.split(b' ')
                sp2 = sp[2]
                c = sp2[1:]
                return int(c)

    def write(self, count):
        self.ser.write(bytes("1", encoding = 'UTF-8'))
        while not self._stopped.is_set():
            buff = self.ser.readline()
            buff = buff[:-2]
            self._setter(str(buff))
            if b'AAA' in buff:
                break
        self.ser.write(bytes(str(count), encoding = 'UTF-8'))
        while not self._stopped.is_set():
            buff = self.ser.readline()
            buff = buff[:-2]
            self._setter(str(buff))
            if b'AAA' in buff:
                break
                    
            
    def run(self):
        self.config()
        try:
            while not self._stopped.is_set():
                self._inReady.wait()
                self.ser.write(bytes(self.req, encoding = 'UTF-8'))
                self.req = None
                while not self._stopped.is_set():
                    buff = self.ser.readline()
                    buff = buff[:-2]
                    if buff == b'AAA':break
                    if b'Found ID' in buff:
                        self._setter("it's work )")
                    self._setter(str(buff))
                self._inReady.clear()
                self._setter("RPI: exit")
                    
        except Exception as e:
            print(e)
            self._setter("ARD: connect broken")
        finally:
            self._setter("ArdHandler stopped")

    def stop(self):
        self._stopped.set()
        self._inReady.set()
