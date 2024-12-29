import pygame


class bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.velocity = 7
        self.player = player
        self.image = pygame.image.load("assets/Personnages/5 Bullets/10.png")
        self.rect = self.image.get_rect()
        self.init_x = player.rect.x + 100
        self.rect.x = player.rect.x + 100

        self.rect.y = player.rect.y + 20
        self.range = 250

    def remove(self):
        self.player.all_bullets.remove(self)

    def move(self):
        self.rect.x += self.velocity
        for monster in self.player.game.check_collision(self, self.player.game.all_monsters):
            self.remove()
            monster.damage(self.player.attack)
        if self.rect.x > 1080 or self.rect.x - self.init_x > self.range:
            self.remove()
            
    def update(self):
        self.move()
