# coding: utf8
# go/vector4D.pxd


cdef class Vector4D(object):
    cdef double _t, _x, _y, _z
    cpdef Vector4D copy(self)
    cpdef double squared_norm_to(self, Vector4D othr)
    cpdef double inner_product(self, Vector4D othr)
    cpdef double squared_norm(self)
    cpdef double dot(self, Vector4D othr)
    cpdef double length(self)
    cpdef double squared_length(self)
    cpdef int normalize(self, double length=*)
    cpdef Vector4D get_linear_add(self, Vector4D N, double s)
    cpdef Vector4D get_div_point(self, Vector4D othr, double s)

cdef Vector4D vec4_from_floats(double t, double x, double y, double z)
