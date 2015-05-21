# -*- mode: python -*-
a = Analysis(['LSBattle3D.py'],
             pathex=['/Users/odakin/Dropbox/Physics/relativity/daiju/FPS3D/v11'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='LSBattle3D',
          debug=False,
          strip=None,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='LSBattle3D')
app = BUNDLE(coll,
             name='LSBattle3D.app',
             icon=None)
