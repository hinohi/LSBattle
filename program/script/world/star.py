#coding: utf8
from math import pi

from ..common import Block, color_func, high_func_num, func_str


class star(Block):
    def __init__(self):
        self.name = "earth"
        self.texture = "earth.jpg"
        self.model = "star"
        self.sphere_radius = 6378000
        self.orbital_radius = 6378000
        self.orbital_phi = 0.0
        self.tilt = 23.4
        self.hp = 1000
        self.primary_star = "sun"
        
class flame(Block):
    def __init__(self):
        self.life = 50.0
        self.speed = 0.1
        self.size = 0.2
        self.color = [1.0, 0.8, 0.8, 0.8]
        self.num = 10
        self._life_func  = high_func_num(float, 0.01, 100.0)
        self._speed_func = high_func_num(float, 0.1, 0.999)
        self._size_func  = high_func_num(float, 0.001, 1.0)
        self._color_func = color_func
        self._num_func = high_func_num(int, 4, 20)

class planet(Block):
    def __init__(self):
        self.stars = []
        self._stars_obj = star
        self.flame = flame()
        self.center = "earth"
        self.dx =  0.0
        self.dy = -0.5
        self.dz = -3.0
