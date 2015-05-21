# coding: utf8
# world.py
from math import pi
from random import random, randint

from OpenGL.GL import *

from go import Vector3, Vector4D, Matrix44, Lorentz
from program.const import *
from program.utils import compile_program, load_texture, DY_TEXTURE_KYU


class WireFrame(object):

    def __init__(self, L, N, color=(1.0,1.0,1.0,0.5)):
        self.L = L
        self.color = color
        vertices = []
        indices = []
        n = 2*N + 1
        for z in xrange(-N, N+1):
            zz = z + N
            for y in xrange(-N, N+1):
                yy = y + N
                for x in xrange(-N, N+1):
                    xx = x + N
                    if x < N:
                        indices.append(xx +     yy*n + zz*n*n)
                        indices.append((xx+1) + yy*n + zz*n*n)
                    if y < N:
                        indices.append(xx + yy*n +     zz*n*n)
                        indices.append(xx + (yy+1)*n + zz*n*n)
                    if z < N:
                        indices.append(xx + yy*n + zz*n*n)
                        indices.append(xx + yy*n + (zz+1)*n*n)
                    vertices.extend([(x+0.5)*self.L/N,
                                     (y+0.5)*self.L/N,
                                     (z+0.5)*self.L/N])
        self.vertices = (GLfloat*len(vertices))(*vertices)
        self.indices = (GLint*len(indices))(*indices)
        self.n = len(indices)

        self.make_program()

    def make_program(self):
        self.program_id = compile_program(
            """
            #version 120
            uniform vec3 Xp;
            uniform mat4 lorentz;
            void main() {
                vec3 v = gl_Vertex.xyz - Xp;
                vec4 vertex = lorentz * vec4(v, -length(v));
                vertex.w = 1.0;
                gl_Position = gl_ModelViewProjectionMatrix * vertex;
                vec4 color = gl_Color;
                color.a = max(color.a/50,min(color.a, color.a/pow(gl_Position.w,2)*10));
                gl_FrontColor = color;
            }
            """,
            """
            #version 120
            void main() {
                gl_FragColor = gl_Color;
            }
            """)
        self.vec_local  = glGetUniformLocation(self.program_id, "Xp")
        self.mat_local  = glGetUniformLocation(self.program_id, "lorentz")
    
    def draw(self, Xp, L, color=None):
        glUseProgram(self.program_id)
        if color is None:
            glColor(*self.color)
        else:
            glColor(*color)
        glUniform3fv(self.vec_local, 1, Xp.get_lis3())
        glUniformMatrix4fv(self.mat_local, 1, GL_FALSE, L.to_glsl())
        glVertexPointer(3, GL_FLOAT, 0, self.vertices)
        glDrawElements(GL_LINES, self.n, GL_UNSIGNED_INT, self.indices)
        glUseProgram(0)



