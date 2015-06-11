#coding: utf8
from ..common import Block, color_func, high_func_num


class wireframe(Block):
    def __init__(self):
        self.color = (1.0, 1.0, 1.0, 0.5)
        self.range = 100.0
        self.div = 30
        self.line_width = 1
        self._color_func = color_func
        self._size_func = high_func_num(float, 0.0001, 1000)
        self._range_func = high_func_num(float, 1.0, 10000.0)
        self._div_func = high_func_num(int, 2, 100)
        self._line_width_func = high_func_num(int, 1, 10)
