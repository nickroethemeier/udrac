# μDRAC
### Dell DRAC Micro Launcher for Windows, Linux and OSX

## Currently Supported
* Dell iDRAC 6
* Dell iDRAC 6 (M-Series Varients)
* Dell C6100 nodes
* Dell C6220 nodes

## Build Dependencies
* Python 3.7 or greater
* PyInstaller

## Some Important Notes
This GUI launcher is based on "reverse engineered" interactions with the out-of-band management card. 

**Absolutly no respect or effort has been made toward security**, and often the password is literally handed to the java code via argument...

**WARNING**: Due to the nature of connecting to OOB server management, *ALL SSL ISSUES ARE BYPASSED AND IGNORED*

## Extra Important License Notes
This launcher package contains code from MANY sources including
* Java JRE, from Sun Microsystems / Oracle
* C6100 JViewer from America Megatrends
* C6220 KVM from Avocent Corporation
* iDRAC 6 from Dell Computers / Avocent Corporation

These external libraries are included as part of the uDRAC simply because they are annoying to acquire.   If anyone cares please let me know.   The only portion that I am licensing GPLv3 is the Python code that I am providing, namely **udrac.py**
