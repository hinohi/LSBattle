#coding: utf8
from ..common import Block, high_func_num, func_str, color_func

_default = [
    ["Earth", "earth.jpg", "star",   6378000, 149597870700,  0.0, 23.4, "Sun", 1000],
    ["Sun",   "sun.gif",   "star", 695500000,            0,  0.0,  0.0,  None, 1000],
    ["Moon",  "moon.jpg",  "star",   1738000,    384400000, 180.,  0.0, "Earth", 1000],
]

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

        self._name_func = func_str
        self._texture_func = func_str
        self._model_func = func_str
        self._sphere_radius_func = high_func_num(float, 0.0, 10.**50)
        self._orbital_radius_func = high_func_num(float, 0.0, 10.**50)
        self._orbital_phi_func = high_func_num(float, -180, 180)
        self._tilt_func = high_func_num(float, -180, 180)
        self._hp_func = high_func_num(int, 1, 10**10)
        self._primary_star_func = func_str

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

class solar(Block):
    def __init__(self):
        self.stars = []
        self._stars_obj = star
        self.flame = flame()
        self.center = "earth"
        self.dx =  0.0
        self.dy = -0.5
        self.dz = -3.0
        self._center_func = func_str
        self._dx_func = float
        self._dy_func = float
        self._dz_func = float

    def _check(self):
        if not self.stars:
            for data in _default:
                s = star()
                s.name = data[0]
                s.texture = data[1]
                s.model = data[2]
                s.sphere_radius = data[3]
                s.orbital_radius = data[4]
                s.orbital_phi = data[5]
                s.tilt = data[6]
                s.primary_star = data[7]
                s.hp = data[8]
                self.stars.append(s)
        super(solar, self)._check()
