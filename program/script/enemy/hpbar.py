#coding: utf8
from ..common import Block, color_func, high_func_num


class hpbar(Block):
    def __init__(self):
        self.visible = True
        self.position = 0.6
        self.width = 0.05
        self.length = 1.0
        self.length_parhp = 0.1
        self.back_color = (1.0, 0.1, 0.1, 0.2)
        self.bar_color = (1.0, 0.392, 1.0, 0.6)
        self._position_func = high_func_num(float, -1.0, 1.0)
        self._width_func = high_func_num(float, 0.01, 0.2)
        self._length_func = high_func_num(float, 0.01, 100.0)
        self._length_parhp_func = high_func_num(float, 0.01, 1.0, True)
        self._back_color_func = color_func
        self._bar_color_func = color_func
