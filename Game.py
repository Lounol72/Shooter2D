import pygame
from Player import Player
from Zombie import Monster
import os
import time
import csv

class Game:
    def __init__(self):
        self.max_monster = None
        self.is_playing = False
        self.Game_over = False
        self.monster_health = 1

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

    def read_fic(self):
        self.player_high_score = []
        os.makedirs(os.path.dirname(self.fic), exist_ok=True)

        score_file = self.fic
        sync_file = "assets/PNG/War2/fic.txt"

        if not os.path.exists(score_file):
            open(score_file, 'w').close()

        if not os.path.exists(sync_file):
            open(sync_file, 'w').close()

        score_mtime = os.path.getmtime(score_file)
        sync_mtime = os.path.getmtime(sync_file)

        if score_mtime != sync_mtime:
            open(score_file, 'w').close()
            os.utime(sync_file, (score_mtime, score_mtime))

        with open(score_file, 'r') as fic:
            reader = csv.reader(fic, delimiter='\n')
            self.player_high_score = [int(line[0]) for line in reader if line and line[0].isdigit()]

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def spawn_monster(self):
        monsters_to_spawn = self.max_monsters - len(self.all_monsters)
        for _ in range(monsters_to_spawn):
            self.all_monsters.add(Monster(self))

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
        
        # Correction de la logique de mouvement
        player.moving = pressed[pygame.K_q] or pressed[pygame.K_d] or pressed[pygame.K_z] or pressed[pygame.K_s]
        player.shooting = pressed[pygame.K_c]
        
        if pressed[pygame.K_r]:
            player.reload()
        if pressed[pygame.K_DELETE]:
            pygame.quit()
            quit()

    def start(self):
        self.is_playing = True
        self.difficulty('hard')
        self.spawn_monster()
        self.current_time = 0
        self.player_reloading = 0
        self.player.delay = 0

    def difficulty(self, chosen):
        self.current_difficulty = chosen
        self.max_monsters = self.Difficulty[chosen][3]
        self.monster_velocity = self.Difficulty[chosen][0]
        self.monster_attack = self.Difficulty[chosen][1]
        self.monster_health_multiplier = self.Difficulty[chosen][2]

        for monster in self.all_monsters:
            monster.update_difficulty(self.monster_velocity, self.monster_attack, self.monster_health_multiplier)

    def update(self, surface):
        self.current_time = pygame.time.get_ticks()

        if self.player.reloading and 760 <= self.current_time - self.player_reloading:
            self.player.reloading = False
            self.player.able_to_shoot = True

        surface.blit(self.player.image, self.player.rect)
        self.player.all_bullets.update()
        self.all_monsters.update()

        self.player.all_bullets.draw(surface)
        self.all_monsters.draw(surface)

        if not self.all_monsters:
            self.spawn_monster()

        for monster in self.all_monsters:
            monster.update_health_bar(surface)
            monster.update_animation()
            monster.move()
        for player in self.all_players:
            player.update_animation()
            player.update_health_bar(surface)

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

        except IOError as e:
            print(f"Error writing to file: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

        surface.blit(pygame.transform.scale(pygame.image.load('assets/Game_over.png'), (500, 120)),
                     (1080 // 2 - 500, 720 // 2 - 120))