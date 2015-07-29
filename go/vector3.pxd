# coding: utf8
# go/vector3.pxd

cdef class Vector3(object):
    cdef double _x, _y, _z
    cpdef copy(self)

cdef Vector3 vec3_from_floats(double x, double y, double z)
