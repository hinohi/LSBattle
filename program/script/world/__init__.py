#coding: utf8
from ..common import Block, color_func, high_func_num
from .sky import sky
from .wireframe import wireframe
from .solar import solar

class World(Block):
    def __init__(self):
        self.sky = sky()
        self.wireframe = wireframe()
        self.solar = solar()
        self.player_bullet_num_limit = 1000
        self.enemy_bullet_num_limit = 2000
        self._player_bullet_num_limit_func = high_func_num(int, 100, 10**8)
        self._enemy_bullet_num_limit_func = high_func_num(int, 100, 10**8)
