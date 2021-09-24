#coding: utf8
# const.py
import os as _os
import sys as _sys

path = _os.path.abspath(_os.path.dirname(_sys.argv[0]))
_input_path = _os.path.join(path, "resources")
sdl2_path = _os.path.join(_input_path, "bin", _os.name)
if _os.path.isdir(sdl2_path):
	_os.environ["PYSDL2_DLL_PATH"] = sdl2_path
else:
	_os.environ["PYSDL2_DLL_PATH"] = path

import sdl2

IMG_DIR    = _os.path.join(_input_path, "img/")
CONFIG_DIR = _os.path.join(_input_path, "config/")
SCRIPT_DIR = _os.path.join(_input_path, "script/")

VIEW_ANGLE = 60.0
GAME_NAME = "Light Speed Battle"

c = 299792458.0 #Light Speed [m/sec]

KS_RETURN = {sdl2.SDLK_RETURN, sdl2.SDLK_RETURN2, sdl2.SDLK_KP_ENTER}
KS_ESC = {sdl2.SDLK_ESCAPE, sdl2.SDLK_BACKSPACE, sdl2.SDLK_DELETE}

disp_sizes = [(640, 480),
              (800, 600),
              (1024, 768),
              (1280, 960),
              (1600, 1200)]
