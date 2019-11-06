import cv2
import FR
import threading
from gi.repository import GObject ,GLib#, Gtk 

cap = cv2.VideoCapture(0)
assert  cap.isOpened()
print("camera opened")

def nameWriter(names):
    print(names)


_, _frame = cap.read()

path = ["image1.jpg", "img_for_test.jpg"]

newFrameEvent = threading.Event()
sysWork = threading.Event()
workAble = threading.Event()

def frameReader():
    while not workAble.is_set():
        _, frame = cap.read()
        print("BBB")
        if not newFrameEvent.is_set():
            _frame = frame
            newFrameEvent.set()

t = threading.Thread(target = frameReader)
t.daemon = True
t.start()
#t.join()

fr = FR.FR(path, newFrameEvent, sysWork, _frame, nameWriter)
fr.start()
print("BBB1")



mainloop = GLib.MainLoop()

try:
    mainloop.run()
except (KeyboardInterrupt, SystemExit):
    print('Ctrl+C pressed')
    workAble.set()
    fr.stop()
    

if sysWork.is_set():
    print("works like clock! )")
