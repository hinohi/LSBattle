#coding: utf8
from math import pi

from ..common import Block, color_func, high_func_num, func_str


class sky(Block):
    def __init__(self):
        self.texture0 = "milkyway.jpg"
        self.texture1 = "milkyway2.jpg"
        self.rotation = pi/3.0
        self._texture0_func = func_str
        self._texture1_func = func_str
        self._rotation_func = high_func_num(float, 0.0, 2.0*pi)
