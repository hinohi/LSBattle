#coding: utf8
from ..common import Block, color_func, high_func_num, func_str


class gun_info(Block):
    def __init__(self):
        self.format = "GUN(%(MODE)i/%(NUM)i):%(NAME)s"
        self.color = (1.0, 1.0, 0.9, 0.9)
        self.position_x = 0.68
        self.position_y = 0.055
        self.height = 0.04
        self._format_func = func_str
        self._color_func = color_func
        self._position_x_func = float
        self._position_y_func = float
        self._height_func = float
