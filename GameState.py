import pygame
from Player import Player
from sys import exit
from Enemies import Enemy
from lasers import Laser
from random import randrange
from drops import Drops
import math

# Game state controls the game itself including the player controls, enemy spawns, health and armor spawns, level
# control, health and shield counters, planet life counter, and player and enemy laser and shell control.
# The goal of the game is to get as many points as possible as each level spawns more and more enemies as well as
# more health and armor pickups.


class GamesState:
    def __init__(self, window):
        self.window = window
        self.background_surface = pygame.image.load("images/spacebackground.png").convert_alpha()

        # Player and enemy sprite groups. Enemies are added to their sprite group as the levels progress
        self.player_group = pygame.sprite.GroupSingle()
        self.player_group.add(Player(self.window.get_width()/2, self.window.get_height()/2+300, self.window))
        self.enemies_group = pygame.sprite.Group()

        # Game variables
        self.level = 0
        self.player_health = 10
        self.world_health = 15

        # Health and shield bar variables
        self.total_player_health_surface = pygame.Surface((100, 20))
        self.total_player_health_surface.fill((105, 105, 105))
        self.total_player_health_rect = self.total_player_health_surface.get_rect(center=(self.player_group.sprite.rect.centerx, self.player_group.sprite.rect.centery + 80))
        self.current_player_health_surface = pygame.Surface((100, 20))
        self.current_player_health_surface.fill((0, 255, 0))
        self.current_player_health_rect = self.current_player_health_surface.get_rect(center=(self.player_group.sprite.rect.centerx, self.player_group.sprite.rect.centery + 80))
        self.shield_number = 0
        self.shield_surface = pygame.Surface((self.shield_number * 10, 20))
        self.shield_surface.fill((96, 123, 141))
        self.shield_rect = self.shield_surface.get_rect(center=(self.player_group.sprite.rect.centerx, self.player_group.sprite.rect.centery + 80))

        # laser variables
        self.player_lasers = pygame.sprite.Group()
        self.player_laser_cooldown = 0
        self.enemy_lasers = pygame.sprite.Group()
        self.enemy_shells = pygame.sprite.Group()

        # level transition variables
        self.transition = False
        self.text_font = pygame.font.Font("font/Lato-BlackItalic.ttf", 150)
        self.small_text_font = pygame.font.Font("font/Lato-Regular.ttf", 40)
        self.end_font = pygame.font.Font("font/Lato-BlackItalic.ttf", 170)
        self.transition_surface = None
        self.transition_rect = None
        self.transition_time = 7

        # Game over detection variables
        self.game_over = False
        self.end_game_surface = self.end_font.render("Game Over", False, (255, 255, 255))
        self.end_game_rect = self.end_game_surface.get_rect(center=(self.window.get_width()/2, -20))

        # Planet health variables
        self.world_health_surface = self.small_text_font.render("Planet Health: ", False, (255, 255, 255))
        self.world_health_rect = self.world_health_surface.get_rect(topleft=(10, 10))
        self.world_health_number_surface = self.small_text_font.render(f"{self.world_health}", False, (255, 255, 255))
        self.world_health_number_rect = self.world_health_number_surface.get_rect(topleft=self.world_health_rect.topright)

        # Points display variables
        self.points = 0
        self.points_surface = self.small_text_font.render(f"Points: {self.points}", False, (255, 255, 255))
        self.points_rect = self.points_surface.get_rect(topright=(self.window.get_width()-10, 10))

        # health and shield drops and shield variables
        self.health_drops_group = pygame.sprite.Group()
        self.shield_drops_group = pygame.sprite.Group()
        self.shield_font = pygame.font.Font("font/Lato-Regular.ttf", 20)
        self.shield_down_surface = self.shield_font.render("Shield Down!", False, (255, 255, 255))
        self.shield_down_rect = self.shield_down_surface.get_rect(center=(self.player_group.sprite.rect.centerx, self.player_group.sprite.rect.centery + 80 + self.shield_down_surface.get_height()))
        self.shield_destroyed = False
        self.shield_down_timer_length = 11
        self.shield_down_timer = self.shield_down_timer_length

        self.pickup_list = []
        self.paused = False
        self.state_done = False
        self.end_game_timer = 15
        self.next_state = "Game"

        # Sounds
        self.next_level_sound = pygame.mixer.Sound("sounds/next_level.wav")
        self.next_level_sound.set_volume(0.5)
        self.player_laser_shot_sound = pygame.mixer.Sound("sounds/player_laser_fire.wav")
        self.player_laser_shot_sound.set_volume(0.2)
        self.enemy_laser_shot_sound = pygame.mixer.Sound("sounds/enemy_laser_fire.wav")
        self.enemy_laser_shot_sound.set_volume(0.1)
        self.enemy_shell_shot_sound = pygame.mixer.Sound("sounds/enemy_shell_fire.wav")
        self.enemy_shell_shot_sound.set_volume(0.1)
        self.enemy_player_collision_sound = pygame.mixer.Sound("sounds/player_enemy_collision.wav")
        self.enemy_player_collision_sound.set_volume(0.5)
        self.laser_impact_on_player_sound = pygame.mixer.Sound("sounds/laser_impact_on_player.wav")
        self.laser_impact_on_player_sound.set_volume(0.5)
        self.laser_impact_on_shield_sound = pygame.mixer.Sound("sounds/laser_impact_on_shield.wav")
        self.laser_impact_on_shield_sound.set_volume(0.9)
        self.shell_impact_on_shield_sound = pygame.mixer.Sound("sounds/shell_impact_on_shield.wav")
        self.shell_impact_on_shield_sound.set_volume(0.5)
        self.shell_impact_on_player_sound = pygame.mixer.Sound("sounds/shell_impact_on_player.wav")
        self.shell_impact_on_player_sound.set_volume(0.5)
        self.shell_explosion_sound = pygame.mixer.Sound("sounds/shell_explosion.wav")

        self.enemy_destroyed_sound = pygame.mixer.Sound("sounds/enemy_destroyed.wav")
        self.enemy_destroyed_sound.set_volume(0.2)
        self.player_destroyed_sound = pygame.mixer.Sound("sounds/player_destroyed.wav")
        self.player_destroyed_sound.set_volume(0.5)
        self.shield_down_sound = pygame.mixer.Sound("sounds/player_shield_down.wav")
        self.shield_down_sound.set_volume(0.6)

        self.acquired_drop_sound = pygame.mixer.Sound("sounds/healtharmor_pickup.wav")
        self.acquired_drop_sound.set_volume(0.5)
        self.health_armor_full_sound = pygame.mixer.Sound("sounds/healthshield_full.wav")
        self.health_armor_full_sound.set_volume(0.5)

    def update_health(self):
        self.total_player_health_rect.center = (self.player_group.sprite.rect.centerx, self.player_group.sprite.rect.centery + 80)
        if self.player_health < 0:
            self.player_health = 0

        self.current_player_health_surface = pygame.Surface((self.player_health * 10, 20))
        self.current_player_health_surface.fill((0, 255, 0))
        self.current_player_health_rect = self.current_player_health_surface.get_rect(center=(self.player_group.sprite.rect.centerx, self.player_group.sprite.rect.centery + 80))

        self.shield_surface = pygame.Surface((self.shield_number * 10, 20))
        self.shield_surface.fill((96, 123, 141))
        self.shield_rect = self.shield_surface.get_rect(center=(self.player_group.sprite.rect.centerx, self.player_group.sprite.rect.centery + 80))

        if self.world_health >= 5:
            self.world_health_number_surface = self.small_text_font.render(f"{self.world_health}", False, (255, 255, 255))
        else:
            self.world_health_number_surface = self.small_text_font.render(f"{self.world_health}", False, (255, 51, 51))

    def shield_down_update(self):
        self.shield_down_rect = self.shield_down_surface.get_rect(center=(self.player_group.sprite.rect.centerx, self.player_group.sprite.rect.centery + 80 + self.shield_down_surface.get_height()))

    def drop_update(self):
        for health_drops in self.health_drops_group:
            if health_drops.rect.top >= self.window.get_height():
                self.health_drops_group.remove(health_drops)
        for shield_drops in self.shield_drops_group:
            if shield_drops.rect.top >= self.window.get_height():
                self.shield_drops_group.remove(shield_drops)

    def pickup_update(self):
        if self.pickup_list:
            for item in self.pickup_list:
                item[1].y += 2
                if item[1].top >= item[2]:
                    self.pickup_list.remove(item)

    def pickup_render(self):
        if self.pickup_list:
            for item in self.pickup_list:
                self.window.blit(item[0], item[1])

    def shield_down_render(self):
        self.shield_down_timer -= 0.1
        if not math.ceil(self.shield_down_timer) % 3 == 0:
            self.window.blit(self.shield_down_surface, self.shield_down_rect)
        if self.shield_down_timer <= 0:
            self.shield_down_timer = self.shield_down_timer_length
            self.shield_destroyed = False

    def render_health(self):
        self.window.blit(self.total_player_health_surface, self.total_player_health_rect)

        self.window.blit(self.current_player_health_surface, self.current_player_health_rect)

        self.window.blit(self.shield_surface, self.shield_rect)

    def update_points(self):
        self.points_surface = self.small_text_font.render(f"Points: {self.points}", False, (255, 255, 255))
        self.points_rect = self.points_surface.get_rect(topright=(self.window.get_width()-10, 10))

    def render_world_health_and_points(self):
        self.window.blit(self.world_health_surface, self.world_health_rect)
        self.window.blit(self.world_health_number_surface, self.world_health_number_rect)
        self.window.blit(self.points_surface, self.points_rect)

    def player_laser_fire(self):
        keys = pygame.key.get_pressed()
        if self.player_laser_cooldown != 0:
            self.player_laser_cooldown -= 0.1
        if keys[pygame.K_SPACE] and self.player_laser_cooldown <= 0:
            self.player_laser_cooldown = 3
            self.player_lasers.add(Laser(self.player_group.sprite.rect.centerx, self.player_group.sprite.rect.top, self.window, "player"))
            self.player_laser_shot_sound.play()

    def player_laser_collision(self):
        for laser in self.player_lasers:
            for enemy in self.enemies_group:
                if pygame.sprite.collide_mask(laser, enemy):
                    self.enemies_group.remove(enemy)
                    self.player_lasers.remove(laser)
                    self.points += 1
                    self.enemy_destroyed_sound.play()
                    break
            for enemy_shell in self.enemy_shells:
                if pygame.sprite.collide_mask(enemy_shell, laser):
                    self.enemy_shells.remove(enemy_shell)
                    self.player_lasers.remove(laser)
                    self.shell_explosion_sound.play()
                    break
            if laser.rect.bottom <= -1500:
                self.player_lasers.remove(laser)

    def enemy_projectile_fire(self):
        for enemy in self.enemies_group:
            if randrange(0, 7 * 60) == 1:
                if randrange(0, 4) == 1:
                    self.enemy_shells.add(Laser(enemy.rect.centerx, enemy.rect.bottom, self.window, "enemy", "shell"))
                    self.enemy_shell_shot_sound.play()
                else:
                    self.enemy_lasers.add(Laser(enemy.rect.centerx, enemy.rect.bottom, self.window, "enemy"))
                    self.enemy_laser_shot_sound.play()

    def enemy_projectile_collision(self):
        for laser in self.enemy_lasers:
            if pygame.sprite.collide_mask(laser, self.player_group.sprite):
                if self.shield_number > 0:
                    self.shield_number -= 1
                    self.laser_impact_on_shield_sound.play()
                    if self.shield_number <= 0:
                        self.shield_destroyed = True
                        self.shield_down_sound.play()
                else:
                    self.player_health -= 1
                    self.laser_impact_on_player_sound.play()
                self.enemy_lasers.remove(laser)
                break
            if laser.rect.top >= self.window.get_height():
                self.enemy_lasers.remove(laser)

        shell_damage = 3
        for shell in self.enemy_shells:
            if pygame.sprite.collide_mask(shell, self.player_group.sprite):
                if self.shield_number > 0:
                    self.shield_number -= shell_damage
                    self.shell_impact_on_shield_sound.play()
                    if self.shield_number <= 0:
                        self.player_health += self.shield_number
                        self.shield_number = 0
                        self.shield_destroyed = True
                        self.shield_down_sound.play()
                        self.shell_impact_on_player_sound.play()
                else:
                    self.player_health -= shell_damage
                    self.shell_impact_on_player_sound.play()
                self.enemy_shells.remove(shell)
                break
            if shell.rect.top >= self.window.get_height():
                self.enemy_shells.remove(shell)

    def enemy_update(self):
        for enemy in self.enemies_group:
            if enemy.rect.top >= self.window.get_height():
                self.enemies_group.remove(enemy)
                self.world_health -= 1

    def transition_update(self):
        if self.transition_rect.centery <= self.window.get_height()/2:
            self.transition_rect.y += 4
        if self.transition_rect.centery >= self.window.get_height()/2:
            self.transition_time -= 0.1
            if self.transition_time <= 0:
                self.transition = False
                self.transition_time = 5

