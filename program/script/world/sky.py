#coding: utf8
from math import pi

from ..common import Block, color_func, high_func_num, func_str


class sky(Block):
    def __init__(self):
        self.texture0 = "milkyway.jpg"
        self.texture1 = "milkyway2.jpg"
        self.rotation0 = 90.0
        self.rotation1 = 30.0
        self._texture0_func = func_str
        self._texture1_func = func_str
        self._rotation0_func = high_func_num(float, -180, 180)
        self._rotation1_func = high_func_num(float, -180, 180)
