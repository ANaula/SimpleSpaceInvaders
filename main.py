import pygame
from Game import Game

pygame.init()

screen = pygame.display.set_mode((1280, 900))
pygame.display.set_caption("Simple Space Invaders")
icon = pygame.image.load("images/MMEnemy.png").convert_alpha()
pygame.display.set_icon(icon)

game = Game(screen)

game.run()



