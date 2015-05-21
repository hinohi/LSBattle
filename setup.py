# coding: utf8
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from glob import iglob
import os

# python setup.py build_ext --inplace

option = {}
if os.name == "nt":
    option['extra_compile_args'] = [
        '/EHsc', # 警告回避
        '/MT', # /MDオプション上書き
        ]
for pyxname in iglob("go/*.pyx"):
    name, ext = os.path.splitext(pyxname)
    ext_modules = [Extension(name.replace(os.sep, "."), [pyxname], **option)]
    setup(
        name = name.replace(os.sep, "."),
        cmdclass = {'build_ext': build_ext},
        ext_modules = ext_modules
    )
