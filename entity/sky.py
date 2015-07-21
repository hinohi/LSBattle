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



class Sky(object):
    
    program = None
    mat_local = None
    tex_local = None
    
    def __init__(self):
        self.init_vertex()
        self.init_program()
        self.m = Matrix44.z_rotation(script.world.sky.rotation)
        texture_name0 = search_imagefile(script.world.sky.texture0)
        self.texture_id0 = load_texture(texture_name0)
        texture_name1 = search_imagefile(script.world.sky.texture1)
        self.texture_id1 = load_texture(texture_name1)

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
            float T = -length(pos);
            vec4 Xi = lorentz * vec4(pos, T);
            float TT = Xi.w;
            vec2 tex;
            tex.t = 1.0 - atan(length(Xi.xy), Xi.z) * 0.31830988618379067;
            tex.s = atan(Xi.y, Xi.x) * 0.15915494309189533;
            vec4 color;
            if(abs(tex.s) < 0.499) {
                color = texture2D(texture0, tex.st);
            }else{
                tex.s = atan(-Xi.y, -Xi.x) * 0.15915494309189533;
                color = texture2D(texture1, tex.st);
            }
            color *= 255.0;
            float l = max(max(color.r, color.g), color.b);
            if (l > 1) {
                color *= 255.0 / l;
                //color /= l;
                float Tr, Tg, Tb;
                Tb = 1000.0 + 904.495*exp(0.00721929 * color.b);
                Tr = 6000.0 + 8.01879e20 * pow(max(color.r, 1.0), -7.507239275877164);
                if (color.b > 254.0) {
                    Tg = 6502.86;
                } else {
                    if (color.b / max(color.r, 1.0) > 0.98084) {
                        Tg = 505.192 * exp(0.0100532 * color.g);
                    } else {
                        Tg = 6000.0 + 3.55446e34 * pow(max(color.g, 1), -13.24242861627803);
                    }
                }

                Tr *= T / TT;
                Tg *= T / TT;
                Tb *= T / TT;
                if (1905 > Tb) {
                    color.b = 0.0;
                } else if (6700 < Tb) {
                    color.b = 255.0;
                } else {
                    color.b = -305.045 + 138.518 * log(0.01 * Tb - 10.0);
                }
                if (6689 > Tr) {
                    color.r = 255.0;
                } else {
                    color.r = 608.873 * pow(Tr - 6000.0, -0.133205);
                }
                if (506 > Tg) {
                    color.g = 0.0;
                } else if (6502.86 > Tg) {
                    color.g = -619.2 + 99.4708 * log(Tg);
                } else {
                    color.g = 406.534 * pow(Tg - 6000.0, -0.0755148);
                }
                color *= l/255;
            }
            gl_FragColor = color/255;
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


class Sky2(object):
    
    program = None
    mat_local = None
    tex_local = None
    
    def __init__(self):
        self.init_vertex()
        self.init_program()
        self.m = Matrix44.z_rotation(script.world.sky.rotation)
        texture_name0 = search_imagefile(script.world.sky.texture0)
        self.texture_id0 = load_texture(texture_name0)
        texture_name1 = search_imagefile(script.world.sky.texture1)
        self.texture_id1 = load_texture(texture_name1)

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
            vec4 Xi = lorentz * vec4(pos, -length(pos));
            vec2 tex;
            tex.t = 1 - atan(length(Xi.xy), Xi.z) * 0.31830988618379067;
            tex.s = atan(Xi.y, Xi.x) * 0.15915494309189533;
            if(abs(tex.s) < 0.499) {
                gl_FragColor = texture2D(texture0, tex.st);
            }else{
                tex.s = atan(-Xi.y, -Xi.x) * 0.15915494309189533;
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
