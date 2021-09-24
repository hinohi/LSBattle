#coding: utf8
from ..common import Block, color_func, high_func_num, func_str


class score(Block):
    def __init__(self):
        self.stage_power = 2.0
        self.clear_time = 10000.0
        self.clear_time_power = -1.0
        self.clear_time_geta = 10.0
        self.hp = 1000.0
        self.hp_power = 1.0
        self.accuracy = 5000.0
        self.accuracy_power = 1.0

        self.hit = 10
        self.hit_by_friend = 30
        self.break_enemy = 100

        self._stage_power_func = high_func_num(float, 0.0, 3.0)
        self._clear_time_func = high_func_num(float, 0.0, 10.0**6)
        self._clear_time_power_func = high_func_num(float, -2.0, 2.0)
        self._clear_time_geta_func = high_func_num(float, 0.01, 10.0**5)
        self._hp_func = high_func_num(float, 0.0, 10.0**6)
        self._hp_power_func = high_func_num(float, -2.0, 2.0)
        self._accuracy_func = high_func_num(float, 0.0, 10.0**6)
        self._accuracy_power_func = high_func_num(float, -2.0, 2.0)
        self._hit_func = high_func_num(int, -1000, 1000)
        self._hit_by_friend_func = high_func_num(int, -1000, 1000)
        self._break_enemy_func = high_func_num(int, -1000, 1000)
