#coding: utf8
from ..common import Block, color_func, high_func_num
from .stardust import stardust
from .sky import sky


class World(Block):
    def __init__(self):
        self.stardust = stardust()
        self.sky = sky()
        self.player_bullet_num_limit = 1000
        self.enemy_bullet_num_limit = 2000
        self._player_bullet_num_limit_func = high_func_num(int, 100, 10**8)
        self._enemy_bullet_num_limit_func = high_func_num(int, 100, 10**8)

    def _check(self):
        for obj in [self.stardust, self.sky]:
            if hasattr(obj, "_check"):
                obj._check()
