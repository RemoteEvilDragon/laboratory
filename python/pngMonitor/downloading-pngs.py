#!/usr/bin/env python
#-*- coding:utf-8 -*-
import time
import ftplib
import os
import sys

#step 1,download files successful!
#step 2,syncing files --TODO
pngDir = "pngLib"

def downloading():
	server="27.126.181.90"
	username="athenking"
	password="freedom"

	myFtp = ftplib.FTP(server,username,password)

	def get_Dir(path,ftp):
		if not os.path.isdir(path):
			os.mkdir(path)
		os.chdir(path)
		print path
		ftp.cwd(path)

		files = ftp.nlst()
		for f in files:
			try:
				# ftp.size(path)
				#download file
				ftp.retrbinary('RETR '+f,open(f,'wb').write)
			except ftplib.error_perm, e:
				get_Dir(f,ftp)
				ftp.cwd("..")
				os.chdir("..")

	get_Dir(pngDir,myFtp)

	myFtp.quit()

downloading()