# The game runs as normal until either there is a transition period where a new level starts and text displaying the
# level number appears or if the game is over.

    def update(self):
        if not self.transition and not self.game_over:
            self.end_check()
            self.player_group.update()
            self.update_health()
            self.player_laser_fire()
            self.enemy_projectile_fire()
            self.enemies_group.update()
            self.enemy_update()
            self.player_lasers.update()
            self.enemy_lasers.update()
            self.enemy_shells.update()
            self.health_drops_group.update()
            self.shield_drops_group.update()
            self.drop_update()
            self.player_enemy_collision()
            self.player_laser_collision()
            self.update_points()
            self.enemy_projectile_collision()
            self.player_drop_collision()
            self.pickup_update()
            if self.shield_destroyed:
                self.shield_down_update()
        else:
            if self.transition:
                self.transition_update()
            else:
                self.end_update()

    def draw(self):
        self.window.blit(self.background_surface, (0, 0))
        self.player_group.draw(self.window)
        self.render_health()
        self.enemies_group.draw(self.window)
        self.player_lasers.draw(self.window)
        self.enemy_lasers.draw(self.window)
        self.enemy_shells.draw(self.window)
        self.health_drops_group.draw(self.window)
        self.shield_drops_group.draw(self.window)
        self.render_world_health_and_points()
        self.pickup_render()
        if self.shield_destroyed and not self.transition and not self.game_over:
            self.shield_down_render()
        if self.transition:
            self.window.blit(self.transition_surface, self.transition_rect)
        elif self.game_over:
            self.window.blit(self.end_game_surface, self.end_game_rect)

