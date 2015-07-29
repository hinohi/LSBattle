#coding: utf8
#vector3.pxd

cdef class Vector3(object):
    cdef double _x, _y, _z
    cpdef Vector3 from_floats(self, double x, double y, double z)
    cpdef copy(self)
