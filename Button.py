import pygame

# This button class detects if the player is hovering their mouse over a button and changes the color of that button.
# Can also detect when the button is clicked and changes the color of the button then as well. The actions that occur
# after the button is clicked have to be defined in the states themselves, but usually involve ending that state's
# loop and changing their next_state variable


class Button:
    def __init__(self, window, x, y, width, height, default_color, hover_color, click_color, text):
        self.x = x
        self.y = y
        self.window = window
        self.width = width
        self.height = height
        self.default_color = default_color
        self.hover_color = hover_color
        self.click_color = click_color
        self.text = text
        self.font = pygame.font.Font("font/Lato-Regular.ttf", 40)

        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_surface.fill(default_color)
        self.button_rect = self.button_surface.get_rect(center=(self.x, self.y))
        self.text_surface = self.font.render(text, False, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=self.button_rect.center)

        self.button_outline_surface = pygame.Surface((self.button_rect.width+4, self.button_rect.height+4))
        self.button_outline_surface.fill((255, 255, 255))
        self.button_outline_rect = self.button_outline_surface.get_rect(center=self.button_rect.center)
        self.button_sound = pygame.mixer.Sound("sounds/button_press.mp3")
        self.button_sound.set_volume(0.2)

    def hover(self, pos):
        if self.button_rect.collidepoint(pos):
            self.button_surface.fill(self.hover_color)
        else:
            self.button_surface.fill(self.default_color)

    def click(self, pos):
        if self.button_rect.collidepoint(pos):
            self.button_surface.fill(self.click_color)
            self.button_sound.play()
            return True
        else:
            self.button_surface.fill(self.default_color)
            return False

    def draw(self):
        self.window.blit(self.button_outline_surface, self.button_outline_rect)
        self.window.blit(self.button_surface, self.button_rect)
        self.window.blit(self.text_surface, self.text_rect)

