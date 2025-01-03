import pygame
from Bullets import bullet
from Animation import Animate_Sprite

class Player(Animate_Sprite):
    def __init__(self, game):
        super().__init__('Soldier', 0.175)
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 5
        self.all_bullets = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = 0
        self.rect.y = 720 - self.height
        self.magazine = 20
        self.score = 0
        self.delay = 0
        self.reloading = False
        self.moving = False
        self.shooting = False
        self.able_to_shoot = True

    def IsMovingLeft(self):
        self.rect.x -= self.velocity
        self.moving = True

    def IsMovingRight(self):
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity
            self.moving = True

    def IsMovingUp(self):
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.y -= self.velocity
            self.moving = True

    def IsMovingDown(self):
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.y += self.velocity
            self.moving = True

    def shoot(self):
        if self.magazine == 0:
            self.reload()
        else:
            self.shooting = True
            self.magazine -= 1
            self.all_bullets.add(bullet(self))
            self.delay = pygame.time.get_ticks()

    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.game.Game_over = True

    def reload(self):
        self.reloading = True
        self.able_to_shoot = False
        self.game.player_reloading = pygame.time.get_ticks()
        self.magazine = 20

    def update_health_bar(self, surface):
        bar_color = (255, 0, 0)
        back_bar_color = (51, 51, 51)
        bar_position = [self.rect.x + 10, self.rect.y - 10, self.health, 5]
        back_bar_position = [self.rect.x + 10, self.rect.y - 10, self.max_health, 5]
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)

    def update_animation(self):
        if not self.shooting and not self.moving and not self.reloading:
            super().Update('Soldier', 0.0875)
        else:
            if self.moving and not self.shooting:
                self.velocity = 5
                super().Update('Walk_to_right_Soldier_1', 0.375)
            if self.shooting:
                self.velocity = 2
                super().Update('Shoot_Soldier_1', 0.375)
            if self.reloading:
                self.velocity = 2
                super().Update('Reloding_Soldier_1', 0.25)
        self.animate()