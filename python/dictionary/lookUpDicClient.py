#!/usr/bin/env python
#-*- coding:utf-8 -*-
import socket
import sys

HOST,PORT = "27.126.181.90",13206
word=sys.argv[1]
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
	sock.connect((HOST,PORT))
	sock.sendall(word+"\n")
	received = sock.recv(1024)

finally:
	sock.close()

print "Recived: {}".format(received)


