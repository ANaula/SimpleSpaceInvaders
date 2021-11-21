import pygame
from Button import Button
from sys import exit


class InstructionsState:
    def __init__(self, window):
        self.window = window
        self.background_surface = pygame.image.load("images/siInstructions.png").convert_alpha()
        self.button = Button(self.window, self.window.get_width()/2, 815, 220, 65, (169, 169, 169), (128, 128, 128), (105, 105, 105), "Main Menu")
        self.next_state = "Instructions"
        self.end_state = False
        pygame.mixer.music.load("sounds/instructions_background.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

    def draw(self):
        self.window.blit(self.background_surface, (0, 0))
        self.button.draw()

    def run_state(self):
        clock = pygame.time.Clock()
        while not self.end_state:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                self.button.hover(pos)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button.click(pos):
                        self.next_state = "Main_Menu"
                        self.end_state = True

            self.draw()

            pygame.display.update()
            clock.tick(60)
        pygame.mixer.music.stop()
