#!/usr/bin/env python
from hashlib import md5
import sys

def Md5(file):
	m = md5()
	b_file = open(file,'rb')
	m.update(b_file.read())
	b_file.close()
	print m.hexdigest()

Md5(sys.argv[1])