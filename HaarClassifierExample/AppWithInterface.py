import pygame
import numpy
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
from sys import exit
from cvimage import ImageOpenCV

pygame.init()

# Configure variables:
MODE = pygame.DOUBLEBUF  # [pygame.DOUBLEBUF or pygame.FULLSCREEN]
RESOLUTION_X = 800
RESOLUTION_Y = 600


def cv2pygame(image):
    return pygame.image.frombuffer(image.tostring(), image.shape[1::-1], "RGB")


class InterfaceModule:
    def __init__(self):
        self.main_display = pygame.display.set_mode((RESOLUTION_X, RESOLUTION_Y), MODE)
        self.image = ImageOpenCV("lena.jpg", 400, 300)
        # TODO: Create Box with all masks
        # TODO: Create Box with all images in app directory

    def event(self):
        for event in pygame.event.get():
            # print(event)

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                print("Exiting Program")
                exit()

    def run(self):
        while True:
            self.main_display.fill((24, 131, 215))
            self.main_display.blit(cv2pygame(self.image.to_draw(1)), (100, 100))
            self.event()
            pygame.display.update()
            # exit()


if __name__ == "__main__":
    print("Program is running")
    app = InterfaceModule()
    app.run()
