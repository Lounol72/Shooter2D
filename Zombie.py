import pygame
import random
from Animation import Animate_Sprite

class Monster(Animate_Sprite):
    def __init__(self, game):
        super().__init__('Walk_to_left_Zombie_1')
        self.is_attacking = False
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 2
        self.velocity = 2
        self.height = 120
        self.weight = 120
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint(0, 300)
        self.rect.y = 700 - self.height + 70 + random.randint(-70, 0)
        self.update_difficulty(game.monster_velocity, game.monster_attack, game.monster_health)

    def update_health_bar(self, surface):
        bar_color = (255, 0, 0)
        back_bar_color = (51, 51, 51)
        bar_position = [self.rect.x - 10, self.rect.y - 10, (self.health / self.max_health) * 100, 5]
        back_bar_position = [self.rect.x - 10, self.rect.y - 10, 100, 5]
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)

    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.max_health += 10
            self.rect.x = 1080 + random.randint(0, 300)
            self.rect.y = 700 - self.height + 70 + random.randint(-70, 0)
            self.health = self.max_health
            self.game.player.score += 5

    def update_difficulty(self, velocity, attack, health_multiplier):
        self.base_health = 100
        self.velocity = velocity
        self.attack = attack
        self.max_health = int(self.base_health * health_multiplier)
        self.health = self.max_health

    def move(self):
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x += self.velocity if self.rect.x < self.game.player.rect.x else -self.velocity
            self.is_attacking = False
        else:
            self.is_attacking = True
            self.game.player.damage(self.attack)

    def update_animation(self):
        if self.is_attacking:
            super().Update('Attack_Zombie_1', 0.33)
        elif self.rect.x < self.game.player.rect.x:
            super().Update('Walk_to_right_Zombie_1', 0.25)
        else:
            super().Update('Walk_to_left_Zombie_1', 0.25)
        self.animate()