# coding: utf8
# utils/utils.py
import os

from program.const import IMG_DIR, path

def search_imagefile(name):
    l = [os.path.join(IMG_DIR, a, b, c) for a in["", "../"]for b in["", "img/"]for c in["", "texture/"]]
    for i in l:
        path = os.path.join(i, name)
        if os.path.isfile(path):
            return path
    return name
