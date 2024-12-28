import pygame

class bullet(pygame.sprite.Sprite):
    def __init__(self,player):
        super().__init__()
        self.velocity = 5
        self.image = pygame.transform.scale(pygame.image.load("assets/Personnages/5_Bullets/bullet_1.png"),(10,5))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
