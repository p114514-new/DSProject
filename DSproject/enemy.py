import pygame
from player import Player
from settings import *
import random
import A
from support import import_folder
import numpy as np
from Interface_component import *
from sound import *

class Enemy(Player):
    def __init__(self, pos, playerpos, movepath, group, obstacle_sprite, trap_sprite, mapp,sur):

        super(Enemy, self).__init__(pos, movepath, group, obstacle_sprite, trap_sprite,sur)
        # import assets and surface setup
        self.import_assets()
        self.status = 'right'
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.display_surface=sur
        # general setup
        self.rect = self.image.get_rect(center=pos)
        self.movepath = movepath
        # movement
        self.playerpos = playerpos
        self.direction_vector = pygame.math.Vector2(0, 0)
        self.pos_vector = pygame.math.Vector2(self.rect.center)
        self.speed = 120  # can modify later
        self.step = 50
        self.ATK = 58
        self.roomNO = [0, 0]

        self.map = mapp
        self.chasemap = np.array(self.map.toRoom(self.map.mazeMatrix, self.roomNO[1], self.roomNO[0]))
        self.cellx = self.map.roomxl
        self.celly = self.map.roomyl
        self.chasedis = self.map.roomxl * 1.1
        self.chasestep = 0

    def update(self, dt):
        self.Move(dt)
        self.animate(dt)
        self.invincibility()
        self.chasestep = 0
        self.Enemy_lifebar_draw()
    def setPlayerPos(self, playerpos):
        self.playerpos = playerpos

    def Move(self, dt):  # needs to modify later
        if (self.pos_vector - self.playerpos).magnitude() < 350 and (
                self.pos_vector - self.playerpos).magnitude() > 150:

            direction = self.chase()
            MaxStep = len(direction) - 1
            if self.chasestep >= MaxStep:
                self.chasestep = MaxStep
            print(self.chasestep, len(direction), 'ok')
            if MaxStep > 0:
                self.direction_vector = pygame.math.Vector2(direction[self.chasestep][1], direction[self.chasestep][0])
                self.move(dt)
                self.chasedis -= self.speed * dt
            if self.chasedis <= 0:
                self.chasestep += 1
                self.chasedis = self.map.roomxl * 1.1
        if (self.pos_vector - self.playerpos).magnitude() <= 50:
            self.direction_vector = -(self.pos_vector - self.playerpos)
            self.move(dt)
        else:
            left_unit_vector = pygame.math.Vector2(-1, 0)
            right_unit_vector = pygame.math.Vector2(1, 0)
            up_unit_vector = pygame.math.Vector2(0, 1)
            down_unit_vector = pygame.math.Vector2(0, -1)
            self.left = self.pos_vector + pygame.math.Vector2(-1, 0) * self.speed * dt
            self.right = self.pos_vector + pygame.math.Vector2(1, 0) * self.speed * dt
            self.up = self.pos_vector + pygame.math.Vector2(0, 1) * self.speed * dt
            self.down = self.pos_vector + pygame.math.Vector2(0, -1) * self.speed * dt
            if self.right.x > GAME_SCREEN_WIDTH:
                self.direction_vector = random.choice((left_unit_vector, up_unit_vector, down_unit_vector))
            if self.left.x < 0:
                self.direction_vector = random.choice((right_unit_vector, up_unit_vector, down_unit_vector))
            if self.up.y > GAME_SCREEN_HEIGHT:
                self.direction_vector = random.choice((left_unit_vector, right_unit_vector, down_unit_vector))
            if self.down.y < 0:
                self.direction_vector = random.choice((left_unit_vector, right_unit_vector, up_unit_vector))
            if self.step <= 0:
                self.direction_vector = random.choice(
                    (left_unit_vector, right_unit_vector, up_unit_vector, down_unit_vector))
                self.step = 100
            else:
                self.move(dt)
                self.step -= 1

        if self.direction_vector.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        elif self.direction_vector.y == -1:
            self.status = 'back'
        elif self.direction_vector.x == 1:
            self.status = 'left'
        else:
            self.status = 'right'

    def import_assets(self):
        self.animations = {'right': [], 'left': [], 'back': [], 'right_idle': [], 'left_idle': [], 'back_idle': []}
        for animation in self.animations.keys():
            full_path = r'./enemy/' + animation
            self.animations[animation] = import_folder(full_path)
    def Enemy_lifebar_draw(self):
        left = self.rect.left
        top = self.rect.top-10
        width = self.rect.left-self.rect.left
        height = 10
        outline_rect = pygame.Rect(left, top, width, height)
        pygame.draw.rect(self.display_surface, Color.WHITE, outline_rect, 1)
        life_rect = pygame.Rect(left + 1, top + 1, self.HP / 100.0 * width, height * 0.93)
        pygame.draw.rect(self.display_surface, Color.RED, life_rect)


    def chase(self):
        # print( (self.rect.x//self.cellx), self.rect.y//self.celly, self.playerpos.x//self.cellx, self.playerpos.y//self.celly)
        steps = A.Astar(self.chasemap, (self.rect.x // self.cellx), (self.rect.y // self.celly),
                        (self.playerpos.x // self.cellx), (self.playerpos.y // self.celly))
        directions = A.getDirection(steps)
        # print(directions)
        size = len(directions)
        if size < 3:
            directions.extend([[0, 0]] * (4 - size))
        return directions[:3]
