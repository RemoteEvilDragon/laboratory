#!/usr/bin/python
#coding=utf-8

import sys
import os
import platform
import shutil
import string
import time
import re
import json
import subprocess

reload(sys)
sys.setdefaultencoding('utf-8')
filepath = sys.path[0]
sys.path.append(os.path.join(filepath,"./"))

from PTlib.utils import *

# print (sys.path)
expath = filepath
pythonpackagepath = ""
for p in sys.path :
	if p.endswith("site-packages") :
		pythonpackagepath = p

pathfile = []

pathfile.append("import sys; sys.__plen = len(sys.path)\n")
pathfile.append(expath+'\n')
# pathfile.append(os.path.join(filepath,"../_libs/nvnlib/classes/auto/py")+'\n')
pathfile.append("import sys; new=sys.path[sys.__plen:]; del sys.path[sys.__plen:]; p=getattr(sys,'__egginsert',0); sys.path[p:p]=new; sys.__egginsert = p+len(new)\n")

CALL("sudo chmod -R 777 %s"%pythonpackagepath)
filepath = os.path.join(pythonpackagepath,"PTlib.pth")

savefile(filepath,lines2buf(pathfile))

