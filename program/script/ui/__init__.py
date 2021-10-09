# coding: utf8
from ..common import Block, color_func, high_func_num

from .backimage import backimage
from .font import font


class UI(Block):
    def __init__(self):
        self.backimage = backimage()
        self.font = font()
        self.near_clip = 0.1
        self.far_clip  = 2000.0
        self._near_clip_func = high_func_num(float, 1e-5, 1e2)
        self._far_clip_func  = high_func_num(float, 1.0, 1e10)
