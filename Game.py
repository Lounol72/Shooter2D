import pygame
from Player import Player
from Zombie import Monster
import os
import time
import csv

class Game:
    def __init__(self):
        self.max_monster = 10  # Example value, set this appropriately
        self.all_monsters = pygame.sprite.Group()
        self.is_playing = False
        self.Game_over = False
        self.player = Player(self)
        self.monster_velocity = 1  # Initialize monster velocity
        self.monster_attack = 1  # Initialize monster attack
        self.monster_health = 1 # Initialize monster health
        # Other initializations...
        self.Difficulty = {
            'easy': [1, 1, 0.5, 2],
            'normal': [1, 1, 1, 4],
            'hard': [1.5, 1.5, 1.5, 6],
            'cauchemar': [2, 2, 1.75, 8],
        }

        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)

        self.all_monsters = pygame.sprite.Group()
        self.pressed = {}
        self.fic = 'score/best.csv'
        self.ground_level = 720
        self.max_score = self.read_max_score()

    def read_fic(self):
        self.player_high_score = []
        os.makedirs(os.path.dirname(self.fic), exist_ok=True)
        try:
            with open(self.fic, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        self.player_high_score.append(int(row[0]))
        except FileNotFoundError:
            pass

    def read_max_score(self):
        try:
            with open(self.fic, 'r') as file:
                scores = file.readlines()
                if scores:
                    return max(int(score.strip()) for score in scores)
        except FileNotFoundError:
            return 0
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
        
        player.moving = pressed[pygame.K_q] or pressed[pygame.K_d] or pressed[pygame.K_z] or pressed[pygame.K_s]
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
        self.monster_velocity = self.Difficulty[chosen][0]
        self.monster_attack = self.Difficulty[chosen][1]
        self.monster_health_multiplier = self.Difficulty[chosen][2]

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

        score_file = self.fic
        sync_file = "assets/PNG/War2/fic.txt"

        try:
            with open(score_file, 'a') as file:
                file.write(f"{self.player.score}\n")

            current_time = time.time()
            os.utime(score_file, (current_time, current_time))
            os.utime(sync_file, (current_time, current_time))
        except Exception as e:
            print(f"Error updating score file: {e}")

        # Update max score if current score is higher
        if self.player.score > self.max_score:
            self.max_score = self.player.score
            self.write_max_score(self.max_score)

        # Reset game state and return to main menu
        self.is_playing = False
        self.Game_over = False

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def start(self):
        self.is_playing = True
        self.update_difficulty('normal')
        self.spawn_monster()