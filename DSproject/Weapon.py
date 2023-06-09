import pygame
from settings import *
from support import *


class Weapon(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.ATK = 100
        self.frame_index = 0
        self.pics = {'right': r'./weapon/Blade/0.png', 'left': r'./weapon/Blade/1.png', 'up': r'./weapon/Blade/2.png',
                     'down': r'./weapon/Blade/3.png'}

    def setWeapon(self, status, pos):
        self.status = status
        self.image = pygame.image.load(self.pics[self.status]).convert()
        self.rect = self.image.get_rect(topleft=pos)


