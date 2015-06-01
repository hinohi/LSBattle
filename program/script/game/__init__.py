#coding: utf8
from ..common import Block, color_func, high_func_num, func_str

from .stage import stage
from .score import score


class Game(Block):
    def __init__(self):
        self.scale = 0.4
        self.stage_num = 20
        self.continue_num = 3
        self.cheat = False
        self.output_script = True
        self.stage = stage()
        self.score = score()
        self._scale_func = high_func_num(float, 0.0001, 10.0)
        self._stage_num_func = high_func_num(int, 1, 10000)
        self._continue_num_func = high_func_num(int, 0, 100)

    def _check(self):
        self.stage._check()
