#coding: utf8
from OpenGL import GL
import sdl2
import sdl2.ext

from program.box import BOX
from sequence.locals import MenuItems

class Loading(object):
    def __init__(self):
        self.text = ["Now loading....."]

    def init(self):
        self.menu = MenuItems(self.text, BOX.Y/12)

    def draw(self):
        self.init()
        GL.glClear(GL.GL_DEPTH_BUFFER_BIT|GL.GL_COLOR_BUFFER_BIT)
        self.menu.draw()
        sdl2.SDL_GL_SwapWindow(BOX.window)
