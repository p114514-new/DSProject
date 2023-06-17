import random

import pygame
from enemy import Enemy
from support import import_folder


class Boss(Enemy):

    def __init__(self, pos, playerpos, movepath, group, obstacle_sprite, trap_sprite, mapp,sur):
        super(Boss, self).__init__(pos, playerpos, movepath, group, obstacle_sprite, trap_sprite, mapp,sur)

        self.import_assets()
        self.speed = 180
        self.ATK = 68
        self.HP = 250
        self.DEF = 60
        self.MP=1000
        self.display_surface=sur
        self.flag=0

    def update(self, dt):
        self.Enemy_lifebar_draw()
        self.Move(dt)
        self.animate(dt)
        self.invincibility()
        self.chasestep = 0
        r=random.randint(0,10)
        if r>=5:
            self.flag=1
        elif r<5:
            self.flag=0
        self.handMagic=self.MagicList[self.flag]
        self.doMagic()



    def import_assets(self):
        self.animations = {'right': [], 'left': [], 'back': [], 'right_idle': [], 'left_idle': [], 'back_idle': []}
        for animation in self.animations.keys():
            full_path = r'./boss'
            for image in import_folder(full_path):
                self.animations[animation].append(pygame.transform.scale(image, (42, 42)))
