#coding: utf8
import os as _os
import glob as _glob
import sys as _sys
# import traceback as _traceback
# import logging as _logging

from program import const
# _logging.basicConfig(filename=_os.path.join(const.path, 'script.log'), filemode='w',
#                      level=_logging.WARNING,
#                      format='%(levelname)s:%(message)s')

from .common import Block
from .parser import Parser
from .game import Game
from .ui import UI
from .enemy import Enemy
from .player import Player
from .world import World


def make_default_script():
    out_path = _os.path.dirname(_sys.argv[0])
    f = open(_os.path.join(out_path, "default.script"), "w")
    indent = "    "

    def pri(block, depth=0):
        f.write(indent*depth + block.__class__.__name__ + " {\n")
        depth += 1
        l = [a for a in dir(block) if not a.startswith("_")]
        l.sort(key=lambda a:isinstance(block[a], Block)*1 + isinstance(block[a], list)*1)
        width = 40
        for name in l:
            if "_"+name+"_obj" in block:
                f.write(indent*depth + name + " {\n")
                for nex in block[name]:
                    pri(nex, depth+1)
                f.write(indent*depth + "}\n")
            elif isinstance(block[name], Block):
                pri(block[name], depth)
            else:
                s = indent*depth + name + " = " + str(block[name]).replace("\n", "\\n")
                n = len(s)
                if "_"+name+"_func" in block:
                    s += " "*(width-n if n < width else 0) + " # " +  block["_"+name+"_func"].__name__
                else:
                    s += " "*(width-n if n < width else 0) + " # eval"
                f.write(s + "\n")
        depth -= 1
        f.write(indent*depth + "}\n")

    for block in _kws.itervalues():
        pri(block)

    # print "make default script: OK"

game   = Game()
ui     = UI()
player = Player()
enemy  = Enemy()
world  = World()

_kws = {"Game":game,
        "UI":ui,
        "Player":player,
        "Enemy":enemy,
        "World":world}
_parser = Parser()
for _name in _glob.iglob(_os.path.join(const.SCRIPT_DIR, "*.script")):
    # _logging.info("parse '%s' file", _name)
    try:
        _parser.parse(open(_name), **_kws)
    except:pass
        # _s = _traceback.format_exc()
        # _logging.error(_s)
for _name in _glob.iglob(_os.path.join(_os.path.dirname(_sys.argv[0]), "*.script")):
    # _logging.info("parse '%s' file", _name)
    try:
        _parser.parse(open(_name), **_kws)
    except:pass
        # _s = _traceback.format_exc()
        # _logging.error(_s)


for _key in _kws:
    if hasattr(_kws[_key], "_check"):
        _kws[_key]._check()

if game.output_script:
    make_default_script()
