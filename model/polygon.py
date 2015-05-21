# -*- coding: utf8 -*-
# polygon.py
import os

from OpenGL.GL import *

from go import Vector4D, Matrix44, Lorentz
from model.mqo.mqo2gpo import mqo2gpo
from program.utils import load_texture, search_imagefile, compile_program


class Material(object):

    def __init__(self, color, tex_name=None, texture=True, path=""):
        self.color = color
        if tex_name and texture:
            #tex_name = search_imagefile(self.tex_name)
            tex_name = os.path.join(path, tex_name)
            self.tex_name = tex_name
            self.texture_id = load_texture(tex_name)
        else:
            self.tex_name = None
            self.texture_id = None

    def reload_texture(self):
        if self.tex_name is not None:
            self.texture_id = load_texture(self.tex_name)

class MqoGpoPolygon(object):

    def load_gpo(self, name, func=lambda x,y,z:(x,y,z), texture=True):
        igpo = open(name)
        if igpo.next().strip() != "Game Polygon Object":
            raise IOError("%s is not gpo file"%name)
        path, name = os.path.split(name)
        self.path = path
        vertices = []
        texcoords = []
        objects = []
        for line in igpo:
            words = line.split()
            if not words:continue
            if words[0] == "p":
                x, y, z, u, v = map(float, words[1:])
                vertices.extend(func(x, y, z))
                texcoords.extend([u, v])
            elif words[0] == "m":
                color = map(float, words[1:-1])
                tex_name = words[-1][1:-1]
                objects.append([Material(color, tex_name, texture, path), []])
            elif words[0] == "i":
                objects[-1][1] = map(int, words[1:])
                
        self.vertices = (GLfloat*len(vertices))(*vertices)
        self.texcoords = (GLfloat*len(texcoords))(*texcoords)
        
        self.objects = []
        for material, indices in objects:
            n = len(indices)
            obj = [material, n, (GLuint*n)(*indices)]
            self.objects.append(obj)
    
    def set_texture(self, tex_name):
        def _set(self, i, name):
            if os.path.isfile(os.path.join(self.path, name)):
                name = os.path.join(self.path, name)
                self.objects[i][0].texture_id = load_texture(name)
                self.objects[i][0].tex_name = name
            else:
                name = search_imagefile(name)
                self.objects[i][0].texture_id = load_texture(name)
                self.objects[i][0].tex_name = name
        if isinstance(tex_name, list) or isinstance(tex_name, tuple):
            for i, name in enumerate(tex_name):
                _set(self, i, name)
        else:
            _set(self, 0, tex_name)
            
    def make_gpo(self, name, ext=""):
        if ext.lower() in [".mqo", ".gpo"]:
            if os.path.isfile(name+ext):
                mqo2gpo(name+ext)
                return name + ".gpo"
            elif os.path.isdir(name):
                name = os.path.join(name, os.path.split(name)[1])
                return self.make_gpo(name, ext)
        elif ext == "":
            if os.path.isfile(name+".gpo"):
                if os.path.isfile(name+".mqo"):
                    if os.path.getmtime(name+".mqo") > os.path.getmtime(name+".gpo"):
                        mqo2gpo(name+".mqo")
                return name + ".gpo"
            elif os.path.isfile(name+".mqo"):
                mqo2gpo(name+".mqo")
                return name + ".gpo"
            elif os.path.isdir(name):
                name = os.path.join(name, os.path.split(name)[1])
                return self.make_gpo(name, ext)
            else:
                raise IOError("%s's model file is not exsit"%(os.path.split(name)[1]))
        raise IOError("%s's model file is not exsit"%(os.path.split(name)[1]+ext))

