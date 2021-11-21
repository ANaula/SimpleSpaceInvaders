import pygame
from Button import Button
from sys import exit


class PauseState:
    def __init__(self, window):
        self.window = window
        self.background = pygame.Surface((self.window.get_width(), self.window.get_height()))
        self.background.fill((0, 0, 0))
        self.pause_outline_surface = pygame.Surface((self.window.get_width(), 250))
        self.pause_outline_surface.fill((255, 255, 255))
        self.pause_outline_rect = self.pause_outline_surface.get_rect(topleft=(0, 100))
        self.pause_surface = pygame.Surface((self.window.get_width(), 240))
        self.pause_rect = self.pause_surface.get_rect(center=self.pause_outline_rect.center)

        self.big_font = pygame.font.Font("font/Lato-BlackItalic.ttf", 150)
        self.pause_text_surface = self.big_font.render("Paused", True, (255, 255, 255))
        self.pause_text_rect = self.pause_text_surface.get_rect(center=self.pause_rect.center)

        self.buttons = []
        self.buttons.append(Button(self.window, self.window.get_width() / 2, 475, 220, 75, (169, 169, 169), (128, 128, 128), (105, 105, 105), "Continue"))
        self.buttons.append( Button(self.window, self.window.get_width() / 2, 600, 220, 75, (169, 169, 169), (128, 128, 128), (105, 105, 105), "Main Menu"))

        self.next_state = "Pause"
        self.end_state = False

        pygame.mixer.music.load("sounds/pause_screen_background.wav")
        pygame.mixer.music.play(-1)

    def draw(self):
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.pause_outline_surface, self.pause_outline_rect)
        self.window.blit(self.pause_surface, self.pause_rect)
        self.window.blit(self.pause_text_surface, self.pause_text_rect)
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
                            if button.text == "Continue":
                                self.next_state = "Game"
                                self.end_state = True
                            if button.text == "Main Menu":
                                self.next_state = "Main_Menu"
                                self.end_state = True

            self.draw()

            pygame.display.update()
            clock.tick(60)
        pygame.mixer.music.stop()
