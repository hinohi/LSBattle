# coding: utf8
# utils/playing.py
from OpenGL.GL import *
from OpenGL.GLU import *

from program.box import BOX


def fill_screen(r, g, b, a=1.0):
    """
    over ray the screen by color (r,g,b,a)
    """
    FlatScreen.push()
    glColor(r, g, b, a)
    glBegin(GL_QUADS)
    glVertex(0,     0)
    glVertex(BOX.X, 0)
    glVertex(BOX.X, BOX.Y)
    glVertex(0,     BOX.Y)
    glEnd()
    FlatScreen.pop()

class FlatScreen(object):
    """
    FlatScreen.push()
    ~~~ some codes ~~~
    FlatScreen.pop()
    """
    matrix_stack = None
    @classmethod
    def push(cls):
        if cls.matrix_stack is None:
            glDisable(GL_DEPTH_TEST)
            glMatrixMode(GL_PROJECTION)
            cls.matrix_stack = glGetDouble(GL_PROJECTION_MATRIX)
            glLoadIdentity()
            glOrtho(0, BOX.X, 0, BOX.Y, -1, 1)
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()
        else:
            raise Exception("FlatScreen.push called two times without calling FlatScreen.pop")

    @classmethod
    def pop(cls):
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glLoadMatrixd(cls.matrix_stack)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        cls.matrix_stack = None

class FramePerSec(object):
    """
    count flame par second
    """
    def __init__(self, n=20):
        self.n = n
        self.l = [1/40.]*n
        self.i = 0

    def add(self, ds):
        self.l[self.i%self.n] = ds
        self.i += 1

    def get(self):
        return self.n / sum(self.l)

class Snapshot(object):
    """
    take a display's snapshot and show it

    sp = Snapshot() -> make instance
    sp.captcha()    -> take a snapshot
    sp.draw()       -> show the image
    sp.delete()     -> delete the image data
    """
    def captcha(self):
        self.buf = glReadPixels(0, 0, BOX.X, BOX.Y, GL_RGB, GL_UNSIGNED_BYTE)
        self.make_image()

    def make_image(self):
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        gluBuild2DMipmaps(GL_TEXTURE_2D,
                          3,
                          BOX.X,
                          BOX.Y,
                          GL_RGB,
                          GL_UNSIGNED_BYTE,
                          self.buf)

    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glColor(1.0, 1.0, 1.0, 1.0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        FlatScreen.push()
        glBegin(GL_QUADS)
        glTexCoord(0.0, 0.0); glVertex(0.0,   0.0)
        glTexCoord(1.0, 0.0); glVertex(BOX.X, 0.0)
        glTexCoord(1.0, 1.0); glVertex(BOX.X, BOX.Y)
        glTexCoord(0.0, 1.0); glVertex(0.0,   BOX.Y)
        glEnd()
        FlatScreen.pop()
        glDisable(GL_TEXTURE_2D)

    def delete(self):
        glDeleteTextures(self.texture_id)