_polygon_cache = {}
class Polygon(MqoGpoPolygon):

    def load_program_tex(self):
        self.program_tex = compile_program(
        """
        #version 120
        uniform vec4 color;
        uniform mat4 Lorentz;
        uniform mat4 Rotate;
        uniform vec4 dX;
        uniform vec4 xp;
        void main() {
            vec4 xi = Rotate * gl_Vertex;
            xi.w = xp.w - distance(xp.xyz, xi.xyz);
            xi = dX + Lorentz * xi;
            xi.w = 1.0;
            gl_Position = gl_ModelViewProjectionMatrix * xi;
            gl_TexCoord[0] = gl_MultiTexCoord0;
            gl_FrontColor = color;
        }
        """,
        """
        #version 120
        uniform sampler2D texture;
        void main() {
            gl_FragColor = texture2D(texture, gl_TexCoord[0].xy) * gl_Color;
        }
        """)
        self.t_color_local = glGetUniformLocation(self.program_tex, "color")
        self.t_L_local = glGetUniformLocation(self.program_tex, "Lorentz")
        self.t_R_local = glGetUniformLocation(self.program_tex, "Rotate")
        self.t_dX_local = glGetUniformLocation(self.program_tex, "dX")
        self.t_xp_local = glGetUniformLocation(self.program_tex, "xp")
        self.tex_local = glGetUniformLocation(self.program_tex, "texture")
    
    def load_program_col(self):
        self.program_col = compile_program(
        """
        #version 120
        uniform vec4 color;
        uniform mat4 Lorentz;
        uniform mat4 Rotate;
        uniform vec4 dX;
        uniform vec4 xp;
        void main() {
            vec4 xi = Rotate * gl_Vertex;
            xi.w = xp.w - distance(xp.xyz, xi.xyz);
            xi = dX + Lorentz * xi;
            xi.w = 1.0;
            gl_Position = gl_ModelViewProjectionMatrix * xi;
            gl_FrontColor = gl_Color * color;
        }
        """,
        """
        #version 120
        void main() {
            gl_FragColor = gl_Color;
        }
        """)
        self.c_color_local = glGetUniformLocation(self.program_col, "color")
        self.c_L_local = glGetUniformLocation(self.program_col, "Lorentz")
        self.c_R_local = glGetUniformLocation(self.program_col, "Rotate")
        self.c_dX_local = glGetUniformLocation(self.program_col, "dX")
        self.c_xp_local = glGetUniformLocation(self.program_col, "xp")

    def __init__(self, name, func=lambda x,y,z:(x,y,z),
                 texture=True, color=(1.0,1.0,1.0,1.0)):
        self.load_program_col()
        self.load_program_tex()
        name, ext = os.path.splitext(name)
        if name in _polygon_cache:
            poly = _polygon_cache[name]
            if func(1.0, 1.0, 1.0) == poly.func(1.0, 1.0, 1.0):
                self.vertices = poly.vertices
                self.texcoords = poly.texcoords
                self.objects = poly.objects
                self.color = color
                self.texture = texture
                self.path = poly.path
                for obj in self.objects:
                    obj[0].reload_texture()
                return
        file_name = self.make_gpo(name, ext)
        self.load_gpo(file_name, func, texture)
        self.color = color
        self.func = func
        self.texture = texture
        _polygon_cache[name] = self

    def draw(self, Xp, L, X=Vector4D(0,0,0,0), U=Vector4D(1,0,0,0), R=Matrix44()):
        dX = X - Xp
        dX.t = -dX.length()
        xp = Lorentz(U).get_transform_v4(-dX)
        xp = [xp.x, xp.y, xp.z, xp.t]
        dX = L.get_transform_lis3(dX) + [0.0]
        L = (L * Lorentz(-U)).to_glsl()
        R = R.to_glsl()
        glVertexPointer(3, GL_FLOAT, 0, self.vertices)
        glTexCoordPointer(2, GL_FLOAT, 0, self.texcoords)
        program = 0
        for material, n, indices in self.objects:
            if material.texture_id is None:
                glColor(*material.color)
                if self.program_col != program:
                    glUseProgram(self.program_col)
                    glUniformMatrix4fv(self.c_L_local, 1, GL_FALSE, L)
                    glUniformMatrix4fv(self.c_R_local, 1, GL_FALSE, R)
                    glUniform4fv(self.c_dX_local, 1, dX)
                    glUniform4fv(self.c_xp_local, 1, xp)
                    glUniform4fv(self.c_color_local, 1, self.color)
                    program = self.program_col
            else:
                glBindTexture(GL_TEXTURE_2D, material.texture_id)
                if self.program_tex != program:
                    glUseProgram(self.program_tex)
                    glUniformMatrix4fv(self.t_L_local, 1, GL_FALSE, L)
                    glUniformMatrix4fv(self.t_R_local, 1, GL_FALSE, R)
                    glUniform4fv(self.t_dX_local, 1, dX)
                    glUniform4fv(self.t_xp_local, 1, xp)
                    glUniform4fv(self.t_color_local, 1, self.color)
                    glUniform1i(self.tex_local, 0)
                    program = self.program_tex
            glDrawElements(GL_TRIANGLES, n, GL_UNSIGNED_INT, indices)
        glUseProgram(0)
            
