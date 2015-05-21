#coding: utf8
from ..common import Block, color_func, high_func_num, func_str


class hpbar(Block):
    def __init__(self):
        self.position_x = 0.68
        self.position_y = 0.05
        self.length_x = 0.3
        self.length_y = 0.05
        self.color = (0.0, 0.0, 0.9, 0.5)
        self.back_color = (0.1, 0.6, 1.0, 0.3)
        self.blood_time = 1.0
        self.blood_color = (1.0, 0.0, 0.0, 1.0)
        self._position_x_func = float
        self._position_y_func = float
        self._length_x_func = float
        self._length_y_func = float
        self._color_func = color_func
        self._back_color_func = color_func
        self._blood_time_func = float
        self._blood_color_func = color_func
