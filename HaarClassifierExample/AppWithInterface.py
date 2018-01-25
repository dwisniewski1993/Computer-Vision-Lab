import os
import pygame
import cv2
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_m, K_l, MOUSEMOTION, MOUSEBUTTONDOWN
from sys import exit

pygame.init()

from cvimage import ImageOpenCV, MaskInstance, ImageInstance
from boxes import ScrollableBox


# Config variables:
MODE = pygame.DOUBLEBUF  # [pygame.DOUBLEBUF or pygame.FULLSCREEN]
RESOLUTION_X = 800
RESOLUTION_Y = 600
BOX_WIDTH = 150
BOX_OFFSET = 7
BAR_HEIGHT = 30
FOOTER = 10
# R G B COLORS:
IMAGE_BG_COLOR = (0, 0, 0)
SCROLLABLE_BG_COLOR = (7, 13, 19)
SCROLLER_BG_COLOR = (21, 38, 56)
SLIDER_BG_COLOR = (42, 75, 111)


class ImageBox:
    def __init__(self, width, height):
        self.draw = pygame.Surface((width, height))
        self.width = width
        self.height = height
        self.x_pivot = None
        self.y_pivot = None
        self.x_delta = None
        self.y_delta = None
        self.image = None
        self.image_converted = None
        self.mode = 0

    def load_image(self, name):
        self.image = ImageOpenCV(name)
        self.mode = 0
        if self.image.width <= self.width:
            self.x_pivot = int((self.width - self.image.width) / 2)
        else:
            self.x_pivot = None
            self.x_delta = self.image.width - self.width
        if self.image.height <= self.height:
            self.y_pivot = int((self.height - self.image.height) / 2)
        else:
            self.y_pivot = None
            self.y_delta = self.image.height - self.height
        self.image_converted = pygame.image.frombuffer(self.image.to_draw(0).tostring(),
                                                       self.image.to_draw(0).shape[1::-1], "RGB")
        self.change_position(int(self.width/2), int(self.height/2))

    def change_mode(self):
        if self.mode == 0:
            self.mode = 1
        else:
            self.mode = 0
        if self.image_converted:
            self.image_converted = pygame.image.frombuffer(self.image.to_draw(self.mode).tostring(),
                                                           self.image.to_draw(self.mode).shape[1::-1], "RGB")
        if self.image is not None:
            self.change_position(int(self.width / 2), int(self.height / 2))

    def change_position(self, x, y):
        x_percent = x / self.width
        y_percent = y / self.height
        if self.x_pivot is not None:
            x_position = self.x_pivot
        else:
            x_position = -int(round(x_percent * self.x_delta, 0))
        if self.y_pivot is not None:
            y_position = self.y_pivot
        else:
            y_position = -int(round(y_percent * self.y_delta, 0))
        if self.image_converted:
            self.draw.fill(IMAGE_BG_COLOR)
            self.draw.blit(self.image_converted, (x_position, y_position))

    def put_mask(self, mask):
        if self.image is not None:
            print()
            self.image.add_mask(mask)
            self.image_converted = pygame.image.frombuffer(self.image.to_draw(0).tostring(),
                                                           self.image.to_draw(0).shape[1::-1], "RGB")
            self.change_position(int(self.width / 2), int(self.height / 2))


class InterfaceModule:
    def __init__(self):
        self.main_display = pygame.display.set_mode((RESOLUTION_X, RESOLUTION_Y), MODE)
        self.image_display = ImageBox(RESOLUTION_X - 2*BOX_WIDTH, RESOLUTION_Y - BAR_HEIGHT - FOOTER)
        self.mask = cv2.imread("glasses.png", cv2.IMREAD_UNCHANGED)

        self.masks_box = ScrollableBox(0, 0, BOX_WIDTH, RESOLUTION_Y)
        self.masks_box.background_color = SCROLLABLE_BG_COLOR

        print("Masks:")
        tmp_instance = MaskInstance("none", None, BOX_WIDTH-BOX_OFFSET)
        self.masks_box.elements.append(tmp_instance)
        for file in os.listdir("./masks"):
            if file.endswith(".png"):
                print(file[:-4])
                tmp_instance = MaskInstance(file[:-4], "./masks/"+file, BOX_WIDTH-BOX_OFFSET)
                self.masks_box.elements.append(tmp_instance)
        self.masks_box.init_scroll()

        self.images_box = ScrollableBox(RESOLUTION_X-BOX_WIDTH, 0, BOX_WIDTH, RESOLUTION_Y)
        self.images_box.background_color = SCROLLABLE_BG_COLOR
        self.active_mask_name = str()

        print("Images")
        for file in os.listdir("./"):
            if file.endswith(".jpg"):
                print(file)
                tmp_instance = ImageInstance(file, BOX_WIDTH-BOX_OFFSET)
                self.images_box.elements.append(tmp_instance)
        self.images_box.init_scroll()
        self.active_image_name = str()

        self.menu_bar = pygame.Surface((RESOLUTION_X - 2*BOX_WIDTH, BAR_HEIGHT))
        self.menu_bar.fill((7, 13, 19))

        self.footer = pygame.Surface((RESOLUTION_X - 2*BOX_WIDTH, FOOTER))
        self.footer.fill((7, 13, 19))

        self.movement = True

    def event(self):
        for event in pygame.event.get():
            # print(event)

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                print("Exiting Program")
                exit()

            if self.image_display.image_converted is not None:
                if event.type == MOUSEMOTION and self.movement:
                    if BOX_WIDTH <= event.pos[0] <= RESOLUTION_X-BOX_WIDTH:
                        if BAR_HEIGHT <= event.pos[1] <= RESOLUTION_Y-FOOTER:
                            self.image_display.change_position(event.pos[0]-BOX_WIDTH, event.pos[1]-BAR_HEIGHT)

            if event.type == KEYDOWN and event.key == K_m:
                self.image_display.change_mode()

            if event.type == KEYDOWN and event.key == K_l:
                if self.movement:
                    self.movement = False
                else:
                    self.movement = True

            if event.type == MOUSEBUTTONDOWN:
                return {"X": event.pos[0], "Y": event.pos[1], "button": event.button}
        return None

    def run(self):
        while True:
            action = self.event()
            self.main_display.blit(self.image_display.draw, (BOX_WIDTH, BAR_HEIGHT))

            change_active_mask = None
            change_active_image_name = None

            if action:
                if self.masks_box.hoover((action["X"], action["Y"])):
                    change_active_mask = self.masks_box.action(action)
                if self.images_box.hoover((action["X"], action["Y"])):
                    change_active_image_name = self.images_box.action(action)

            if change_active_mask is not None:
                self.active_mask_name, active_mask = change_active_mask
                self.image_display.put_mask(active_mask)
            if change_active_image_name is not None:
                self.active_image_name = change_active_image_name
                self.image_display.load_image(self.active_image_name)

            self.main_display.blit(self.masks_box.draw(), self.masks_box.pivot)
            self.main_display.blit(self.images_box.draw(), self.images_box.pivot)
            self.main_display.blit(self.menu_bar, (BOX_WIDTH, 0))
            self.main_display.blit(self.footer, (BOX_WIDTH, RESOLUTION_Y-FOOTER))
            pygame.display.update()


if __name__ == "__main__":
    print("Program is running")
    app = InterfaceModule()
    app.run()
