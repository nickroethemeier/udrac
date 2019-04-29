#!/usr/bin/python3
from tkinter import *
from tkinter.messagebox import showinfo
import urllib.request	
import urllib.parse 
from urllib.error import URLError, HTTPError
import os
import ssl
import json
import re
from subprocess import Popen
import platform

hosttypes = ["C6100", "C6220", "iDRAC6", "iDRAC6-Blade"]

### Default Values
defaultHost = ""
defaultType = "C6100"
defaultUser = "root"
defaultPass = ""

### Global Vars
debugmsg = 0
ver="0.6"



class hostInfo:
	def __init__(self, addr, type, username, password):
		self.addr = addr
		self.type = type
		self.username = username
		self.password = password



def connC6100(host):
	params = { "WEBVAR_USERNAME" : host.username, "WEBVAR_PASSWORD": host.password }  ## Builds Host creds for POST Method
	data = urllib.parse.urlencode(params).encode()
	
	print("Attempting to connect to "+host.addr+', using '+host.type+' format with username '+host.username)
	try:
		ssl._create_default_https_context = ssl._create_unverified_context   ##Disables SSL Checks... EVIL
		req = urllib.request.Request('https://'+host.addr+':443/rpc/WEBSES/create.asp',data=data)
		with urllib.request.urlopen(req,timeout=4) as f:
			buf = f.read().decode('utf-8')
	except HTTPError as e:
		# do something
		print('Error code: ', e.code)
	except URLError as e:
		# do something (set req to blank)
		print('Reason: ', e.reason)
	cookie = re.search("'SESSION_COOKIE'\s:\s'(\w*)'",buf)		## GET DAT COOKIE
	cookie = cookie.group(1)
	print("Conn Phase 1: SessionCookie: "+cookie)
	if (cookie.find('Failure') != -1):
		print("Invalid Username or Password...")
		showinfo("Invalid Username or Password...", "Returned session cookie is invalid")
		return
	

	sessionCookieString = "SessionCookie=" + cookie 	## Conform SessionCookie to format expected for Header
	req = urllib.request.Request('https://'+host.addr+':443/Java/jviewer.jnlp',headers={"Cookie": sessionCookieString })
	with urllib.request.urlopen(req,timeout=4) as f:
		buf = f.read(3000).decode('utf-8')
	returnedArgs = re.findall(r'(\<argument\>(\S*)\<\/argument>)',buf, re.MULTILINE) 	### REGEX to extract Java ARGS
	JNLPhost=returnedArgs[0][1]
	JNLPport=returnedArgs[1][1]
	JNLPtoken=returnedArgs[2][1]
	
	scrpath = os.path.abspath(os.path.dirname(sys.argv[0]))
	if opsys == "Windows":
		cmd = '"'+scrpath+'\\win-jre\\bin\\java.exe" -cp "'+scrpath+'\\c6100\\JViewer.jar" -Djava.library.path="'+scrpath+'\\c6100\\lib" com.ami.kvm.jviewer.JViewer '+ JNLPhost + " " + JNLPport + " " + JNLPtoken
	elif opsys == "Linux":
		cmd = '"'+scrpath+'/lin-jre/bin/java" -cp "'+scrpath+'/c6100/JViewer.jar" -Djava.library.path="'+scrpath+'/c6100/lib" com.ami.kvm.jviewer.JViewer '+ JNLPhost + " " + JNLPport + " " + JNLPtoken
	elif opsys == "Darwin":
		cmd = '"'+scrpath+'/osx-jre/bin/java" -cp "'+scrpath+'/c6100/JViewer.jar" com.ami.kvm.jviewer.JViewer '+ JNLPhost + " " + JNLPport + " " + JNLPtoken
	
	if debugmsg == 1:
		print (cmd)
		showinfo("CMD", cmd)
	
	Popen(cmd)
	return




