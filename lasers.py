import pygame

# Controls the lasers and shells that are fired by both the enemies and the player in the game state  These lasers are
# differentiated by who shot them when defined and that decides what sprite they get and what speed they go at. If an
# enemy shoots a shell, it also gets a different sprite which moves at a different speed. Whether the enemy shoots a
# laser or shell is determined in the game state.


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, window, fired_by, laser_type="normal"):
        super().__init__()
        self.x = x
        self.y = y
        self.window = window
        self.fired_by = fired_by
        self.laser_type = laser_type
        if self.fired_by == "player":
            self.image = pygame.image.load("images/player_laser.png").convert_alpha()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.mask.get_rect(center=(x, y))
            self.laser_speed = -8
        else:
            if laser_type == "normal":
                self.image = pygame.image.load("images/enemy_laser.png").convert_alpha()
                self.mask = pygame.mask.from_surface(self.image)
                self.rect = self.mask.get_rect(center=(x, y))
                self.laser_speed = 7
            else:
                self.image = pygame.image.load("images/enemy_shell.png").convert_alpha()
                self.mask = pygame.mask.from_surface(self.image)
                self.rect = self.mask.get_rect(center=(x, y))
                self.laser_speed = 5

    def movement(self):
        self.rect.y += self.laser_speed

    def update(self):
        self.movement()
