#coding: utf8
from ..common import Block, color_func, high_func_num

from .character import character
from .bullet import bullet
from .flame import flame
from .timer import timer
from .hpbar import hpbar


_default = [
    ["dorake",     0,   2, 2.0,  1.2, 0.7,      1  , 2.0],
    ["reimu",      6,   1, 1.5,  3.0, 0.75,     0.9, 4.0],
    ["marisa",     3,   1, 1.5,  1.0, 0.75,     0.9, 2.0],
    ["kuma",       1,  10, 2.5,  0.5, 0.85,     2.2, 2.0],
    ["buta",       2,   8, 2.0,  0.5, 0.9,      1.5, 2.0],
    ["medaka",     0,   5, 1.5,  2.5, 0.9,      0.9, 2.0],
    ["Manticore",  3,  15, 1.75, 1.8, 0.95,     2.4, 2.0],
    ["allosaurus", 2,   5, 0.5,  2.8, 0.85,     3  , 2.0],
    ["Griffin",    1,   5, 1.0,  8.0, 0.999,    2.4, 2.0],
    ["gargoyle",   4,  40, 1.0,  3.0, 0.99,     2  , 2.0],
    ["Medusa",     5,   5, 0.01, 1.0, 0.9,      3  , 2.0],
    ["minotaurus", 2,  30, 1.0,  4.0, 0.99,     4  , 2.0],
    ["Golem",      5, 100, 1.5,  1.0, 0.99,     6  , 2.0],
    ["Phoenix",    4,  30, 1.0,  5.0, 0.99,     4  , 2.0],
    ["wyvern",     2,  30, 1.0,  6.0, 0.99,     6  , 2.0],
    ["bos",        3, 200, 0.05, 3.0, 0.99999,  10 , 2.0]
]
"""
[name, think type, HP, shooting interval, acceleration, bullet velocity, size, resistivity]
"""
class Enemy(Block):
    def __init__(self):
        self.character = []
        self._character_obj = character
        self.bullet = bullet()
        self.flame = flame()
        self.timer = timer()
        self.hpbar = hpbar()
        self.repulsion = 100.0
        self._repulsion_func = high_func_num(float, 0.0, 1000.0)

    def _check(self):
        for c in self.character:
            c._check()
        if not self.character:
            for line in _default:
                name, tt, hp, inter, accel, b, size, resistivity = line
                c = self._character_obj()
                c.name = name
                c.think_type = c._think_type_func(tt)
                c.hp = c._hp_func(hp)
                c.shoot_interval = c._shoot_interval_func(inter)
                c.acceleration = c._acceleration_func(accel)*2.0
                c.bullet_speed = c._bullet_speed_func(b)
                c.size = c._size_func(size)
                c.resistivity = resistivity
                c._check()
                self.character.append(c)
