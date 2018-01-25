import pygame
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
IMAGE_BG_COLOR = (0, 0, 0)  # R G B


def cv2pygame(image):
    return pygame.image.frombuffer(image.tostring(), image.shape[1::-1], "RGB")


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
        if not self.image:
            self.image = ImageOpenCV(name)
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
        self.image_converted = pygame.image.frombuffer(self.image.to_draw().tostring(), self.image.to_draw().shape[1::-1], "RGB")
        self.change_position(0, 0)

    def change_position(self, x, y):
        x_percent = x / self.width
        y_percent = y / self.height
        if self.x_pivot:
            x_position = self.x_pivot
        else:
            x_position = -int(round(x_percent * self.x_delta, 0))
        if self.y_pivot:
            y_position = self.y_pivot
        else:
            y_position = -int(round(y_percent * self.y_delta, 0))
        if self.image_converted:
            self.draw.fill(IMAGE_BG_COLOR)
            self.draw.blit(self.image_converted, (x_position, y_position))


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
                        self.image_display.change_position(event.pos[0]-BOX_WIDTH, event.pos[1]-BAR_HEIGHT)

    def run(self):
        while True:
            self.main_display.fill((24, 131, 215))
            self.event()
            self.main_display.blit(self.masks_box, (0, 0))
            self.main_display.blit(self.images_box, (RESOLUTION_X-BOX_WIDTH, 0))
            self.main_display.blit(self.menu_bar, (BOX_WIDTH, 0))
            self.main_display.blit(self.image_display.draw, (BOX_WIDTH, BAR_HEIGHT))
            pygame.display.update()


if __name__ == "__main__":
    print("Program is running")
    app = InterfaceModule()
    app.run()
