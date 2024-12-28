import pygame



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health =100
        self.attack = 10
        self.velocity = 5
        self.weight = 220
        self.height = 250
        self.image = pygame.transform.scale(pygame.image.load("assets/Personnages/Perso 1.png"),(self.weight, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 720-self.height

    def IsMovingLeft(self):
        pass


class Monter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pass

class Comets:
    def __init__(self):
        pass