# Here, the amount of enemies and drops that spawn depend on what the level is.

    def level_check(self):
        if not self.enemies_group:
            self.next_level_sound.play()
            self.level += 1
            self.transition = True
            self.transition_surface = self.text_font.render(f"Level {self.level}", False, (255, 255, 255))
            self.transition_rect = self.transition_surface.get_rect(center=(self.window.get_width()/2, -20))
            for x in range(5 + (2 * self.level)):
                self.enemies_group.add(Enemy(self.window))
            for z in range(1 + (1 * self.level)):
                self.health_drops_group.add(Drops(self.window, "health"))
            for y in range(1 + self.level):
                self.shield_drops_group.add(Drops(self.window, "shield"))

    def end_check(self):
        if self.player_health <= 0 or self.world_health <= 0:
            self.game_over = True
            pygame.mixer.music.stop()
            self.player_destroyed_sound.play()

    def end_update(self):
        if self.end_game_rect.centery <= self.window.get_height()/2:
            self.end_game_rect.y += 4
        if self.end_game_rect.centery >= self.window.get_height()/2:
            self.end_game_timer -= 0.1
            if self.end_game_timer <= 0:
                self.end_game_timer = 15
                self.state_done = True

    def player_enemy_collision(self):
        if self.enemies_group:
            for enemy in self.enemies_group:
                if pygame.sprite.collide_mask(self.player_group.sprite, enemy):
                    self.enemy_player_collision_sound.play()
                    self.enemies_group.remove(enemy)
                    if self.shield_number > 0:
                        self.shield_number -= 1
                        self.shell_impact_on_shield_sound.play()
                        if self.shield_number <= 0:
                            self.shield_destroyed = True
                            self.shield_down_sound.play()
                    else:
                        self.player_health -= 1

    def player_drop_collision(self):
        for health in self.health_drops_group:
            if pygame.sprite.collide_mask(self.player_group.sprite, health):
                self.health_drops_group.remove(health)
                if self.player_health < 10:
                    self.player_health += 1
                    health_drop_surface = self.shield_font.render("+10 Health!", False, (255, 255, 255))
                    health_drop_rect = health_drop_surface.get_rect(center=(self.player_group.sprite.rect.centerx, self.player_group.sprite.rect.centery + 80 + self.shield_down_surface.get_height()))
                    drop_limit = health_drop_rect.bottom + 150
                    self.pickup_list.append([health_drop_surface, health_drop_rect, drop_limit])
                    self.acquired_drop_sound.play()
                else:
                    health_full_surface = self.shield_font.render("Health Full!", False, (255, 255, 255))
                    health_full_rect = health_full_surface.get_rect(center=(self.player_group.sprite.rect.centerx, self.player_group.sprite.rect.centery + 80 + self.shield_down_surface.get_height()))
                    drop_limit = health_full_rect.bottom + 150
                    self.pickup_list.append([health_full_surface, health_full_rect, drop_limit])
                    self.health_armor_full_sound.play()

        for shield in self.shield_drops_group:
            if pygame.sprite.collide_mask(self.player_group.sprite, shield):
                self.shield_drops_group.remove(shield)
                if self.shield_number < 10:
                    self.shield_number += 1
                    shield_drop_surface = self.shield_font.render("+10 Armour", False, (255, 255, 255))
                    shield_drop_rect = shield_drop_surface.get_rect(center=(self.player_group.sprite.rect.centerx, self.player_group.sprite.rect.centery + 80 + self.shield_down_surface.get_height()))
                    drop_limit = shield_drop_rect.bottom + 150
                    self.pickup_list.append([shield_drop_surface, shield_drop_rect, drop_limit])
                    self.acquired_drop_sound.play()
                else:
                    shield_full_surface = self.shield_font.render("Shield Full!", False, (255, 255, 255))
                    shield_full_rect = shield_full_surface.get_rect(center=(self.player_group.sprite.rect.centerx, self.player_group.sprite.rect.centery + 80 + self.shield_down_surface.get_height()))
                    drop_limit = shield_full_rect.bottom + 150
                    self.pickup_list.append([shield_full_surface, shield_full_rect, drop_limit])
                    self.health_armor_full_sound.play()

    def run_state(self):
        clock = pygame.time.Clock()
        pygame.mixer.music.load("sounds/game_state_background.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        while True:
            self.paused = False
            self.level_check()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = True
                        self.state_done = True

            self.update()
            self.draw()

            pygame.display.update()
            if self.state_done:
                self.state_done = False
                if self.paused:
                    self.next_state = "Pause"
                else:
                    self.next_state = "Score"

                break
            clock.tick(60)
        pygame.mixer.music.stop()

# Get_stats and get_paused is needed since the game class needs those stats to run the ScoreState and we need to know
# if the gamestate loop was stopped due to pausing or the player losing. This will determine if we delete the GameState
# or push it down the state_queue

    def get_stats(self):
        stats = [self.points, self.level]
        return stats

    def get_paused(self):
        return self.paused




