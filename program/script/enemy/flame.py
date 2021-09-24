#coding: utf8
from ..common import Block, color_func, high_func_num


class flame(Block):
    def __init__(self):
        self.life = 0.8
        self.speed = 0.4
        self.size = 0.04
        self.color = (1.0, 1.0, 1.0, 0.8)#(0.95, 0.1, 0.1, 0.5)
        self.num = 10
        self._life_func  = high_func_num(float, 0.01, 100.0)
        self._speed_func = high_func_num(float, 0.1, 0.999)
        self._size_func  = high_func_num(float, 0.001, 1.0)
        self._color_func = color_func
        self._num_func = high_func_num(int, 4, 20)
