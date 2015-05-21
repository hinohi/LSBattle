#coding: utf8
from ..common import Block, color_func, high_func_num, func_str


class stage(Block):
    def __init__(self):
        self.enemy_num_a = 1.0
        self.enemy_num_b = 0.5
        self.enemy_num_c = 1.0
        self.types_num_a = 1.0
        self.types_num_b = 1.0
        self.types_num_c = 0.0
        self.colosseum_size_a = 0.0
        self.colosseum_size_b = 0.0
        self.colosseum_size_c = 15.0
        self._enemy_num_a_func = high_func_num(float, 0.0, 10.0)
        self._enemy_num_b_func = high_func_num(float, -3.0, 3.0)
        self._enemy_num_c_func = high_func_num(float, -100.0, 100.0)
        self._types_num_a_func = high_func_num(float, 0.0, 10.0)
        self._types_num_b_func = high_func_num(float, -3.0, 3.0)
        self._types_num_c_func = high_func_num(float, -100.0, 100.0)
        self._colosseum_size_a_func = high_func_num(float, 0.0, 10.0)
        self._colosseum_size_b_func = high_func_num(float, -3.0, 3.0)
        self._colosseum_size_c_func = high_func_num(float, -100.0, 100.0)

    def _check(self):
        e = self.enemy_num_a + self.enemy_num_c
        if e < 1.0:
            self.enemy_num_c = 1.0 - self.enemy_num_a
        self._enemy_num = lambda x:int(self.enemy_num_a*x**self.enemy_num_b + self.enemy_num_c)
        e = self.types_num_a + self.types_num_c
        if e < 1.0:
            self.types_num_c = 1.0 - self.types_num_a
        self._types_num = lambda x:int(self.types_num_a*x**self.types_num_b + self.types_num_c)
        e = self.colosseum_size_a + self.colosseum_size_c
        if e < 1.0:
            self.colosseum_size_c = 1.0 - self.colosseum_size_a
        self._colosseum_size = lambda x:int(self.colosseum_size_a*x**self.colosseum_size_b + self.colosseum_size_c)
