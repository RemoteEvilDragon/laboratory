#!/usr/bin/python
#coding=utf-8
import sys
import os
import platform
import subprocess


reload(sys)
sys.setdefaultencoding('utf-8')
filepath = sys.path[0]


def CALL(cmd):
	p=subprocess.Popen(cmd, shell=True)  
	a = p.wait()
	if a != 0 :
		LOGERR("An error occured when call command : %s , STOPPED!!!"%cmd)
		exit(1)
	return 0

CALL("python ./libs/register.py")