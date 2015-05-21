# -*- coding: utf8 -*-
# pointsplite.py
from OpenGL.GL import *

from program.utils import compile_program, load_texture, DY_TEXTURE_KYU


_vshader = """
#version 120
%s float size;
uniform vec3 Xp;
uniform mat4 lorentz;
void main() {
    vec3 v = gl_Vertex.xyz - Xp;
    vec4 vertex = lorentz * vec4(v, -length(v));
    float r = -vertex.w/5;
    %svertex /= r;
    vertex.w = 1.0;
    gl_Position = gl_ModelViewProjectionMatrix * vertex;
    %s;
    vec4 color = gl_Color;
    %scolor.a = min(color.a, color.a/pow(r,2)*100);    
    gl_FrontColor = color;
}
"""
_fshader = """
#version 120
uniform sampler2D texture;
void main() {
    vec4 color = gl_Color * texture2D(texture, gl_PointCoord.xy);
    if(color.a == 0.0) discard;
    gl_FragColor = color;
}
"""

class PointSprite(object):

    def __init__(self, vertices=None, size=None, color=None, size_w=True, texture=DY_TEXTURE_KYU):
        if vertices is not None:
            n = len(vertices)
            self.vertices = (GLfloat*n)(*vertices)
            self.n = n / 3
        if size is None:
            vshader_0 = "attribute"
            size_local_geter = glGetAttribLocation
        else:
            self.size = size
            vshader_0 = "uniform"
            size_local_geter = glGetUniformLocation
        self._draw = getattr(self, "_draw_%i_%i"%(1 if vertices is None else 0,
                                                  1 if size is None else 0)
                            )

        self.color = color

        if size_w:
            vshader_1 = "gl_PointSize = size / gl_Position.w"
            a = ""
            b = "//"
        else:
            vshader_1 = "gl_PointSize = size"
            a = "//"
            b = ""
        self.program_id = compile_program(_vshader%(vshader_0, b, vshader_1, a), _fshader)
        self.size_local = size_local_geter(self.program_id, "size")
        self.vec_local  = glGetUniformLocation(self.program_id, "Xp")
        self.mat_local  = glGetUniformLocation(self.program_id, "lorentz")
        self.tex_local  = glGetUniformLocation(self.program_id, "texture")

        self.texture_id = load_texture(texture)

    def draw(self, Xp, L, vertices=None, size=None, color=None):
        glUseProgram(self.program_id)
        if color is None:
            glColor(*self.color)
        else:
            glColor(*color)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glUniform1i(self.tex_local, 0)
        glUniform3fv(self.vec_local, 1, Xp.get_lis3())
        glUniformMatrix4fv(self.mat_local, 1, GL_FALSE, L.to_glsl())
        self._draw(vertices, size)
        glUseProgram(0)

    def _draw_0_0(self, vertices, size):
        if size is None:
            glUniform1f(self.size_local, self.size)
        else:
            glUniform1f(self.size_local, size)
        glVertexPointer(3, GL_FLOAT, 0, self.vertices)
        glDrawArrays(GL_POINTS, 0, self.n)
    def _draw_0_1(self, vertices, sizes):
        glEnableVertexAttribArray(self.size_local)
        glVertexAttribPointer(self.size_local, 1, GL_FLOAT, GL_FALSE, 0, (GLfloat*self.n)(*sizes))
        glVertexPointer(3, GL_FLOAT, 0, self.vertices)
        glDrawArrays(GL_POINTS, 0, self.n)
        glDisableVertexAttribArray(self.size_local)
    def _draw_1_0(self, vertices, size):
        if size is None:
            glUniform1f(self.size_local, self.size)
        else:
            glUniform1f(self.size_local, size)
        n = len(vertices)
        glVertexPointer(3, GL_FLOAT, 0, (GLfloat*n)(*vertices))
        glDrawArrays(GL_POINTS, 0, n/3)
    def _draw_1_1(self, vertices, sizes):
        n = len(sizes)
        glEnableVertexAttribArray(self.size_local)
        glVertexAttribPointer(self.size_local, 1, GL_FLOAT, GL_FALSE, 0, (GLfloat*n)(*sizes))
        glVertexPointer(3, GL_FLOAT, 0, (GLfloat*(n*3))(*vertices))
        glDrawArrays(GL_POINTS, 0, n)
        glDisableVertexAttribArray(self.size_local)
