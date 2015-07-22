# coding: utf8
# cython: profile=False
# go.worldline.pyx
cimport cython
from libc.math cimport sqrt

from vector4D cimport Vector4D


cdef class WorldLine(object):

    cdef int i, n, last
    cdef double s
    cdef list line, state

    def __init__(self, P, Q=None):
        self.line  = [P.X.copy()]
        self.state = [Q]
        self.i = 0
        self.n = 1
        self.last = -1
        self.s =  0.0

    def add(self, P, Q=None):
        self.line.append(P.X.copy())
        self.state.append(Q)
        self.n += 1

    cdef int search_position_on_PLC(self, Vector4D Xp):
        cdef Vector4D X = self.line[self.i]
        cdef double Xpt = Xp._t
        cdef int i

        if Xpt < X._t:
            for i in xrange(self.i-1, -1, -1):
                X = self.line[i]
                if Xpt > X._t and X.squared_norm_to(Xp) < 0.0:
                    self.i = i
                    if self.last > self.i:
                        self.last = self.i
                    return i+1
        elif X.squared_norm_to(Xp) <= 0.0:
            for i in xrange(self.i+1, self.n):
                X = self.line[i]
                if X.squared_norm_to(Xp) > 0.0:
                    self.i = i-1
                    if self.last > self.i:
                        self.last = self.i
                    return i
        else:
            for i in xrange(self.i-1, -1, -1):
                X = self.line[i]
                if X.squared_norm_to(Xp) < 0.0:
                    self.i = i
                    if self.last > self.i:
                        self.last = self.i
                    return i+1
        self.last = 0
        return -1

    @cython.cdivision(True)
    def get_X_FP(self, Vector4D Xp, double w=0.5):
        cdef int i = self.search_position_on_PLC(Xp)
        if i == -1:
            return None
        cdef Vector4D X0 = self.line[i-1]
        cdef Vector4D X1 = self.line[i]
        cdef Vector4D dX = X0 - X1
        cdef Vector4D dY = X0 - Xp
        cdef double a = dX.squared_norm()
        cdef double b = dX.inner_product(dY)
        cdef double s, c
        if w == 0.5:
            s = b / a
        else:
            c = dY.squared_norm()
            s = (b + (1.0 - 2.0*w)*sqrt(b*b - a*c)) / a
        return X0.get_div_point(X1, s)

    @cython.cdivision(True)
    def get_XU_on_PLC(self, Vector4D Xp):
        cdef int i = self.search_position_on_PLC(Xp)
        if i == -1:
            return None, None
        cdef Vector4D X0 = self.line[i-1]
        cdef Vector4D X1 = self.line[i]
        cdef Vector4D dX = X1 - X0
        cdef Vector4D dY = Xp - X0
        cdef double a = dX.squared_norm()
        cdef double b = dX.inner_product(dY)
        cdef double c = dY.squared_norm()
        cdef double s = (b + sqrt(b*b - a*c))/a
        self.s = s
        dX /= sqrt(-a)
        return X0.get_div_point(X1, s), dX

    def get_State_on_PLC(self, Vector4D Xp):
        cdef int i = self.search_position_on_PLC(Xp)
        q0 = self.state[i-1]
        q1 = self.state[i]
        return q0, q1, self.s

    def get_last(self):
        return self.line[-1]

