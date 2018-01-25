import pygame
import numpy
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEMOTION
from sys import exit
from cvimage import ImageOpenCV

pygame.init()

# Configure variables:
MODE = pygame.DOUBLEBUF  # [pygame.DOUBLEBUF or pygame.FULLSCREEN]
RESOLUTION_X = 800
RESOLUTION_Y = 600
BOX_WIDTH = 150
BAR_HEIGHT = 30


def cv2pygame(image):
    return pygame.image.frombuffer(image.tostring(), image.shape[1::-1], "RGB")


class ImageBox:
    def __init__(self, width, height):
        self.image_box = pygame.Surface((width, height))
        self.width = width
        self.height = height
        self.x_pivot = None
        self.y_pivot = None
        self.position = None
        self.image = None
        self.mode = 0

    def load_image(self, name):
        if not self.image:
            self.image = ImageOpenCV(name)
            if self.image.width <= self.width:
                self.x_pivot = int((self.width - self.image.width) / 2)
            else:
                self.x_pivot = None
            if self.image.height <= self.height:
                self.y_pivot = int((self.height - self.image.height) / 2)
            else:
                self.y_pivot = None

    def change_position(self, x, y):
        self.position = self.position[0] + x, self.position[1] + y

    def draw(self):
        if self.image:
            image = pygame.image.frombuffer(self.image.to_draw.tostring(), self.image.shape[1::-1], "RGB")
            self.image_box.blit(image, self.position)


class InterfaceModule:
    def __init__(self):
        self.main_display = pygame.display.set_mode((RESOLUTION_X, RESOLUTION_Y), MODE)
        self.image_display = ImageBox(RESOLUTION_X - 2*BOX_WIDTH, RESOLUTION_Y - BAR_HEIGHT)
        self.image_display.load_image("lena.jpg")
        # TODO: Create Box with all masks
        self.masks_box = pygame.Surface((BOX_WIDTH, RESOLUTION_Y))
        self.masks_box.fill((30, 20, 10))
        # TODO: Create Box with all images in app directory
        self.images_box = pygame.Surface((BOX_WIDTH, RESOLUTION_Y))
        self.images_box.fill((10, 20, 30))
        # TODO: Create Simple Menu Bar
        self.menu_bar = pygame.Surface((RESOLUTION_X - 2*BOX_WIDTH, BAR_HEIGHT))
        self.menu_bar.fill((100, 100, 100))

    def event(self):
        for event in pygame.event.get():
            # print(event)

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                print("Exiting Program")
                exit()

            if event.type == MOUSEMOTION:
                if BOX_WIDTH <= event.pos[0] <= RESOLUTION_X-BOX_WIDTH:
                    if BAR_HEIGHT <= event.pos[1]:
                        print(event.pos)

    def run(self):
        while True:
            self.main_display.fill((24, 131, 215))
            self.main_display.blit(self.masks_box, (0, 0))
            self.main_display.blit(self.images_box, (RESOLUTION_X-BOX_WIDTH, 0))
            self.main_display.blit(self.menu_bar, (BOX_WIDTH, 0))
            self.event()
            pygame.display.update()
            # exit()


if __name__ == "__main__":
    print("Program is running")
    app = InterfaceModule()
    app.run()
