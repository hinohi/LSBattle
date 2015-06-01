# coding: utf8
# entity.stardust.py
from random import random
from math import sin, cos, pi, sqrt

from model.pointsprite import PointSprite
from program.box import BOX
from program.utils import DY_TEXTURE_KYU
from program import script


class StarDust(object):

    def __init__(self, scale):
        n = script.world.stardust.num
        R = script.world.stardust.range * scale
        vertices = []
        for i in xrange(n):
            r = R * random()**(1./3)
            z = 1.0 - random()*2.0
            p = 2.0*pi*random()
            zz = sqrt(1.0-z*z)
            vertices.extend([r*zz*cos(p),
                             r*zz*sin(p),
                             r*z])
        self.model = PointSprite(vertices=vertices,
                                 size=script.world.stardust.size*BOX.Y,
                                 color=script.world.stardust.color,
                                 texture=DY_TEXTURE_KYU)

    def draw(self, Xp, L):
        self.model.draw(Xp, L)
