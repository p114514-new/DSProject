import pygame
from enemy import Enemy


class Boss(Enemy):
    def __init__(self, pos, playerpos, movepath, group, obstacle_sprite, trap_sprite, mapp):
        super(Boss, self).__init__(pos, playerpos, movepath, group, obstacle_sprite, trap_sprite, mapp)
        self.import_assets()
        self.speed = 180
        self.ATK = 68
        self.HP = 250
        self.DEF = 60

    def import_assets(self):
        pass
