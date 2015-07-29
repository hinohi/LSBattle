# coding: utf8

cdef class Vector4D(object):
    cdef double _t, _x, _y, _z
    cpdef Vector4D from_floats(self, double t, double x, double y, double z)
    cpdef double squared_norm_to(self, Vector4D othr)
    cpdef double inner_product(self, Vector4D othr)
    cpdef double dot(self, Vector4D othr)
    cpdef double length(self)
    cpdef double squared_length(self)

