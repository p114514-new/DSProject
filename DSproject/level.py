import random
import pygame

import settings
from settings import *
from player import Player
from enemy import Enemy
from mapeditor import myMap
from medicine import Medicine
from key import Key
from gate import Gate

n = 20  # number of enemies

m = 5  # number of medicine


class Level:
    def __init__(self):
        # display surface
        self.display_surface = pygame.display.get_surface()
        self.all_block_sprites = pygame.sprite.Group()
        # sprite groups
        self.enemy_sprites = pygame.sprite.Group()
        self.temp_enemy = pygame.sprite.Group()
        self.play_sprites = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.map = myMap(self.display_surface, self.all_sprites)
        self.medicine_sprites = pygame.sprite.Group()
        self.temp_medicine = pygame.sprite.Group()
        self.key_sprites = pygame.sprite.Group()
        self.temp_key = pygame.sprite.Group()
        self.gate_sprites = pygame.sprite.Group()
        self.temp_gate = pygame.sprite.Group()
        # setup
        self.curRoom = [0, 0]
        self.RR = self.map.getRoomRC()[0]
        self.RC = self.map.getRoomRC()[1]
        self.map.drawRoom(self.curRoom[0], self.curRoom[1])
        self.isShift = 0
        self.setup()
        # print(self.map.getMoveArea())

    def run(self, dt):
        if self.player.rect.x <= 0 or self.player.rect.x >= GAME_SCREEN_WIDTH or self.player.rect.y <= 0 or self.player.rect.y >= GAME_SCREEN_HEIGHT:
            self.shiftRoom()
        self.display_surface.fill('black')
        self.map.drawRoom(self.curRoom[0], self.curRoom[1])
        playerpos = self.player.getpos()

        ####移除不在该房间的enemy 用temp保存 下次回来时调用
        for sp in self.temp_enemy:
            self.enemy_sprites.add(sp)
        for sp in self.enemy_sprites:
            if sp.roomNO[0] != self.curRoom[0] or sp.roomNO[1] != self.curRoom[1]:
                self.enemy_sprites.remove(sp)
                self.temp_enemy.add(sp)

        for sp in self.temp_medicine:
            self.medicine_sprites.add(sp)
        for sp in self.medicine_sprites:
            if sp.roomNO[0] != self.curRoom[0] or sp.roomNO[1] != self.curRoom[1]:
                self.medicine_sprites.remove(sp)
                self.temp_medicine.add(sp)

        for sp in self.temp_key:
            self.key_sprites.add(sp)
        for sp in self.key_sprites:
            if sp.roomNO[0] != self.curRoom[0] or sp.roomNO[1] != self.curRoom[1]:
                self.key_sprites.remove(sp)
                self.temp_key.add(sp)

        for sp in self.temp_gate:
            self.gate_sprites.add(sp)
            self.player.add_obstacle(sp)
        for sp in self.gate_sprites:
            if sp.roomNO[0] != self.curRoom[0] or sp.roomNO[1] != self.curRoom[1]:
                self.gate_sprites.remove(sp)
                self.player.kill_obstacle(sp)
                self.temp_gate.add(sp)

        # for sp in self.enemy_sprites:
        #     print(sp.pos_vector,sp.HP)
        self.enemy_sprites.draw(self.display_surface)
        self.play_sprites.draw(self.display_surface)
        self.medicine_sprites.draw(self.display_surface)
        self.key_sprites.draw(self.display_surface)
        self.gate_sprites.draw(self.display_surface)
        #####draw Enemy

        ###generate new enemies
        if self.isShift == 1:
            self.map.initMoveArea()
            self.map.drawRoom(self.curRoom[0], self.curRoom[1])
            self.all_block_sprites.empty()
            for sp in self.map.getBlock():
                self.all_block_sprites.add(sp)
            self.isShift = 0

        # map‘s level is above the sprite
        self.all_sprites.update(dt)
        self.play_sprites.update(dt)
        self.enemy_sprites.update(dt)
        self.medicine_sprites.update(dt)
        self.key_sprites.update(dt)
        self.gate_sprites.update(dt)
        # self.enemy_sprites.update(dt)
        # enemy gets player's position
        for sp in self.enemy_sprites:
            sp.setPlayerPos(playerpos)
        #####设置攻击对象
        self.player.setEnemy(self.enemy_sprites)
        #####kill enemy#####
        for sp in self.enemy_sprites:
            if sp.HP < 0:
                sp.kill()

        for medicine_sprite in self.medicine_sprites:
            if self.player.rect.colliderect(medicine_sprite):
                self.player.inventory['medicine'] += 1

                # delete medicine
                medicine_sprite.kill()
                break

        for key_sprite in self.key_sprites:
            if self.player.rect.colliderect(key_sprite):
                self.player.inventory['keys'] += 1

                # delete key
                key_sprite.kill()
                break

        for gate_sprite in self.gate_sprites:
            # Create a buffer zone around the gate_sprite rect
            gate_buffer = gate_sprite.rect.inflate(10, 10)
            if self.player.rect.colliderect(gate_buffer):
                if self.player.inventory['keys'] > 0:
                    self.player.inventory['keys'] -= 1

                    # delete gate
                    gate_sprite.kill()
                break

    def shiftRoom(self):
        ##情况比较多 用树考虑比较好？
        # print(self.player.rect)
        if self.player.rect.x < 0:

            if self.curRoom[0] > 0:
                self.curRoom[0] -= 1
                self.player.rect.x = GAME_SCREEN_WIDTH - 1
                self.isShift = 1
            else:
                self.player.rect.x = 0
        elif self.player.rect.x > GAME_SCREEN_WIDTH:

            if self.curRoom[0] < self.RR - 1:
                self.curRoom[0] += 1
                self.player.rect.x = 0
                self.isShift = 1
            else:

                self.player.rect.x = GAME_SCREEN_WIDTH

        elif self.player.rect.y < 0:
            if self.curRoom[1] > 0:
                self.curRoom[1] -= 1
                self.player.rect.y = GAME_SCREEN_HEIGHT - 1
                self.isShift = 1
            else:
                self.player.rect.y = 0
        elif self.player.rect.y > GAME_SCREEN_HEIGHT:

            if self.curRoom[1] < self.RC - 1:
                self.curRoom[1] += 1
                self.player.rect.y = 0
                self.isShift = 1
            else:
                self.player.rect.y = GAME_SCREEN_HEIGHT

    def setup(self):

        for i in [self.map.gate1, self.map.gate2, self.map.gate3]:
            print(i)
            roomNO = [i[1] // 4, i[0] // 4]
            pos = [(i[1] % 4 + 1) * self.map.roomxl, (i[0] % 4 + 1) * self.map.roomyl]
            globals()['self.gate' + str(i)] = Gate(roomNO, pos, self.map.roomxl, self.map.roomyl)
            globals()['self.gate' + str(i)].create_gate_tile(self.gate_sprites)

        for sp in self.map.getBlock():
            self.all_block_sprites.add(sp)

        movepath = self.map.getMoveArea()
        birthPos = []
        err = 30
        for i in range(err, GAME_SCREEN_HEIGHT - err):
            for j in range(err, GAME_SCREEN_WIDTH - err):
                if movepath[i][j] == 1 and (movepath[i + k][j + p] == 1 for k, p in [-err, err]):
                    birthPos.append((j, i))
        self.Player_birth = birthPos[random.randint(0, len(birthPos))]
        birthPos.remove(self.Player_birth)
        # print(Player_birth)
        self.player = Player(self.Player_birth, movepath, self.play_sprites, self.all_block_sprites,
                             self.map.getTrap())
        self.player.setDisplaySur(self.display_surface)
        for i in range(0, n):
            roomNO = [random.randint(0, self.RR - 1), random.randint(0, self.RC - 1)]
            pos = self.map.getRoomBirthPos(roomNO)
            globals()['self.enemy' + str(i)] = Enemy(pos, self.player.getpos(), movepath,
                                                     self.enemy_sprites, self.map.getBlock(), self.map.getTrap(),
                                                     self.map)
            globals()['self.enemy' + str(i)].roomNO = roomNO
        for i in range(0, m):
            roomNO = [random.randint(0, self.RR - 1), random.randint(0, self.RC - 1)]
            pos = self.map.getRoomBirthPos(roomNO)
            globals()['self.medicine' + str(i)] = Medicine(roomNO, pos)
            globals()['self.medicine' + str(i)].create_medicine_tile(self.medicine_sprites)

        for i in [self.map.key1, self.map.key2, self.map.key3]:
            roomNO = [i[1] // 4, i[0] // 4]
            pos = [(i[1] % 4 + 1.5) * self.map.roomxl, (i[0] % 4 + 1.5) * self.map.roomyl]
            globals()['self.key' + str(i)] = Key(roomNO, pos)
            globals()['self.key' + str(i)].create_key_tile(self.key_sprites)

