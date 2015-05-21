# coding: utf8
# entity/sky.py
from math import pi

from OpenGL.GL import *

from go import Matrix44
from model.polygon import MqoGpoPolygon
from program.box import BOX
from program.utils import load_texture, compile_program
from program.const import IMG_DIR, VIEW_ANGLE
from program import script


class Sky_old(MqoGpoPolygon):

    def load_program(self):
        self.program = compile_program(
        """
        #version 120
        uniform mat4 lorentz;
        void main() {
            vec4 vertex = lorentz * vec4(gl_Vertex.xyz, -length(gl_Vertex.xyz));
            vertex.w = 1.0;
            gl_Position = gl_ModelViewProjectionMatrix * vertex;
            gl_TexCoord[0] = gl_MultiTexCoord0;
        }
        """,
        """
        #version 120
        uniform sampler2D texture;
        void main() {
            gl_FragColor = texture2D(texture, gl_TexCoord[0].xy);
        }
        """)
        self.mat_local = glGetUniformLocation(self.program, "lorentz")
        self.tex_local = glGetUniformLocation(self.program, "texture")

    def __init__(self):
        self.load_program()
        m = Matrix44.z_rotation(script.world.sky.rotation)
        def func(x, y, z):
            return m.get_rotate([x, y, z])
        file_path = self.make_gpo(IMG_DIR+script.world.sky.model)
        if script.world.sky.texture is None:
            self.load_gpo(file_path, func=func)
        else:
            self.load_gpo(file_path, func=func, texture=False)
            self.set_texture(script.world.sky.texture)
        self.material, self.n, self.indices = self.objects[0]

    def draw(self, L):
        glUseProgram(self.program)
        glVertexPointer(3, GL_FLOAT, 0, self.vertices)
        glTexCoordPointer(2, GL_FLOAT, 0, self.texcoords)
        glBindTexture(GL_TEXTURE_2D, self.material.texture_id)
        glUniformMatrix4fv(self.mat_local, 1, GL_FALSE, L.to_glsl())
        glUniform1i(self.tex_local, 0)
        glDrawElements(GL_TRIANGLES, self.n, GL_UNSIGNED_INT, self.indices)
        glUseProgram(0)

class Sky2(MqoGpoPolygon):

    def load_program(self):
        self.program = compile_program(
        """
        #version 120
        
        varing vec3 vertex;
        void main() {
            vec4 vertex = lorentz * vec4(gl_Vertex.xyz, -length(gl_Vertex.xyz));
            vertex.w = 1.0;
            gl_Position = gl_ModelViewProjectionMatrix * vertex;
            gl_TexCoord[0] = gl_MultiTexCoord0;
        }
        """,
        """
        #version 120
        uniform sampler2D texture;
        uniform mat4 lorentz;
        varing vex3 vertex;
        void main() {
            gl_FragColor = texture2D(texture, gl_TexCoord[0].xy);
        }
        """)
        self.mat_local = glGetUniformLocation(self.program, "lorentz")
        self.tex_local = glGetUniformLocation(self.program, "texture")

    def __init__(self):
        self.load_program()
        m = Matrix44.z_rotation(script.world.sky.rotation)
        def func(x, y, z):
            return m.get_rotate([x, y, z])
        file_path = self.make_gpo(IMG_DIR+script.world.sky.model)
        if script.world.sky.texture is None:
            self.load_gpo(file_path, func=func)
        else:
            self.load_gpo(file_path, func=func, texture=False)
            self.set_texture(script.world.sky.texture)
        self.material, self.n, self.indices = self.objects[0]

    def draw(self, L):
        glUseProgram(self.program)
        glVertexPointer(3, GL_FLOAT, 0, self.vertices)
        glTexCoordPointer(2, GL_FLOAT, 0, self.texcoords)
        glBindTexture(GL_TEXTURE_2D, self.material.texture_id)
        glUniformMatrix4fv(self.mat_local, 1, GL_FALSE, L.to_glsl())
        glUniform1i(self.tex_local, 0)
        glDrawElements(GL_TRIANGLES, self.n, GL_UNSIGNED_INT, self.indices)
        glUseProgram(0)

class Sky(object):
    
    program = None
    mat_local = None
    tex_local = None
    
    def __init__(self, n=20, m=10):
        self.ver = []
        alpha = VIEW_ANGLE*pi/360
        a = alpha/n
        b = alpha*BOX.X/BOX.Y/m
        for i in xrange(-n, n+1):
            v = Matrix44.x_rotation(a*i).get_rotate((0, 0, -1))
            for k in xrange(-m, m+1):
                vv = Matrix44.y_rotation(b*k).get_rotate(v)
                self.ver.append(vv)
        self.faces = []
        a = 2*n + 1
        b = 2*m + 1
        for i in xrange(a-1):
            for k in xrange(b-1):
                self.faces.append((k   + b*i,
                                   k   + b*(i+1),
                                   k+1 + b*(i+1),
                                   k+1 + b*i))
        vertex = []
        for f in self.faces:
            for i in f:
                vertex.extend(self.ver[i])
        self.n = len(vertex)/3
        self.vertex = (GLfloat*len(vertex))(*vertex)
        self.GLtex = GLfloat*(len(self.faces)*8)
        
        self.m = Matrix44.z_rotation(pi*63/180)
        
        self.texture_id = load_texture(IMG_DIR+"milkyway.jpg")

        if self.program is None or not glIsProgram(self.program):
            self.init_program()

    @classmethod
    def init_program(cls):
        cls.program = compile_program(
        """
        #version 120
        varying vec3 pos;
        void main() {
            pos = vec3(gl_Vertex);
            gl_Position = gl_ProjectionMatrix * gl_Vertex;
        }
        """,
        """
        #version 120
        varying vec3 pos;
        uniform mat4 lorentz;
        uniform sampler2D texture;
        void main() {
            vec4 v = lorentz * vec4(pos, -length(pos));
            vec2 tex;
            //tex.s = atan(v.z, v.x) * 0.15915494309189533;
            //tex.t = atan(length(v.xz), v.y) * 0.31830988618379067;
            tex.s = atan(v.y, v.x) * 0.15915494309189533;
            tex.t = 1.0 - atan(length(v.xy), v.z) * 0.31830988618379067;
            gl_FragColor = texture2D(texture, tex);
        }
        """)
        cls.mat_local = glGetUniformLocation(cls.program, "lorentz")
        cls.tex_local = glGetUniformLocation(cls.program, "texture")
    
    def draw(self, pm, L):
        m = self.m * L * pm
        glUseProgram(self.program)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glUniform1i(self.tex_local, 0)
        glUniformMatrix4fv(self.mat_local, 1, GL_FALSE, m.to_glsl())
        glVertexPointer(3, GL_FLOAT, 0, self.vertex)
        glDrawArrays(GL_QUADS, 0, self.n)
        glUseProgram(0)

