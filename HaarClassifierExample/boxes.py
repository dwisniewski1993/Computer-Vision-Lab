import pygame
import copy

# Config variables
DEFAULT_COLOR = (21, 38, 56)
SCROLL_COLOR = (21, 38, 56)
SLIDER_COLOR = (42, 75, 111)


class MainBox:
    def __init__(self, x, y, width, height):
        self.pivot = x, y
        self.width = width
        self.height = height

        self.surface = pygame.Surface((width, height))
        self.background_color = DEFAULT_COLOR

        self.elements = []

    def hoover(self, mouse_position):
        x_position = mouse_position[0] - self.pivot[0]
        y_position = mouse_position[1] - self.pivot[1]
        if 0 <= x_position <= self.width:
            if 0 <= y_position <= self.height:
                return True
        return False

    def draw(self):
        self.surface.fill(self.background_color)
        if self.elements:
            for element in self.elements:
                self.surface.blit(element.draw(), element.pivot)
        return self.surface

    def action(self, action):
        if self.elements:
            self.new_actions(action)

    def new_actions(self, action):
        new_action = copy.deepcopy(action)
        new_action['X'] -= self.pivot[0]
        new_action['Y'] -= self.pivot[1]
        for element in self.elements:
            if element.hoover((new_action['X'], new_action['Y'])):
                result = element.action(new_action)
                if result:
                    return result
        del new_action


class ScrollableBox(MainBox):
    class Scroll:
        def __init__(self, true_height, display_height):
            self.true_height = true_height
            self.display_height = display_height
            self.slider_height = int(display_height ** 2 / true_height)
            if self.slider_height <= 0:
                self.slider_height = 1
            self.offset = true_height - display_height
            self.position = 0

            self.surface = pygame.Surface((3, self.display_height))
            self.slider = pygame.Surface((3, self.slider_height))
            self.slider.fill(SLIDER_COLOR)
            self.color = SCROLL_COLOR

        def change_position(self, change):
            self.position += change
            if self.position > self.offset:
                self.position = self.offset
            if self.position < 0:
                self.position = 0

        def draw(self):
            self.surface.fill(self.color)
            delta = int((self.position / self.true_height) * self.display_height)
            self.surface.blit(self.slider, (0, delta))
            return self.surface

    def __init__(self, x, y, width, height):
        MainBox.__init__(self, x, y, width, height)
        self.element_dictionary = None
        self.to_draw = None
        self.scroll = None

    def init_scroll(self):
        self.element_dictionary = dict()
        if self.elements:
            counter = 0
            for element in self.elements:
                self.element_dictionary[counter] = element
                element.pivot = (5, counter)
                counter += element.height + 2
            counter -= 2
        else:
            counter = self.height
        self.scroll = self.Scroll(counter, self.height)
        self.set_drawable()

    def set_drawable(self):
        self.to_draw = list()
        tmp = 0
        first_element = True
        for key in sorted(self.element_dictionary):
            if key >= self.scroll.position:
                if key < self.scroll.position + self.height:
                    if first_element and key != self.scroll.position:
                        self.to_draw.append(tmp)
                        first_element = False
                    elif key == self.scroll.position:
                        first_element = False
                    self.to_draw.append(key)
                else:
                    break
            else:
                tmp = key

    def draw(self):
        self.surface.fill(self.background_color)
        self.surface.blit(self.scroll.draw(), (0, 0))
        if self.elements:
            for key in self.to_draw:
                self.surface.blit(self.element_dictionary[key].draw(), (5, key - self.scroll.position))
        return self.surface

    def action(self, action):
        if action['button'] == 4:
            self.scroll.change_position(-20)
        elif action['button'] == 5:
            self.scroll.change_position(20)
        self.set_drawable()
        image = self.new_actions(action)
        if image is not None:
            return image
        else:
            return None

    def new_actions(self, action):
        new_action = copy.deepcopy(action)
        new_action['X'] -= self.pivot[0]
        new_action['Y'] -= self.pivot[1] - self.scroll.position
        image = None
        for key in self.to_draw:
            if self.element_dictionary[key].hoover((new_action['X'], new_action['Y'])):
                image = self.element_dictionary[key].action(new_action)
        del new_action
        if image is not None:
            return image
