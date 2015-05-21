# -*- coding: utf8 -*-
# flame.py
from math import sqrt, sin, cos, pi

from go import Vector4D, Lorentz
from model.pointsprite import PointSprite
from program.box import BOX
from program.utils import DY_TEXTURE_KYU


class Flame(object):

    def __init__(self, S=0.5, v=0.6, n=5, m=10, color=(1.0, 0.9, 0.99, 0.6), psize=0.02):
        """
        S: float, lifetime of each particle consisting of the flame.
        v: float, velocity of each particle consisting of the flame.
        n: int, number of particles in zenith angle direction.
        m: int, number of particles in azimuthal angle direction.
        psize: float, size of each particle consisting of the flame, relative to screen size.
        """
        self.model = PointSprite(color=color, texture=DY_TEXTURE_KYU)
        self.S = S * 1.0
        self.size = BOX.Y*psize
        t = 1.0/v
        vertex = [Vector4D(t, 0.0, 1.0, 0.0)]
        for i in xrange(1, m):
            phi = pi/m*i
            if i%2: e = pi/n
            else:   e = 0.0
            for j in xrange(n):
                theta = 2.0*pi/n*j + e
                vertex.append(Vector4D(t, sin(phi)*sin(theta),
                                          cos(phi),
                                          sin(phi)*cos(theta)))
        vertex.append(Vector4D(t, 0.0, -1.0, 0.0))
        self.vertex = vertex
        self.a = self.vertex[0].squared_norm()

    def draw(self, X, Xp, L, LL=None, color=None):
        a = self.a
        dX = (Xp - X)*(1.0/a)
        c = dX.squared_norm()
        ac = a * c
        vertices = []
        sizes = []
        if LL is None:
            NN = self.vertex
        else:
            NN = [LL.get_transform_v4(N) for N in self.vertex]
        for N in NN:
            b = N.inner_product(dX)
            s = b - sqrt(b*b - ac)
            if 0.0 < s < self.S:
                vertices.extend(X.get_linear_add_lis3(N, s))
                r = 2.0*s/self.S
                sizes.append(self.size*r*(2.0-r))
        if vertices:
            self.model.draw(Xp, L, vertices, sizes, color=color)
            return True
        else:
            return False
