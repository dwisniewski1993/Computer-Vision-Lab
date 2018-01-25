import copy
import cv2
import pygame
from boxes import MainBox

face_cascade = cv2.CascadeClassifier('xml/haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier('xml/haarcascade_eye.xml')

SCALE_FACTOR = 1.3
MIN_NEIGHBORS = 5
FACE_COLOR = (255, 0, 0)  # B G R
EYES_COLOR = (0, 255, 0)  # B G R
BORDER_SIZE = 1
FONT_COLOR = (42, 75, 111)

font = pygame.font.Font("font.ttf", 13)

class ImageOpenCV:
    def __init__(self, name):
        self.width = None
        self.height = None
        self.file_name = str()
        self.image = None
        self.image_wth_borders = None
        self.image_original = None
        self.gray = None
        self.faces = None
        # self.eyes = None
        self.load_image(name)

    def load_image(self, name):
        self.file_name = name
        self.image = cv2.imread(name)
        self.width = self.image.shape[1]
        self.height = self.image.shape[0]
        self.image_wth_borders = copy.deepcopy(self.image)
        self.image_original = copy.deepcopy(self.image)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.detect_faces_and_eyes()

    def detect_faces_and_eyes(self):
        self.faces = face_cascade.detectMultiScale(self.gray, SCALE_FACTOR, MIN_NEIGHBORS)
        for (x, y, width, height) in self.faces:
            cv2.rectangle(self.image_wth_borders, (x, y), (x+width, y+height), FACE_COLOR, BORDER_SIZE)

            # roi_gray = self.gray[y:y+height, x:x+width]
            # roi_color = self.image_wth_borders[y:y+height, x:x+width]
            # self.eyes = eye_cascade.detectMultiScale(roi_gray)
            # for (x_eye, y_eye, width_eye, height_eye) in self.eyes:
            #     cv2.rectangle(roi_color, (x_eye, y_eye), (x_eye+width_eye, y_eye+height_eye), EYES_COLOR, BORDER_SIZE)

    def add_mask(self, mask):
        self.image = copy.deepcopy(self.image_original)
        if mask is not None:
            for (x, y, width, height) in self.faces:
                scaled_mask = cv2.resize(mask, (width, height))

                # add alpha
                alpha_mask = scaled_mask[:, :, 3] / 255.0
                alpha_image = 1.0 - alpha_mask

                for c in range(0, 3):
                    self.image[y:y+height, x:x+width, c] = (alpha_mask * scaled_mask[:, :, c] +
                                                            alpha_image * self.image[y:y+height, x:x+width, c])

    def to_draw(self, flag=0):
        """
        default - image scaled without borders
        flag 1  - image scaled with borders
        """
        if flag == 1:
            image = self.image_wth_borders
        else:
            image = self.image
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


class MaskInstance(MainBox):
    def __init__(self, name, path, width):
        MainBox.__init__(self, 0, 0, width, 30)
        self.name = name
        if path is None:
            self.image = None
        else:
            self.image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        font_render = font.render(name.upper(), 1, FONT_COLOR)
        self.surface.blit(font_render, (5, 5))

    def draw(self):
        return self.surface

    def action(self, action):
        print("MASK CLICK " + self.name)
        return self.name, self.image


class ImageInstance(MainBox):
    def __init__(self, name, width):
        MainBox.__init__(self, 0, 0, width, 30)
        self.name = name
        font_render = font.render(name.upper(), 1, FONT_COLOR)
        self.surface.blit(font_render, (5, 5))

    def draw(self):
        return self.surface

    def action(self, action):
        print("IMAGE CLICK " + self.name)
        return self.name
