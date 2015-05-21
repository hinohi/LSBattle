#coding: utf8
from math import pi

from ..common import Block, color_func, high_func_num, func_str


class sky(Block):
    def __init__(self):
        self.model = "galaxy"
        self.texture = None
        self.rotation = pi/3.0
        self._model_func = str
        self._texture_func = func_str
        self._rotation_func = high_func_num(float, 0.0, 2.0*pi)
