#coding: utf8
from ..common import Block, color_func, high_func_num


class bullet(Block):
    def __init__(self):
        self.color = (1.0, 0.0, 1.0, 1.0)
        self.size = 0.02
        self._color_func = color_func
        self._size_func = high_func_num(float, 0.001, 0.1)
