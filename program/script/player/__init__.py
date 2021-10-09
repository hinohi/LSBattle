#coding: utf8
from ..common import Block, color_func, high_func_num, func_str

from .gun import gun
from .hpbar import hpbar
from .gun_info import gun_info
from .window import window

_default_gun = [
    ["Hand Gun",    None,       20.0,  300, False, 0.0,  0,  1,    0.025],
    ["Big Gun",     "M26A1",   100.0, 1000, False, 0.0,  3, 27,    0.06],
    ["Machine Gun", "M134",     50.0,  100,  True, 0.01,  5,  1,    0.02],
    ["Beam Gun",    "chainsaw", 25.0,    5,  True, 0.5, 10,  0.25, 0.01]
]
class Player(Block):
    def __init__(self):
        self.collision_radius = 0.35
        self.hp = 30
        self.acceleration = 1.8
        self.resistivity = 2.0
        self.turn_acceleration = 9.0
        self.turn_resistivity = 5.0
        self.turbo = 2.5
        self.repulsion = 100.0
        self.recovery_interval = 3.0
        self.guns = []
        self.hpbar = hpbar()
        self.gun_info = gun_info()
        self.window = window()
        self._guns_obj = gun
        self._collision_radius_func = high_func_num(float, 0.0, 1.0)
        self._hp_func = high_func_num(int, 1, 10000000)
        self._acceleration_func = high_func_num(float, 0.0, 10.0)
        self._resistivity_func = high_func_num(float, 0.0, 10.0)
        self._turn_acceleration_func = high_func_num(float, -100.0, 100.0)
        self._turn_resistivity_func = high_func_num(float, 0.0, 100.0)
        self._turbo_func = high_func_num(float, 0.0, 100.0)
        self._repulsion_func = high_func_num(float, 0.0, 1000.0)
        self._recovery_interval_func = high_func_num(float, 0.0, 100000.0)

    def _check(self):
        if not self.guns:
            for data in _default_gun:
                gun = self._guns_obj()
                gun.name               = data[0]
                gun.model.name         = data[1]
                gun.range              = data[2]
                gun.reload_time        = data[3]
                gun.automatic          = data[4]
                gun.accuracy_condition = data[5]
                gun.stage_condition    = data[6]
                gun.power              = data[7]
                gun.bullet.size        = data[8]
                self.guns.append(gun)
        super(Player, self)._check()

