#!/usr/bin/env python
import ftplib
import os

server="27.126.181.90"
username="athenking"
password="freedom"

myFtp = ftplib.FTP(server,username,password)
myPath = "./testUpload"

def uploadDir(path):
	files = os.listdir(path)
	os.chdir(path)
	print files
	for f in files:
		# formated_f = os.path.join(r'\{}'.format(f))
		formated_f = f
		print "orginal f is " + f
		print formated_f
		if os.path.isfile(formated_f):
			print "detect one file "+f
			fc = open(f,'rb')
			myFtp.storbinary('STOR '+f,fc)
			fc.close()
		elif os.path.isdir(formated_f):
			print "detect one directory "+f
			myFtp.mkd(f)
			myFtp.cwd(f)
			uploadDir(formated_f)
	myFtp.cwd('..')
	os.chdir('..')

uploadDir(os.path.join(myPath))