import face_recognition
import numpy as np
import threading
import cv2

class FR(object):
    def __init__(self, worker=None):
        self.known_face_encodings = []
        self.worker = worker
        self.func_for_pc = worker.func_for_pc

    def read(self, iden):
        frame = self.worker.q.get()
        while not self.worker._stopped:
            frame = self.worker.q.get()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            #self.func_for_pc("getting face location")
            face_locations = face_recognition.face_locations(rgb_small_frame)
            if(len(face_locations) == 0):
                #self.func_for_pc("face not found")
                pass
            else:break
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        for face_encoding in face_encodings:
            if not len(self.known_face_encodings) == 0:
                #a = self.known_face_encodings[0]
                matches = face_recognition.compare_faces([self.known_face_encodings[0]], face_encoding)
                if matches[0]:
                    return True
        return False

    def write(self):
        frame = self.worker.q.get()
        while not self.worker._stopped:
            frame = self.worker.q.get()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            #self.func_for_pc("getting face location")
            face_locations = face_recognition.face_locations(rgb_small_frame)
            if(len(face_locations) == 0):
                #self.func_for_pc("face not found")
                pass
            else:
                #self.func_for_pc("gettign face encodings")
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                for face_encoding in face_encodings:
                    self.known_face_encodings.append(face_encoding)
                    #self.func_for_pc("written")
                    self.func_for_pc("stored")
                break
                
