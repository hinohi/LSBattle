#coding: utf8
from ..common import Block, color_func, high_func_num, func_str


class window(Block):
    def __init__(self):
        self.size = 0.05
        self.color = (1.0, 1.0, 1.0, 1.0)
        self.pre_size = self.size*0.5
        self.pre_color = (1.0, 0.8, 0.8, 0.8)
        self.texture = None
        self.texture_dynamic_num = 1
        self._size_func = high_func_num(float, 1e-4, 0.2)
        self._color_func = color_func
        self._pre_size_func = high_func_num(float, 1e-4, 0.2)
        self._pre_color_func = color_func
        self._texture_func = func_str
        self._texture_dynamic_num_func = int
