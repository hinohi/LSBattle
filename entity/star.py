# coding: utf8
# entity/star.py
from math import pi

from OpenGL.GL import *

from go import Matrix44, Vector4D, Lorentz
from model.polygon import Polygon
from model.flame import Flame
from program.const import IMG_DIR, c
from program.box import BOX
from program.text import drawSentence3d
from program import script

_data = [["earth.jpg", 6378000, 23.4*pi/180,            0, 30],
         ["moon.jpg",  1738000,           0,    384400000, 10],
         ["sun.gif", 695500000,           0, 149597870700, 100]]

def _high_func(sphere_radius, tilt, rescale):
    mat = Matrix44.scale(sphere_radius*rescale) * Matrix44.x_rotation(tilt)
    def func(x, y, z):
        return mat.get_rotate([x, y, z])
    return func

class Star(object):

    def __init__(self, pos, rescale, star_data):
        func = _high_func(star_data.sphere_radius, star_data.tilt, rescale)
        self.radius = star_data.sphere_radius * rescale
        self.radius2 = self.radius**2
        if star_data.texture is None:
            self.model = Polygon(IMG_DIR+star_data.model, func=func)
        else:
            self.model = Polygon(IMG_DIR+star_data.model, func=func, texture=False)
            self.model.set_texture(star_data.texture)
        self.X = pos + Vector4D(0.0, 0.0, 0.0, -orbital_radius*rescale)
        self.hp = star_data.hp
        flame_data = script.world.planet.flame
        self.flame = Flame(S=flame_data.life*self.radius, v=flame_data.speed,
                           n=flame_data.num, m=flame_data.num*2,
                           color=flame_data.num.color,
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

class Stars(object):

    def __init__(self, world, pos):
        self.world = world
        rescale = 1.0 / c
        
        self.stars = {}
        for star_data in script.world.planet.stars:
            self.stars[star_data.name] = Star()
        [Star(pos, rescale, i) for i in xrange(len(_data))]

    def draw(self, Xp, L, LL):
        for star in self.stars:
            star.draw(Xp, L, LL)

    def hit_check(self, Xp):
        for star in self.stars:
            star.hit_check(Xp, self.world)

