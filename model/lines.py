# -*- coding: utf8 -*-
# lines.py
import os

from OpenGL.GL import *

from program.utils import compile_program


class Lines(object):
    def load_program(self):
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
            float factor = max(1.0/5.0,
                                   min(1.0, 10.0/(gl_Position.w*gl_Position.w))
                                   );
            vec4 color = gl_Color;
            color.a *= factor;
            gl_FrontColor = color;
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

    def __init__(self, color):
        self.color = color
        self.load_program()

    def draw(self, Xp, L, vertices_1, vertices_2, color=None):
        glUseProgram(self.program_id)
        if color is None:
            glColor(*self.color)
        else:
            glColor(*color)
        glUniform3fv(self.vec_local, 1, Xp.get_lis3())
        glUniformMatrix4fv(self.mat_local, 1, GL_FALSE, L.to_glsl())
        glBegin(GL_LINES)
        for i in range(len(vertices_1)/3):
            glVertex(vertices_1[i*3], vertices_1[i*3+1], vertices_1[i*3+2])
            glVertex(vertices_2[i*3], vertices_2[i*3+1], vertices_2[i*3+2])
        glEnd()
        # vertices = vertices_1 + vertices_2
        # a = len(vertices_1) / 3
        # indices = []
        # for i in xrange(a):
        #     indices += [i, i+a]
        # n = len(vertices)
        # glVertexPointer(3, GL_FLOAT, 0, (GLfloat*n)(*vertices))
        # glDrawElements(GL_LINES, n, GL_UNSIGNED_BYTE, (GLint*len(indices))(*indices))
        glUseProgram(0)
