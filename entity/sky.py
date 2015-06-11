# coding: utf8
# entity/sky.py
from math import pi, tan

from OpenGL.GL import *

from go import Matrix44
from model.polygon import MqoGpoPolygon
from program.box import BOX
from program.utils import load_texture, compile_program, search_imagefile
from program.const import IMG_DIR, VIEW_ANGLE
from program import script


class Sky2(object):
    
    program = None
    mat_local = None
    tex_local = None
    
    def __init__(self):
        self.init_vertex()
        self.init_program()
        self.m = Matrix44.z_rotation(script.world.sky.rotation)
        texture_name = search_imagefile(script.world.sky.texture)
        self.texture_id = load_texture(texture_name)

    def init_vertex(self):
        angle = VIEW_ANGLE*pi/180
        z = -1.0
        x = tan(angle) * abs(z)
        y = x * BOX.Y / BOX.X
        vertex = [ x,  y, z,
                  -x,  y, z,
                  -x, -y, z,
                   x, -y, z]
        self.n = len(vertex)/3
        self.vertex = (GLfloat*len(vertex))(*vertex)

    def init_program(self):
        self.program = compile_program(
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
            tex.s = atan(v.y, v.x) * 0.15915494309189533;
            tex.t = 1-atan(length(v.xy), v.z) * 0.31830988618379067;
            gl_FragColor = texture2D(texture, tex);
        }
        """)
        self.mat_local = glGetUniformLocation(self.program, "lorentz")
        self.tex_local = glGetUniformLocation(self.program, "texture")
    
    def draw(self, pm, L):
        m = self.m * L * pm
        glUseProgram(self.program)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glUniform1i(self.tex_local, 0)
        glUniformMatrix4fv(self.mat_local, 1, GL_FALSE, m.to_glsl())
        glVertexPointer(3, GL_FLOAT, 0, self.vertex)
        glDrawArrays(GL_QUADS, 0, self.n)
        glUseProgram(0)


class Sky(object):
    
    program = None
    mat_local = None
    tex_local = None
    
    def __init__(self):
        self.init_vertex()
        self.init_program()
        self.m = Matrix44.z_rotation(script.world.sky.rotation)
        texture_name = search_imagefile(script.world.sky.texture)
        self.texture_id0 = load_texture(texture_name)
        self.texture_id1 = load_texture(search_imagefile("milkyway2.jpg"))
        # self.texture_id0 = load_texture(search_imagefile("a.png"))
        # self.texture_id1 = load_texture(search_imagefile("b.png"))

    def init_vertex(self):
        angle = VIEW_ANGLE*pi/180
        z = -1.0
        x = tan(angle) * abs(z)
        y = x * BOX.Y / BOX.X
        vertex = [ x,  y, z,
                  -x,  y, z,
                  -x, -y, z,
                   x, -y, z]
        self.n = len(vertex)/3
        self.vertex = (GLfloat*len(vertex))(*vertex)

    def init_program(self):
        self.program = compile_program(
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
        uniform sampler2D texture0;
        uniform sampler2D texture1;
        void main() {
            vec4 v = lorentz * vec4(pos, -length(pos));
            vec2 tex;
            tex.t = 1 - atan(length(v.xy), v.z) * 0.31830988618379067;
            tex.s = atan(v.y, v.x) * 0.15915494309189533;
            //if(abs(tex.s) > 0.4) {
            //    tex.s = atan(-v.y, -v.x) * 0.15915494309189533;
            //    gl_FragColor = texture2D(texture1, tex.st);
            //}else{
            //    gl_FragColor = texture2D(texture0, tex.st);
            //}
            if(abs(tex.s) < 0.499) {
                gl_FragColor = texture2D(texture0, tex.st);
            }else{
                tex.s = atan(-v.y, -v.x) * 0.15915494309189533;
                gl_FragColor = texture2D(texture1, tex.st);
            }
        }
        """)
        self.mat_local = glGetUniformLocation(self.program, "lorentz")
        self.tex0_local = glGetUniformLocation(self.program, "texture0")
        self.tex1_local = glGetUniformLocation(self.program, "texture1")
    
    def draw(self, pm, L):
        m = self.m * L * pm
        glUseProgram(self.program)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id0)
        glUniform1i(self.tex0_local, 0)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id1)
        glUniform1i(self.tex1_local, 1)
        glUniformMatrix4fv(self.mat_local, 1, GL_FALSE, m.to_glsl())
        glVertexPointer(3, GL_FLOAT, 0, self.vertex)
        glDrawArrays(GL_QUADS, 0, self.n)
        glUseProgram(0)
        glActiveTexture(GL_TEXTURE0)
