#coding: utf8
from ..common import Block, color_func, high_func_num


class stardust(Block):
    def __init__(self):
        self.num = 50000
        self.color = (0.6, 0.6, 0.6, 0.9)
        self.size = 0.005
        self.range = 3.0
        self._num_func = high_func_num(int, 1, 10**10)
        self._color_func = color_func
        self._size_func = high_func_num(float, 0.0001, 1000)
        self._range_func = high_func_num(float, 1.0, 10000.0)
