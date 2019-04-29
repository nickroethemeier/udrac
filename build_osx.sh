python3 -m PyInstaller ./uDRAC_osx.spec --onefile --windowed
cp -R dist/uDRAC\ OSX/* dist/uDRAC\ OSX.app/Contents/MacOS/
