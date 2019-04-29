# -*- mode: python -*-

block_cipher = None


a = Analysis(['src/uDRAC.py'],
             pathex=['/Users/nick/Dropbox/uDRAC/src'],
			 binaries=[
			      ('/System/Library/Frameworks/Tk.framework/Tk', 'tk'),
			      ('/System/Library/Frameworks/Tcl.framework/Tcl', 'tcl')],
             datas=[('src/osx-jre', 'osx-jre') , ('src/c6100','c6100'), ('src/c6220','c6220'), ('src/idrac6','idrac6'),  ('src/idrac6-blade', 'idrac6-blade')],
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
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='uDRAC OSX')
app = BUNDLE(exe,
        name='uDRAC OSX.app',
        icon=None,
        bundle_identifier=None,
		info_plist={
		    'NSHighResolutionCapable': 'True'
		    },)
