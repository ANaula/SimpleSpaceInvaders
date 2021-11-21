import pygame
from random import randint
import math


class Drops(pygame.sprite.Sprite):
    def __init__(self, window, drop_type):
        super().__init__()
        self.window = window
        self.drop_type = drop_type
        self.speed = 1
        if drop_type == "health":
            self.image = pygame.image.load("images/health_drop.png").convert_alpha()
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.image = pygame.image.load("images/shield_drop.png").convert_alpha()
            self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect(center=self.random_location_generator())

    def update(self):
        self.rect.y += self.speed

    def random_location_generator(self):
        half_width = int(math.ceil(self.mask.get_size()[0]/2))
        rand_x = randint(0 + half_width, self.window.get_width() + 1 - half_width)
        rand_y = randint(-1500, -100)
        random_loc = (rand_x, rand_y)
        return random_loc

