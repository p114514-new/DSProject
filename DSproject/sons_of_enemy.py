import pygame
from enemy import Enemy
from settings import *
import random
import A
from support import import_folder
import numpy as np
from Interface_component import *
from sound import *


class Slime(Enemy):
    def __init__(self, pos, playerpos, movepath, group, obstacle_sprite, trap_sprite, mapp, sur):
        super(Slime, self).__init__(pos, playerpos, movepath, group, obstacle_sprite, trap_sprite, mapp, sur)
        #self.HP=200
        # self.MP=50
        self.ATK=50
        self.DEF=60
        self.speed=80

    def import_assets(self):
        self.animations = {'right': [], 'left': [], 'back': [], 'right_idle': [], 'left_idle': [], 'back_idle': []}
        for animation in self.animations.keys():
            full_path = r'./sons_of_enemy/slime/' + animation
            self.animations[animation] = import_folder(full_path)

class Bat(Enemy):
    def __init__(self, pos, playerpos, movepath, group, obstacle_sprite, trap_sprite, mapp, sur):
        super(Bat, self).__init__(pos, playerpos, movepath, group, obstacle_sprite, trap_sprite, mapp, sur)
        # self.HP=100
        # self.MP=40
        self.ATK=52
        self.DEF=50
        self.speed=140
    def import_assets(self):
        self.animations = {'right': [], 'left': [], 'back': [], 'right_idle': [], 'left_idle': [], 'back_idle': []}
        for animation in self.animations.keys():
            full_path = r'./sons_of_enemy/bat/' + animation
            self.animations[animation] = import_folder(full_path)

class Ghost(Enemy):
    def __init__(self, pos, playerpos, movepath, group, obstacle_sprite, trap_sprite, mapp, sur):
        super(Ghost, self).__init__(pos, playerpos, movepath, group, obstacle_sprite, trap_sprite, mapp, sur)
        # self.HP=150
        # self.MP=100
        self.ATK=60
        self.DEF=45
        self.speed=120
    def import_assets(self):
        self.animations = {'right': [], 'left': [], 'back': [], 'right_idle': [], 'left_idle': [], 'back_idle': []}
        for animation in self.animations.keys():
            full_path = r'./sons_of_enemy/ghost/' + animation
            self.animations[animation] = import_folder(full_path)

class Goblin(Enemy):
    def __init__(self, pos, playerpos, movepath, group, obstacle_sprite, trap_sprite, mapp, sur):
        super(Goblin, self).__init__(pos, playerpos, movepath, group, obstacle_sprite, trap_sprite, mapp, sur)
        # self.HP=200
        # self.MP=40
        self.ATK=54
        self.DEF=60
        self.speed=100
    def import_assets(self):
        self.animations = {'right': [], 'left': [], 'back': [], 'right_idle': [], 'left_idle': [], 'back_idle': []}
        for animation in self.animations.keys():
            full_path = r'./sons_of_enemy/goblin/' + animation
            self.animations[animation] = import_folder(full_path)

class Magician(Enemy):
    def __init__(self, pos, playerpos, movepath, group, obstacle_sprite, trap_sprite, mapp, sur):
        super(Magician, self).__init__(pos, playerpos, movepath, group, obstacle_sprite, trap_sprite, mapp, sur)
        # self.HP=120
        # self.MP=150
        self.ATK=60
        self.DEF=40
        self.speed=100
    def import_assets(self):
        self.animations = {'right': [], 'left': [], 'back': [], 'right_idle': [], 'left_idle': [], 'back_idle': []}
        for animation in self.animations.keys():
            full_path = r'./sons_of_enemy/magician/' + animation
            self.animations[animation] = import_folder(full_path)
