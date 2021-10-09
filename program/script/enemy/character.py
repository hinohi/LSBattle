#coding: utf8
from ..common import Block, color_func, high_func_num


class think(Block):
    def __init__(self):
        self.zgzg_interval = 10.0
        self.near_n = -1.0
        self.near_p = 0.0
        self.far_n  = 1.0
        self.far_p  = 0.0
        self.distance0 = 4.0
        self.distance1 = 10.0
        self._zgzg_interval_func  = float
        self._near_n_func = self._near_p_func = float
        self._far_n_func = self._far_p_func = float
        self._distance0_func = float
        self._distance1_func = float

class character(Block):
    def __init__(self):
        self.name = "default"
        self.color = (1.0, 1.0, 1.0, 1.0)
        self.size = 1.0
        self.collision_radius = 0.5
        self.collision_radius_by_friend = self.collision_radius * 0.5
        self.hp = 5
        self.shoot_interval = 5.0
        self.shoot_div = []
        self.shoot_div_phi = 0.02
        self.acceleration = 2.0
        self.resistivity = 2.0
        self.bullet_speed = 0.9
        self.bullet_range = 2.0
        self.think = think()
        self._name_func = str
        self._color_func = color_func
        self._size_func = high_func_num(float, 0.1, 1000.0)
        self._collision_radius_func = high_func_num(float, 0.0, 1.0)
        self._collision_radius_by_friend_func = high_func_num(float, 0.0, 1.0)
        self._hp_func = high_func_num(int, 1, 10000000)
        self._shoot_interval_func = float
        self._shoot_div_phi_func = high_func_num(float, 0.0, 1.0)
        self._acceleration_func = high_func_num(float, 0.0, 10.0)
        self._resistivity_func = high_func_num(float, 0.0, 10.0)
        self._bullet_speed_func = high_func_num(float, 0.5, 0.99999)
        self._bullet_range_func = high_func_num(float, 1.0, 1000.0)

    def _check(self):
        if isinstance(self.shoot_div, int):
            self.shoot_div = [self.shoot_div]
        super(character, self)._check()
