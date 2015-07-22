# -*- coding: utf8 -*-
# flame.py
from math import sqrt, sin, cos, pi
from random import random

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
        t = 1.0/v
        vertices = [Vector4D(t, 0.0, 1.0, 0.0)]
        for i in xrange(1, m):
            phi = pi/m*i
            if i%2: e = pi/n
            else:   e = 0.0
            for j in xrange(n):
                theta = 2.0*pi/n*j + e
                vertices.append(Vector4D(t, sin(phi)*sin(theta),
                                            cos(phi),
                                            sin(phi)*cos(theta)))
        vertices.append(Vector4D(t, 0.0, -1.0, 0.0))
        self.vertices = vertices
        self.a = self.vertices[0].squared_norm()
        # self.sizes = [BOX.Y*psize*(random() + 0.5) for i in self.vertices]
        self.sizes = [BOX.Y*psize for i in self.vertices]
        self.SS = [S * (random()*2.0 + 0.5) for i in self.vertices]

    def draw(self, X, Xp, L, LL=None, color=None):
        a = self.a
        dX = (Xp - X)*(1.0/a)
        c = dX.squared_norm()
        ac = a * c
        vertices = []
        sizes = []
        if LL is None:
            NN = self.vertices
        else:
            NN = [LL.get_transform(N) for N in self.vertices]
        for N, size, S in zip(NN, self.sizes, self.SS):
            b = N.inner_product(dX)
            s = b - sqrt(b*b - ac)
            if 0.0 < s < S:
                vertices.extend(X.get_linear_add_lis3(N, s))
                # r = 2.0*s/S
                # sizes.append(size*r*(2.0-r))
                sizes.append(size)
        if vertices:
            self.model.draw(Xp, L, vertices, sizes, color=color)
            return True
        else:
            return False
