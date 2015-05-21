#coding: utf8
from ..common import Block, color_func, high_func_num, func_str


class bullet(Block):
    def __init__(self):
        self.color = (0.8, 0.8, 0.2, 0.9)
        self.size = 0.02
        self._color_func = color_func
        self._size_func = high_func_num(float, 0.001, 0.1)

class model(Block):
    def __init__(self):
        self.name = None
        self.color = (1.0, 1.0, 1.0, 1.0)
        self.size = 0.4
        self.rotation_speed = 0.5
        self._name_func = func_str
        self._color_func = color_func
        self._size_func = high_func_num(float, 0.01, 10.0)
        self._rotation_speed_func = float

class gun(Block):
    def __init__(self):
        self.name = ""
        self.speed = 1.0
        self.range = 20.0
        self.reload_time = 200
        self.automatic = False
        self.power = 1.0
        self.div = []
        self.accuracy_condition = 0.1
        self.stage_condition = 3
        self.shoot_position = -0.05
        self.bullet = bullet()
        self.model = model()
        self._name_func = str
        self._speed_func = high_func_num(float, 0.7, 1.0)
        self._range_func = high_func_num(float, 2.0, 1000.0)
        self._reload_time_func = high_func_num(int, 1, 100000)
        self._power_func = high_func_num(float, 0.01, 1000.0)
        self._accuracy_condition_func = high_func_num(float, 0.0, 1.0)
        self._stage_condition_func = high_func_num(int, -1, 1000)
        self._shoot_position_func = high_func_num(float, -1.0, 1.0)

    def _check(self):
        if self.model.name is None:
            self.model.name = self.name
        if isinstance(self.div, int):
            self.div = [self.div]
