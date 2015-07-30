# coding: utf8
# world.py
from math import pi
from random import random, randint

from OpenGL.GL import *

from go import Vector3, Vector4D, Matrix44, Lorentz
from entity import Player
from entity import Enemies
from entity import WireFrame
from entity import Sky
from entity import SolarSystem
from entity import Item
from program.const import *


class World(object):

    def __init__(self, playerstate, level, scale=1.0, L=10, item=None):
        self.level = level
        self.scale = scale
        L *= scale
        self.L = L
        self.wireframe = WireFrame(scale)
        self.sky = Sky()
        self.player = Player(self, playerstate, Vector4D(0, 0, 0, L), level=level)
        self.enemies = Enemies(self)
        types = [randint(0, level.types - 1)for i in xrange(level.enemy_num-1)]
        types += [level.types-1]
        for typ in types:
            x = 6*L*(2.0*random()-1.0)
            y = 6*L*(2.0*random()-1.0)
            z = 6*L*(1.0*random()-2.0)
            self.enemies.add(Vector4D(0, x, y, z), typ=typ, level=self.level)

        self.solar = SolarSystem(self, self.player.P.X, scale)
        
        if item is not None and item == playerstate.gun_num:
            self.item = Item(item, self.player.P.X+Vector4D(0, 0, 0.5*scale, -5*scale), scale)
        else:
            self.item = None
            
        self.score = 0

    def action(self, keys, level, ds):
        # self.player.worldline.reset()
        # for enemy in self.enemies:
        #     enemy.worldline.reset()

        n = int(ds * 10.0) + 1
        ds /= n
        count = 0
        while count < n:
            self.player.action(keys, level, ds)
            self.score += self.enemies.action(ds)
            self.solar.hit_check(self.player.P.X)
            
            if (self.item is not None and
                self.player.P.X.distance_to_squared(self.item.X) < self.player.collision_radius2*4):
                self.player.state.gun_get()
                self.player.gun_get_time = self.player.time
                self.item = None
            elif self.item is not None:
                self.item.action(ds)

            count += 1

        # self.player.worldline.cut()
        # for enemy in self.enemies:
        #     enemy.worldline.cut()

    def draw(self, keys):
        L = Lorentz(self.player.P.U)
        LL = Lorentz(-self.player.P.U)
        Xp = self.player.P.X
        matrix = self.player.quaternion.get_RotMat()
        if keys.k_look_behind:
            matrix *= Matrix44.y_rotation(pi)
        matrix_i = matrix.get_inverse_rot()

        glDisable(GL_DEPTH_TEST)
        glLoadMatrixd(matrix_i.to_opengl())
        self.sky.draw(matrix_i, LL)
        if keys.k_map:
            self.wireframe.draw(Xp, L)
        glEnable(GL_DEPTH_TEST)
        self.solar.draw(Xp, L, LL)
        self.enemies.draw(Xp, L, LL)
        if self.item is not None:
            self.item.draw(Xp, L, LL)
        
        for gun in self.player.guns:
            gun.bullets.draw(Xp, L)
        self.enemies.bullets.draw(Xp, L)

        if keys.k_map:
            glDisable(GL_DEPTH_TEST)
            self.player.draw_window(L)
            glEnable(GL_DEPTH_TEST)
            self.player.draw_hp()
            self.player.draw_gun_name()
        self.player.draw_booster(keys)
