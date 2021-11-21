import pygame
from Button import Button
from random import randint
from ScoreEnemies import ScoreEnemy
from sys import exit

class MainMenuState:
    def __init__(self, window):
        self.background_image = pygame.image.load("images/spacebackground.png").convert_alpha()
        self.window = window
        self.buttons = []
        self.buttons.append(Button(self.window, self.window.get_width()/2, 450, 220, 75, (169, 169, 169), (128, 128, 128), (105, 105, 105), "Start Game"))
        self.buttons.append(Button(self.window, self.window.get_width()/2, 575, 220, 75, (169, 169, 169), (128, 128, 128), (105, 105, 105), "How to Play"))
        self.buttons.append(Button(self.window, self.window.get_width()/2, 700, 220, 75, (169, 169, 169), (128, 128, 128), (105, 105, 105), "Quit"))
        self.big_text = pygame.font.Font("font/Lato-BlackItalic.ttf", 150)
        self.title_surface = self.big_text.render("Space Invaders", True, (255, 255, 255))
        self.title_rect = self.title_surface.get_rect(center=(self.window.get_width()/2, 225))
        self.small_text = pygame.font.Font("font/Lato-BlackItalic.ttf", 50)
        self.small_title_surface = self.small_text.render("Simple", True, (255, 255, 255))
        self.small_title_rect = self.small_title_surface.get_rect(bottomleft=(self.title_rect.left + 20, 145))
        self.enemy_group = pygame.sprite.Group()
        self.next_state = "Main_Menu"
        self.end_state = False
        pygame.mixer.music.load("sounds/main_menu_background.mp3")
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)

    def update(self):
        if not self.enemy_group or len(self.enemy_group) < 4:
            num = randint(5, 15)
            for number in range(num):
                self.enemy_group.add(ScoreEnemy(self.window, self.window.get_height(), True))

        if self.enemy_group:
            for enemy in self.enemy_group:
                if enemy.rect.left >= self.window.get_width():
                    self.enemy_group.remove(enemy)

        self.enemy_group.update()

    def draw(self):
        self.window.blit(self.background_image, (0, 0))
        self.enemy_group.draw(self.window)
        self.window.blit(self.small_title_surface, self.small_title_rect)
        self.window.blit(self.title_surface, self.title_rect)
        for button in self.buttons:
            button.draw()

    def run_state(self):
        clock = pygame.time.Clock()
        while not self.end_state:

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    button.hover(pos)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.click(pos):
                            if button.text == "Start Game":
                                self.next_state = "Game"
                                self.end_state = True
                            if button.text == "How to Play":
                                self.next_state = "Instructions"
                                self.end_state = True
                            if button.text == "Quit":
                                pygame.quit()
                                exit()

            self.update()
            self.draw()

            pygame.display.update()
            clock.tick(60)
        pygame.mixer.music.stop()

