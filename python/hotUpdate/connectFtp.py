#!/usr/bin/env python
import ftplib
import os
import sys

server="27.126.181.90"
username="athenking"
password="freedom"

myFtp = ftplib.FTP(server,username,password)
newDir = sys.argv[1]

def uploadDir(path):
	files = os.listdir(path)
	os.chdir(path)
	for f in files:
		if os.path.isfile(f):
			fc = open(f,'rb')
			myFtp.storbinary('STOR '+f,fc)
			fc.close()
		elif os.path.isdir(f):
			myFtp.mkd(f)
			myFtp.cwd(f)
			uploadDir(f)
	myFtp.cwd('..')
	os.chdir('..')

myFtp.mkd(newDir)
myFtp.cwd(newDir)
uploadDir(os.path.join(newDir))