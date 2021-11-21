import pygame
from random import randint
from ScoreEnemies import ScoreEnemy
from sys import exit
from Button import Button


class ScoreState:
    def __init__(self, window, stats):
        self.window = window
        self.stats = stats
        self.background_image = pygame.image.load("images/scorescreen.png").convert_alpha()
        self.enemy_group = pygame.sprite.Group()
        self.start_score = 0
        self.font = pygame.font.Font("font/Lato-BlackItalic.ttf", 75)
        self.score_surface = self.font.render(f"Total Points:   {self.start_score}", False, (255, 255, 255))
        self.score_rect = self.score_surface.get_rect(center=(self.window.get_width()/2, self.window.get_height()/2+25))
        self.start_level = 0
        self.level_surface = self.font.render(f"Level Reached:  {self.start_level}", False, (255, 255, 255))
        self.level_rect = self.level_surface.get_rect(center=(self.window.get_width()/2, self.window.get_height()/2+(50 + self.score_rect.height)))
        self.start_timer_score = 0.5
        self.start_timer_level = 1
        self.next_state = "Score"
        self.end_state = False

        self.buttons = []
        self.buttons.append(Button(self.window, self.window.get_width()/2+150, 800, 215, 75, (169, 169, 169), (128, 128, 128), (105, 105, 105), "Main Menu"))
        self.buttons.append(Button(self.window, self.window.get_width()/2-150, 800, 215, 75, (169, 169, 169), (128, 128, 128), (105, 105, 105), "Play Again"))
        self.points_counter_sound = pygame.mixer.Sound("sounds/points_counter_sound.wav")
        self.points_counter_sound.set_volume(0.3)
        self.level_counter_sound = pygame.mixer.Sound("sounds/level_counter_sound.wav")
        self.level_counter_sound.set_volume(0.3)
        pygame.mixer.music.load("sounds/score_screen_background.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

    def update(self):
        if not self.enemy_group or len(self.enemy_group) <= 3:
            num = randint(4, 10)
            for number in range(num):
                self.enemy_group.add(ScoreEnemy(self.window))

        if self.enemy_group:
            for enemy in self.enemy_group:
                if enemy.rect.left >= self.window.get_width():
                    self.enemy_group.remove(enemy)

        self.enemy_group.update()

        if self.start_score != self.stats[0]:
            self.start_timer_score -= 0.1
            if self.start_timer_score <= 0:
                self.start_score += 1
                self.points_counter_sound.play()
                self.start_timer_score = 0.5
        if self.start_level != self.stats[1]:
            self.start_timer_level -= 0.1
            if self.start_timer_level <= 0:
                self.start_timer_level = 1
                self.start_level += 1
                self.level_counter_sound.play()
        self.score_surface = self.font.render(f"Total Points:   {self.start_score}", False, (255, 255, 255))
        self.level_surface = self.font.render(f"Level Reached:  {self.start_level}", False, (255, 255, 255))

    def draw(self):
        self.window.blit(self.background_image, (0, 0))
        self.enemy_group.draw(self.window)
        self.window.blit(self.score_surface, self.score_rect)
        self.window.blit(self.level_surface, self.level_rect)
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
                            if button.text == "Main Menu":
                                self.next_state = "Main_Menu"
                                self.end_state = True
                            if button.text == "Play Again":
                                self.next_state = "Game"
                                self.end_state = True

            self.update()
            self.draw()

            pygame.display.update()
            clock.tick(60)
        pygame.mixer.music.stop()

# main menu, pause, how to play
# Main menu moving enemies going across the screen? showing a mothership?
