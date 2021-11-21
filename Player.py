import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, window):
        super().__init__()
        self.x = x
        self.y = y
        self.window = window
        self.image = pygame.image.load("images/player.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect(center=(self.x, self.y))
        self.speed = 9

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if keys[pygame.K_w] and self.rect.y >= 0:
            self.rect.y -= self.speed
        if keys[pygame.K_d] and self.rect.right <= self.window.get_width():
            self.rect.x += self.speed
        if keys[pygame.K_s] and self.rect.bottom + 45 <= self.window.get_height():
            self.rect.y += self.speed

    def update(self):
        self.input()



