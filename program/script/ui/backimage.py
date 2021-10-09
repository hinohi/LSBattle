#coding: utf8
from ..common import Block, color_func, high_func_num, func_str

_modes = ["FILL",
          "ALIGN",
          "CUT"]
def _image_fill_mode_func(line):
    line = line.strip().upper()
    if line in _modes:
        return line
    else:
        return _modes[0]

class backimage(Block):
    def __init__(self):
        self.color = (0.4, 0.4, 0.4, 1.0)
        self.image = None
        self.image_color = (1.0, 1.0, 1.0, 1.0)
        self.image_fill_mode = _modes[0]
        self.alpha = 0.5
        self._color_func = color_func
        self._image_func = func_str
        self._image_color_func = color_func
        self._image_fill_mode_func = _image_fill_mode_func
        self._alpha_func = high_func_num(float, 0.0, 1.0)
