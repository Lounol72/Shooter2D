import pygame
from Player import Player
from Bullets import bullet

class Game:
    def __init__(self):
        self.player = Player()
        self.pressed = {}