def connC6220(host):
	print("Attempting to connect to "+host.addr+', using '+host.type+' format with username '+host.username)
	
	scrpath = os.path.abspath(os.path.dirname(sys.argv[0]))
	if opsys == "Windows":
		cmd = '"'+scrpath+'\\win-jre\\bin\\java.exe" -cp "'+scrpath+'\\c6220\\avctKVM.jar" -Djava.library.path="'+scrpath+'\\c6220\\lib" com.avocent.kvm.client.Main C6220 ip='+host.addr+' platform=ast2300 vmprivilege=true user='+host.username+' passwd='+host.password+' kmport=7578 vport=7578 apcp=1 version=2 platform=ASPEED color=0 softkeys=1 statusbar=ip,un,fr,bw,kp,led power=1'
	elif opsys == "Linux":
		cmd = '"'+scrpath+'/lin-jre/bin/java" -cp "'+scrpath+'/c6220/avctKVM.jar" -Djava.library.path="'+scrpath+'/c6220/lib" com.avocent.kvm.client.Main C6220 ip='+host.addr+' platform=ast2300 vmprivilege=true user='+host.username+' passwd='+host.password+' kmport=7578 vport=7578 apcp=1 version=2 platform=ASPEED color=0 softkeys=1 statusbar=ip,un,fr,bw,kp,led power=1'
	elif opsys == "Darwin":
		cmd = '"'+scrpath+'/osx-jre/bin/java" -cp "'+scrpath+'/c6220/avctKVM.jar" -Djava.library.path="'+scrpath+'/c6220/lib" com.avocent.kvm.client.Main C6220 ip='+host.addr+' platform=ast2300 vmprivilege=true user='+host.username+' passwd='+host.password+' kmport=7578 vport=7578 apcp=1 version=2 platform=ASPEED color=0 softkeys=1 statusbar=ip,un,fr,bw,kp,led power=1'
	
	if debugmsg == 1:
		print (cmd)
		showinfo("CMD", cmd)
	
	Popen(cmd)
	return



def conniDRAC6(host):
	print("Attempting to connect to "+host.addr+', using '+host.type+' format with username '+host.username)
	
	scrpath = os.path.abspath(os.path.dirname(sys.argv[0]))
	if opsys == "Windows":
		cmd = '"'+scrpath+'\\win-jre\\bin\\java.exe" -cp "'+scrpath+'\\idrac6\\avctKVM.jar" -Djava.library.path="'+scrpath+'\\idrac6\\lib" com.avocent.idrac.kvm.Main ip='+host.addr+' kmport=5900 vport=5900 user='+host.username+' passwd='+host.password+' apcp=1 version=2 vmprivilege=true '
	elif opsys == "Linux":
		cmd = '"'+scrpath+'/lin-jre/bin/java" -cp "'+scrpath+'/idrac6/avctKVM.jar" -Djava.library.path="'+scrpath+'/idrac6/lib" com.avocent.idrac.kvm.Main ip='+host.addr+' kmport=5900 vport=5900 user='+host.username+' passwd='+host.password+' apcp=1 version=2 vmprivilege=true '
	elif opsys == "Darwin":
		cmd = '"'+scrpath+'/osx-jre/bin/java" -cp "'+scrpath+'/idrac6/avctKVM.jar" -Djava.library.path="'+scrpath+'/idrac6/lib" com.avocent.idrac.kvm.Main ip='+host.addr+' kmport=5900 vport=5900 user='+host.username+' passwd='+host.password+' apcp=1 version=2 vmprivilege=true '
	
	if debugmsg == 1:
		print (cmd)
		showinfo("CMD", cmd)

	Popen(cmd)
	return
	


def conniDRAC6_Blade(host):
	params = { "WEBVAR_USERNAME" : host.username, "WEBVAR_PASSWORD": host.password ,"WEBVAR_ISCMCLOGIN": "0"}  ## Builds Host creds for POST Method
	data = urllib.parse.urlencode(params).encode()
	
	print("Attempting to connect to "+host.addr+', using '+host.type+' format with username '+host.username)
	try:
		ssl._create_default_https_context = ssl._create_unverified_context   ##Disables SSL Checks... EVIL
		req = urllib.request.Request('https://'+host.addr+':443/Applications/dellUI/RPC/WEBSES/create.asp',data=data)
		with urllib.request.urlopen(req,timeout=4) as f:
			buf = f.read().decode('utf-8')
	except HTTPError as e:
		# do something
		print('Error code: ', e.code)
	except URLError as e:
		# do something (set req to blank)
		print('Reason: ', e.reason)
	##print(buf)
	cookie = re.search("'SESSION_COOKIE'\s:\s'(\w*)',",buf)		## GET DAT COOKIE
	cookie = cookie.group(1)
	print("Conn Phase 1: SessionCookie: "+cookie)
	if (cookie.find('Failure') != -1):
		print("Invalid Username or Password...")
		showinfo("Invalid Username or Password...", "Returned session cookie is invalid")
		return
		
	sessionCookieString = "SessionCookie=" + cookie 	## Conform SessionCookie to format expected for Header
	req = urllib.request.Request('https://'+host.addr+':443/Applications/dellUI/Java/jviewer.jnlp',headers={"Cookie": sessionCookieString })
	with urllib.request.urlopen(req,timeout=4) as f:
		buf = f.read(3000).decode('utf-8')
	returnedArgs = re.findall(r'(\<argument\>(\S*)\<\/argument>)',buf, re.MULTILINE) 	### REGEX to extract Java ARGS
	args = returnedArgs[1][1], returnedArgs[2][1], returnedArgs[3][1], returnedArgs[4][1], returnedArgs[5][1], returnedArgs[6][1], returnedArgs[7][1], returnedArgs[8][1], returnedArgs[9][1], returnedArgs[10][1]
	fullArgs = str(" ".join(args))
	
	#fullArgs=returnedArgs[0][1].string, returnedArgs[1][1].string
	
	scrpath = os.path.abspath(os.path.dirname(sys.argv[0]))
	if opsys == "Windows":
		cmd = '"'+scrpath+'\\win-jre\\bin\\java.exe" -cp "'+scrpath+'\\idrac6-blade\\JViewer.jar" -Djava.library.path="'+scrpath+'\\idrac6-blade\\lib" com.ami.kvm.jviewer.JViewer '+host.addr+" "+fullArgs
	elif opsys == "Linux":
		cmd = '"'+scrpath+'/lin-jre/bin/java" -cp "'+scrpath+'/idrac6-blade/JViewer.jar" -Djava.library.path="'+scrpath+'/idrac6-blade/lib" com.ami.kvm.jviewer.JViewer '+host.addr+" "+fullArgs
	elif opsys == "Darwin":
		showerror("Dell iDRAC6 for Blades SUCK", "They don't provide the correct OSX Native Libraries (In particular the Floppy Library WTF?), and for whatever reason, the keyboard doesn't work without it.   I'll Continue to connect without it, but you won't be able to type. Sorry")
		cmd = '"'+scrpath+'/osx-jre/bin/java" -cp "'+scrpath+'/idrac6-blade/JViewer.jar" -Djava.library.path="'+scrpath+'/idrac6-blade/lib" com.ami.kvm.jviewer.JViewer '+host.addr+" "+fullArgs
	
	if debugmsg == 1:
		print (cmd)
		showinfo("CMD", cmd)
	
	Popen(cmd)
	return


