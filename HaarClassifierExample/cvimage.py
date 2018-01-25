import copy
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

SCALE_FACTOR = 1.3
MIN_NEIGHBORS = 5
FACE_COLOR = (255, 0, 0)  # B G R
EYES_COLOR = (0, 255, 0)  # B G R
BORDER_SIZE = 1


class ImageOpenCV:
    def __init__(self, name):
        self.file_name = str()
        self.image = None
        self.image_wth_borders = None
        self.gray = None
        self.faces = None
        self.eyes = None
        self.load_image(name)

    def load_image(self, name):
        self.file_name = name
        self.image = cv2.imread(name)
        self.image_wth_borders = copy.deepcopy(self.image)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.detect_faces_and_eyes()

    def detect_faces_and_eyes(self):
        self.faces = face_cascade.detectMultiScale(self.gray, SCALE_FACTOR, MIN_NEIGHBORS)
        for (x, y, width, height) in self.faces:
            cv2.rectangle(self.image_wth_borders, (x, y), (x+width, y+height), FACE_COLOR, BORDER_SIZE)

            roi_gray = self.gray[y:y+height, x:x+width]
            roi_color = self.image_wth_borders[y:y+height, x:x+width]
            self.eyes = eye_cascade.detectMultiScale(roi_gray)
            for (x_eye, y_eye, width_eye, height_eye) in self.eyes:
                cv2.rectangle(roi_color, (x_eye, y_eye), (x_eye+width_eye, y_eye+height_eye), EYES_COLOR, BORDER_SIZE)
