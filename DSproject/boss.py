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

        self.display_surface=sur

    def import_assets(self):
        self.animations = {'right': [], 'left': [], 'back': [], 'right_idle': [], 'left_idle': [], 'back_idle': []}
        for animation in self.animations.keys():
            full_path = r'./boss'
            for image in import_folder(full_path):
                self.animations[animation].append(pygame.transform.scale(image, (42, 42)))
