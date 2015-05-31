#coding: utf8
from math import pi

from ..common import Block, color_func, high_func_num, func_str


class sky(Block):
    def __init__(self):
        self.texture = "milkyway.jpg"
        self.rotation = pi/3.0
        self._texture_func = func_str
        self._rotation_func = high_func_num(float, 0.0, 2.0*pi)
