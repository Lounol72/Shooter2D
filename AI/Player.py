import pygame
from Bullets import bullet


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health =100
        self.attack = 10
        self.velocity = 5
        self.all_bullets = pygame.sprite.Group()
        self.weight = 220
        self.height = 250
        self.image = pygame.transform.scale(pygame.image.load("assets/Personnages/1 Characters/1 Biker/Idle1/1.png"),(self.weight,self.height))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 720-self.height

    def animation(self):

        pygame.display.flip()
        self.image = pygame.transform.scale(pygame.image.load("assets/Personnages/1 Characters/1 Biker/Idle1/2.png"),(self.weight,self.height))
        pygame.display.flip()
        self.image = pygame.transform.scale(pygame.image.load("assets/Personnages/1 Characters/1 Biker/Idle1/3.png"),(self.weight,self.height))
        pygame.display.flip()
        self.image = pygame.transform.scale(pygame.image.load("assets/Personnages/1 Characters/1 Biker/Idle1/4.png"),(self.weight,self.height))


    def IsMovingLeft(self):
        self.rect.x -= self.velocity

    def IsMovingright(self):
        self.rect.x += self.velocity

    def shoot(self):
        self.all_bullets.add(bullet(self))

class Monter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pass

class Comets:
    def __init__(self):
        pass





