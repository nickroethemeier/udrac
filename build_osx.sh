echo "Marking Execute bit on Java JRE binary"
chmod +x src/osx-jre/bin/java
echo "Building Package using PyInstaller"
python3 -m PyInstaller ./uDRAC_osx.spec --onefile --windowed
echo "Copying rest of JRE, JARs and libs to .app file"
cp -R dist/uDRAC\ OSX/* dist/uDRAC\ OSX.app/Contents/MacOS/
