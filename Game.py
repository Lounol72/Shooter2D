import pygame
from Player import Player
from Zombie import Monster
import os
import time
import csv

class Game:
    def __init__(self):
        self.max_monster = 10
        self.difficulty = 'normal'
        self.all_monsters = pygame.sprite.Group()
        self.is_paused = False
        self.settings = False
        self.set_difficulty = False
        self.is_playing = False
        self.Game_over = False
        self.player = Player(self)
        self.monster_velocity = 1
        self.monster_attack = 1
        self.monster_health = 1
        self.Difficulty = {
            'easy': [1, 1, 0.5, 2],
            'normal': [1, 1, 1, 4],
            'hard': [1.5, 1.5, 1.5, 6],
            'cauchemar': [2, 2, 1.75, 8],
        }
        self.all_players = pygame.sprite.Group()
        self.all_players.add(self.player)
        self.pressed = {}
        self.fic = 'score/best.csv'
        self.ground_level = 720
        self.max_score = self.read_max_score()

    def read_fic(self):
        self.player_high_score = []
        os.makedirs(os.path.dirname(self.fic), exist_ok=True)
        with open(self.fic, 'r') as file:
            reader = csv.reader(file)
            self.player_high_score.extend(int(row[0]) for row in reader if row)

    def read_max_score(self):
        try:
            with open(self.fic, 'r') as file:
                scores = file.readlines()
                return max(int(score.strip()) for score in scores) if scores else 0
        except FileNotFoundError:
            return 0

    def write_max_score(self, score):
        with open(self.fic, 'a') as file:
            file.write(f"{score}\n")

    def handle_input(self):
        self.current_time = pygame.time.get_ticks()
        pressed = pygame.key.get_pressed()
        player = self.player

        if pressed[pygame.K_c] and player.able_to_shoot and self.current_time - player.delay > 200:
            player.shoot()
        if pressed[pygame.K_z] and player.rect.y >= 550:
            player.IsMovingUp()
        if pressed[pygame.K_s] and player.rect.y <= 720 - player.height:
            player.IsMovingDown()
        if pressed[pygame.K_q] and player.rect.x >= -35:
            player.IsMovingLeft()
        if pressed[pygame.K_d] and player.rect.x < (1080 - player.width):
            player.IsMovingRight()

        player.moving = any([pressed[pygame.K_q], pressed[pygame.K_d], pressed[pygame.K_z], pressed[pygame.K_s]])
        player.shooting = pressed[pygame.K_c]

        if pressed[pygame.K_r]:
            player.reload()
        if pressed[pygame.K_DELETE]:
            pygame.quit()
            quit()

    def spawn_monster(self):
        monsters_to_spawn = self.max_monster - len(self.all_monsters)
        for _ in range(monsters_to_spawn):
            self.all_monsters.add(Monster(self))

    def update_difficulty(self, chosen):
        self.monster_velocity, self.monster_attack, self.monster_health_multiplier = self.Difficulty[chosen]
        for monster in self.all_monsters:
            monster.update_difficulty(self.monster_velocity, self.monster_attack, self.monster_health_multiplier)

    def update(self, surface):
        self.current_time = pygame.time.get_ticks()
        self.check_reloading()
        self.update_player(surface)
        self.update_monsters(surface)
        self.spawn_monster()
        self.check_game_over(surface)

    def check_reloading(self):
        if self.player.reloading and 760 <= self.current_time - self.player_reloading:
            self.player.reloading = False
            self.player.able_to_shoot = True

    def update_player(self, surface):
        surface.blit(self.player.image, self.player.rect)
        self.player.all_bullets.update()
        self.player.all_bullets.draw(surface)
        self.player.update_animation()
        self.player.update_health_bar(surface)

    def update_monsters(self, surface):
        self.all_monsters.update()
        self.all_monsters.draw(surface)
        for monster in self.all_monsters:
            monster.update_health_bar(surface)
            monster.update_animation()
            monster.move()

    def check_game_over(self, surface):
        if self.Game_over:
            self.game_over(surface)

    def game_over(self, surface):
        self.all_monsters.empty()
        self.player.health = self.player.max_health
        self.write_max_score(self.player.score)
        self.is_playing = False

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def start(self):
        self.is_playing = True
        self.Game_over = False
        self.player.health = self.player.max_health
        self.player.score = 0
        self.all_monsters.empty()
        difficulty_settings = {
            "easy": (200, 1.0),
            "medium": (100, 1.5),
            "hard": (50, 2.0),
            "extreme": (25, 2.5)
        }
        self.player.max_health, self.monster_spawn_rate = difficulty_settings.get(self.difficulty, (100, 1.0))