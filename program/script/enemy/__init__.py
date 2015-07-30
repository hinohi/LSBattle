#coding: utf8
from ..common import Block, color_func, high_func_num

from .character import character
from .bullet import bullet
from .flame import flame
from .timer import timer
from .hpbar import hpbar


class Enemy(Block):
    def __init__(self):
        self.characters = []
        self._characters_obj = character
        self.bullet = bullet()
        self.flame = flame()
        self.timer = timer()
        self.hpbar = hpbar()
        self.repulsion = 100.0
        self._repulsion_func = high_func_num(float, 0.0, 1000.0)
