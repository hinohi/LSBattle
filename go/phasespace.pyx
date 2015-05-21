# coding: utf8
# cython: profile=False
# go.phasespace.pyx
from libc.math cimport sqrt

from vector4D cimport Vector4D
from matrix44 cimport Matrix44

from vector4D import Vector4D, vec4
from matrix44 import Matrix44


cdef class PhaseSpace(object):

    cdef public Vector4D X, U

    def __init__(self, X, U):
        self.X = Vector4D.from_iter(X)
        self.U = Vector4D.from_iter(U)

    def copy(self):
        return PhaseSpace(self.X, self.U)

    def get_resist(self, double b):
        return vec4.from_floats(0.0, -self.U._x*b, -self.U._y*b, -self.U._z*b)

    def transform(self, Vector4D acceleration, double ds):
        self.X._t += self.U._t * ds
        self.X._x += self.U._x * ds
        self.X._y += self.U._y * ds
        self.X._z += self.U._z * ds
        acceleration._t = 0.0
        cdef Matrix44 L = Matrix44.Lorentz(-self.U)
        cdef Vector4D accel = L.get_transform_v4(acceleration)
        cdef double r = accel.length()
        if r > 10.0:
            self.U += accel * (ds*10.0/r)
        else:
            self.U += accel * ds
        self.U._t = sqrt(1.0 + self.U._x*self.U._x + self.U._y*self.U._y + self.U._z*self.U._z)

