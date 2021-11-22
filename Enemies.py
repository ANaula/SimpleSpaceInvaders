import pygame
from random import randint

# Enemies that are used in the game state. They spawn randomly above the top window edge but have a range of what
# their y coordinate could be. Similar to how drops spawn.


class Enemy(pygame.sprite.Sprite):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.image = pygame.image.load("images/enemy.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect(topleft=self.random_location_generator())
        self.speed = 1

    def random_location_generator(self):
        rand_x = randint(0, self.window.get_width()+1-self.image.get_width())
        rand_y = randint(-1500, -100)
        random_loc = (rand_x, rand_y)
        return random_loc

    def move(self):
        self.rect.y += self.speed

    def update(self):
        self.move()