def conninit(hostforminfo):
	##Copy user entries from form into hostInfo class
	host=hostInfo(hostforminfo[0].get(), hostforminfo[1].get(), hostforminfo[2].get(), hostforminfo[3].get())
	
    
	## What type of host is this?
	if host.type == "C6100":
		connC6100(host)
	elif host.type == "C6220":
		connC6220(host)
	elif host.type == "iDRAC6":
		conniDRAC6(host)
	elif host.type == "iDRAC6-Blade":
		conniDRAC6_Blade(host)
	elif host.type == "iDRAC7":
		showinfo("Do you really need this?  If so, contact Nick")



def makeform(root):
	hostinfo = []
	
	row1 = Frame(root)
	hosttypelabel = Label(row1, width=15, text="DRAC Type", anchor='w')
	ht = StringVar()
	ht.set(defaultType)
	hosttype = OptionMenu(row1,ht,*hosttypes)
	row1.pack(side=TOP, fill=X, padx=5, pady=5)
	hosttypelabel.pack(side=LEFT)
	hosttype.pack(side=RIGHT, expand=YES, fill=X)

	
	row2 = Frame(root)
	hostnamelabel = Label(row2, width=15, text="Hostname", anchor='w')
	hostname = Entry(row2)
	hostname.insert(0, defaultHost)
	row2.pack(side=TOP, fill=X, padx=5, pady=5)
	hostnamelabel.pack(side=LEFT)
	hostname.pack(side=RIGHT, expand=YES, fill=X)


	row3 = Frame(root)
	usernamelabel = Label(row3, width=15, text="Username", anchor='w')
	username = Entry(row3)
	username.insert(0, defaultUser)
	row3.pack(side=TOP, fill=X, padx=5, pady=5)
	usernamelabel.pack(side=LEFT)
	username.pack(side=RIGHT, expand=YES, fill=X)


	row4 = Frame(root)
	passwordlabel = Label(row4, width=15, text="Password", anchor='w')
	password = Entry(row4, show='*')
	password.insert(0, defaultPass)
	row4.pack(side=TOP, fill=X, padx=5, pady=5)
	passwordlabel.pack(side=LEFT)
	password.pack(side=RIGHT, expand=YES, fill=X)


	hostinfo = [hostname, ht, username, password]
	return hostinfo





if __name__ == '__main__':
	opsys = platform.system()
	
	print("μDRAC "+ver+" Multiplatform Edition")
	print("OS Detected as "+opsys)
	
	root = Tk()
	form = makeform(root)
	root.title("μDRAC "+ver)
	root.bind('<Return>', (lambda event, e=form: conninit(e)))
	
	btnconn = Button(root, text='Connect', command=(lambda e=form: conninit(e)))
	btnconn.pack(side=LEFT, padx=5, pady=5)
	btnquit = Button(root, text='Quit', command=root.quit)
	btnquit.pack(side=LEFT, padx=5, pady=5)
	
	root.mainloop()
