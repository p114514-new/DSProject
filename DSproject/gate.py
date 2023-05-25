import pygame
from settings import *


class GateTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, roomNO):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.roomNO = roomNO
        self.pos = pos


class Gate:
    def __init__(self, roomNO, pos, x, y):
        # graphics
        self.gate_surf = pygame.transform.scale(pygame.image.load(r'./gate/100.jpg').convert_alpha(), (x, y))
        self.roomNO = roomNO
        self.pos = pos

    def create_gate_tile(self, gate_sprites):
        GateTile(self.pos, self.gate_surf, gate_sprites, self.roomNO)
        self.rect = self.gate_surf.get_rect(topleft=self.pos)
