import face_recognition
import numpy as np
import threading
import cv2

class FR(object):
    def __init__(self, func_for_pc):
        #self._src_image = src_image #pathes to source image
        #self._frame = frame
        #self._sysWork = sysWork
        self.known_face_encodings = []
        #self.dic = {}
        self.func_for_pc = func_for_pc
        #self.loadParam() #Start Point

    def read(self, iden, cap):
        while True:
            ret, frame = cap.read()
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
                '''name = "Unknown"
                face_distances = face_recognition.face_distance(self.known_face_encodings[iden], face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                return True'''
                if matches[0]:
                    return True
        return False

    def write(self, img_src):
        while True:
            ret, frame = img_src.read()
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
                
        
    
    def run(self):
        face_locations = []
        face_encodings = []
        face_names = []
        #process_this_frame = True
        while not self._sysWork.is_set():
            print("AAA")
            self._newFrameEvent.wait()
            if not (self._frame is None):
                small_frame = cv2.resize(self._frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]
                face_locations = face_recognition.face_locations(rgb_small_frame)
                if(len(face_locations) == 0):
                    self._newFrameEvent.clear()
                    self._onNameCallable(face_names)
                else:
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                    for face_encoding in face_encodings:
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                        name = "Unknown"
                        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = known_face_names[best_match_index]
                        face_names.append(name)
                    self._onNameCallable(face_names)
                face_names.clear()
            self._newFrameEvent.clear()
        print("///FaceRecognition stopped")        
