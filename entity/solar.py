# coding: utf8
# entity/solar.py
from math import pi, sin, cos

from OpenGL.GL import *

from go import Matrix44, Vector4D, Lorentz, calc_repulsion
from model.polygon import Polygon
from model.flame import Flame
from program.const import IMG_DIR, c
from program.box import BOX
from program.text import drawSentence3d
from program import script


def _high_func(sphere_radius, tilt):
    mat = Matrix44.scale(sphere_radius) * Matrix44.z_rotation(tilt*pi/180) * Matrix44.y_rotation(pi/2)
    def func(x, y, z):
        return mat.get_rotate([x, y, z])
    return func

class Star(object):

    def __init__(self, X, star_data):
        func = _high_func(star_data.sphere_radius, star_data.tilt)
        self.radius = star_data.sphere_radius
        self.radius2 = self.radius**2
        if star_data.texture is None:
            self.model = Polygon(IMG_DIR+star_data.model, func=func)
        else:
            self.model = Polygon(IMG_DIR+star_data.model, func=func, texture=False)
            self.model.set_texture(star_data.texture)
        self.X = X.copy()
        self.hp = star_data.hp
        flame_data = script.world.solar.flame
        self.flame = Flame(S=flame_data.life*self.radius, v=flame_data.speed,
                           n=flame_data.num, m=flame_data.num*2,
                           color=flame_data.color,
                           psize=flame_data.size*self.radius)
        self.alive = True
        self.X_dead = None

    def draw(self, Xp, L, LL):
        if self.hp > 0:
            dX = self.X - Xp
            dX.t = -dX.length()
            dx = L.get_transform(dX)
            r = -dx.t
            if r > 0.5*BOX.far_clip:
                s = 0.05 * BOX.far_clip / r
                X = Xp + dX*s
                self.model.draw(Xp, L, LL, X=X, R=Matrix44.scale(s))
            else:
                self.model.draw(Xp, L, LL, X=self.X)
        else:
            if not self.flame.draw(self.X_dead, Xp, L):
                self.alive = False

    def hit_check(self, Xp, world):
        if self.hp > 0:
            t = Xp.t - Xp.distance_to(self.X)
            self.X.t = t
            X1 = self.X + Vector4D(0.02, 0, 0, 0)
            self.hp -= world.player.bullet_hit_check(X1, self.X, self.radius2)
            self.hp -= world.enemies.bullets.hit_check(X1, self.X, self.radius2)
            if self.hp <= 0:
                self.X_dead = self.X.copy()

class SolarSystem(object):
    star_datum = None
    def __init__(self, world, Xp, scale):
        self.world = world
        self.stars = {}
        self.read_data()
        if not self.star_datum:
            return
        self.calc_star_pos(Xp, scale)
        for name in self.star_pos:
            star = Star(self.star_pos[name], self.star_datum[name])
            self.stars[name] = star

    @classmethod
    def read_data(cls):
        if cls.star_datum is not None:
            return
        rescale = 1.0 / c
        cls.star_datum = {}
        for star_data in script.world.solar.stars:
            star_data.sphere_radius *= rescale
            star_data.orbital_radius *= rescale
            star_data.name = star_data.name.lower()
            pname = star_data.primary_star
            star_data.primary_star = pname.lower() if pname is not None else None
            cls.star_datum[star_data.name] = star_data

    def calc_pos(self, r, phi):
        cos_p = cos(phi * pi / 180)
        sin_p = sin(phi * pi / 180)
        return Vector4D(0.0, sin_p*r, 0.0, cos_p*r)
    def calc_star_pos(self, Xp, scale):
        self.star_pos = {}
        center = script.world.solar.center.lower()
        if center not in self.star_datum:
            if "sun" not in self.star_datum:
                return
            else:
                center = "sun"
        offset = Vector4D(0.0,
                          script.world.solar.dx,
                          script.world.solar.dy,
                          script.world.solar.dz) * scale
        self.star_pos[center] = Xp + offset
        loop_count = 0
        flg = True
        while loop_count < 3 and flg:
            loop_count += 1
            flg = False
            for name in self.star_datum:
                if name in self.star_pos:
                    continue
                star_data = self.star_datum[name]
                if star_data.primary_star is not None:
                    pname = self.star_datum[star_data.primary_star].name
                    if pname in self.star_pos:
                        pos = self.calc_pos(star_data.orbital_radius,
                                            star_data.orbital_phi)
                        self.star_pos[name] = self.star_pos[pname] + pos
                        continue
                for sname in self.star_pos:
                    sdata = self.star_datum[sname]
                    if name == sdata.primary_star:
                        pos = self.calc_pos(sdata.orbital_radius,
                                            sdata.orbital_phi)
                        self.star_pos[name] = self.star_pos[sname] - pos
                        break
                else:
                    flg = True

    def __getitem__(self, key):
        return self.stars[key]

    def __iter__(self):
        for name in self.stars:
            yield self.stars[name]

    def draw(self, Xp, L, LL):
        for star in self.stars.itervalues():
            star.draw(Xp, L, LL)

    def hit_check(self, Xp):
        for star in self.stars.itervalues():
            if star.hp > 0:
                star.hit_check(Xp, self.world)

    def calc_repulsion(self, Xp, acceleration, collision_radius, repulsion):
        U = Vector4D(1.0, 0.0, 0.0, 0.0)
        for star in self.stars.itervalues():
            if star.hp > 0:
                star.X.t = Xp.t - Xp.distance_to(star.X)
                calc_repulsion(Xp, star.X, U,
                               collision_radius + star.radius,
                               repulsion,
                               acceleration)


