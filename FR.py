import face_recognition
import cv2
import numpy as np

class FR(threading.Thread):
    def __init__(self, , src_image, newFrameEvent, sysWork, frame, onNameCallable):
        threading.Thread.__init__(self)
        self._src_image = src_image #pathes to source image
        self.known_face_encodings = []
        self.known_face_names = []
        self._frame = frame
        self._newFrameEvent = newFrameEvent #флаг на обработку нового кадра
        self._sysWork = sysWork
        self._onNameCallable = None
        if (not onNameCallable is None) and callable(onNameCallable):
            self._onNameCallable = onNameCallable
        self.loadParam() #Start Point

    def stop(self): #остановка потока
        self._sysWork.set()
        if not self._newFrameEvent.is_set(): #если кадр не обрабатывается
            self._frame = None
            self._newFrameEvent.set() 
        self.join()

    def loadParam(self):
        for img in self._src_image:
            obama_image = face_recognition.load_image_file(img)
            self.known_face_encodings.append(face_recognition.face_encodings(obama_image)[0])
            self.known_face_names.append(img[0 : img.find(".", 0, len(img))]) #"image.jpg" -> "image"
        print("source images read")
        if self._onNameCallable is None:
            print("Have a problem with callable function")
            self.stop()
        else:
            print("///FaceRecognition started sucsesfully")
        self.run()
            
    def run(self):
        face_locations = []
        face_encodings = []
        face_names = []
        #process_this_frame = True
        while not self._sysWork.is_set():
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

        
                    

                
            



























            
            

    
    
