# coding: utf8
# utils/texture.py
from math import sqrt

from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image


DY_TEXTURE_BETA = 0
DY_TEXTURE_KYU  = 1
DY_TEXTURE_EDGE = 2
def dynamic_texture(n):
    if n == DY_TEXTURE_BETA:
        L = 64
        raw_data = "\xff"*(L*L)
        return raw_data, L, L, "L"
    elif n == DY_TEXTURE_KYU:
        L = 64
        a = L - 1.0
        data = []
        for y in xrange(L):
            yy = y/a * 2.0 - 1.0
            for x in xrange(L):
                xx = x/a * 2.0 - 1.0
                z = 1.0 - (xx**2 + yy**2)
                data.extend([1, sqrt(z) if z > 0.0 else 0])
        raw_data = "".join(map(lambda i:chr(int(i*255)), data))
        return raw_data, L, L, "LA"
    elif n == DY_TEXTURE_EDGE:
        L = 64
        a = L / 32 * 15
        b = L / 8
        data = []
        for y in xrange(L):
            yy = abs(y-(L-1)/2.0)
            for x in xrange(L):
                xx = abs(x-(L-1)/2.0)
                if (yy > a and xx > b) or (xx > a and yy > b):
                    z = 1
                else:
                    z = 0
                data.extend([1, z])
        raw_data = "".join(map(lambda i:chr(int(i*255)), data))
        return raw_data, L, L, "LA"

class TextureInfo(object):
    def __init__(self, name, texture_id, width, height, mode):
        self.name = name
        self.texture_id = texture_id
        self.width = width
        self.height = height
        self.mode = mode

_loaded_texture = {}
_using_texture_id = {}
def load_texture(name, use_cache=True, id_only=True):
    if use_cache:
        # cache check
        texture_info = _loaded_texture.get(name)
        if texture_info is not None and glIsTexture(texture_info.texture_id):
            if id_only:
                return texture_info.texture_id
            else:
                return texture_info
    if isinstance(name, str):
        try:
            img = Image.open(name)
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            width, height = img.size
            mode = img.mode
            if mode not in {"L", "RGB", "RGBA"}:
                img = img.convert("RGBA")
                mode = img.mode
            raw_data = img.tobytes()
        except IOError:
            raw_data, width, height, mode = dynamic_texture(0)
    else:
        raw_data, width, height, mode = dynamic_texture(name)

    texture_id = bind_texture(raw_data, width, height, mode)
    texture_info = TextureInfo(name, texture_id, width, height, mode)
    if texture_id in _using_texture_id:
        deleted_name = _using_texture_id[texture_id].name
        del _loaded_texture[deleted_name]
    _loaded_texture[name] = texture_info
    _using_texture_id[texture_id] = texture_info
    if id_only:
        return texture_id
    else:
        return _loaded_texture[name]

def bind_texture(raw_data, width, height, mode):
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D,
                    GL_TEXTURE_MAG_FILTER,
                    GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D,
                    GL_TEXTURE_MIN_FILTER,
                    GL_LINEAR_MIPMAP_LINEAR)
    n = {1:1, 2:2, 3:3, 4:4, "L":1, "LA":2, "RGB":3, "RGBA":4, "A":1}[mode]
    m = {1:GL_LUMINANCE, 2:GL_LUMINANCE_ALPHA, 3:GL_RGB, 4:GL_RGBA,
         "L":GL_LUMINANCE, "LA":GL_LUMINANCE_ALPHA,"RGB":GL_RGB, "RGBA":GL_RGBA,
         "A":GL_ALPHA}[mode]
    gluBuild2DMipmaps(GL_TEXTURE_2D,
                      n,
                      width,
                      height,
                      m,
                      GL_UNSIGNED_BYTE,
                      raw_data)
    return texture_id

