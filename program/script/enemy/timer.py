#coding: utf8
from ..common import Block, color_func, high_func_num


class timer(Block):
    def __init__(self):
        self.visible = True
        self.format = "%.1fs"
        self.size = 100.0
        self.color = (1.0, 1.0, 1.0, 1.0)
        self.position = 0.8
        self._format_func = str
        self._size_func = high_func_num(float, 0.01, 1.0)
        self._color_func = color_func
        self._position_func = high_func_num(float, -3.0, 3.0)
