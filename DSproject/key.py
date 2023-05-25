import pygame
from settings import *


class KeyTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, roomNO):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.roomNO = roomNO
        self.pos = pos


class Key:
    def __init__(self, roomNO, pos):
        # graphics
        self.key_surf = pygame.image.load(r'./key/145.png').convert_alpha()
        self.roomNO = roomNO
        self.pos = pos

    def create_key_tile(self, key_sprites):
        KeyTile(self.pos, self.key_surf, key_sprites, self.roomNO)
