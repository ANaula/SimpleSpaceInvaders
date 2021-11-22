import pygame
from random import randint

# Non-game enemy sprites used in non-game states such as main menu and score state. All they do is move from left to
# right. They spawn behind the left side of the window in a random location however has a limit on where its y
# coordinate could be. The spawning of these are controlled by the states that use them.


class ScoreEnemy(pygame.sprite.Sprite):
    def __init__(self, window, y_limit=300, main_menu=False):
        super().__init__()
        self.window = window
        self.y_limit = y_limit
        if not main_menu:
            self.image = pygame.image.load("images/enemy_end.png").convert_alpha()
        else:
            self.image = pygame.image.load("images/MMEnemy.png").convert_alpha()
        self.rect = self.image.get_rect(topright=self.rand_loc())
        self.speed = randint(5, 10)

    def rand_loc(self):
        rand_x = randint(-1000, 0)
        rand_y = randint(0, self.y_limit - self.image.get_height())
        rand_location = (rand_x, rand_y)
        return rand_location

    def update(self):
        self.rect.x += self.speed


