# -*- mode: python -*-

block_cipher = None

a = Analysis(['src\\uDRAC.py'],
             pathex=['X:\\Dropbox\\uDrac\\src'],
             binaries=[],
             datas=[('src\\win-jre', 'win-jre') , ('src\\c6100','c6100'), ('src\\c6220','c6220'), ('src\\idrac6','idrac6'),  ('src\\idrac6-blade', 'idrac6-blade')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='uDRAC',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='uDRAC Windows')
