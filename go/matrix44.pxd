#coding: utf8
#matrix44.pxd

cdef class Matrix44(object):
    cdef double m00, m01, m02, m03, m10, m11, m12, m13, m20, m21, m22, m23, m30, m31, m32, m33
