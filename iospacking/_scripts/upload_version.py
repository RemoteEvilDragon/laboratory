#!/usr/bin/python
#coding=utf-8
import sys
import os
import platform
import shutil
import xlrd
import string
import zipfile
import time
import pickle
import plistlib
import re
import subprocess

# build 一个 channel

reload(sys)
sys.setdefaultencoding('utf-8')
filepath = sys.path[0]

from PTlib.utils import *
from PTlib.xfer import *

versionpickle = os.path.join(filepath,"../VERSION")
with open(versionpickle, 'rb') as f:
	version = pickle.load(f) 
versionstr = str(version["version.1"])+'.'+str(version["version.2"])+'.'+str(version["version.3"])

configFilePath = os.path.join(filepath,'build_config.json')
print('读取打包配置文件: '+configFilePath)
config = loadJson(configFilePath)
if config == None :
	exit(0)
projName = config['Name']

# 上传../_VERSION_RELEASE中的版本到redmine服务器
releaseconfigpath = os.path.join(filepath,"release_config.json")
config = loadJson(releaseconfigpath)
ftpHost = config["Host"]
ftpPort = config["Port"]
ftpUser = config["User"]
ftpPass = config["Password"]

releasePath = os.path.join(filepath,"../_VERSIONS_RELEASE/v%s"%(versionstr))
remotePath = "%s/v%s"%(projName,versionstr)
# remotePath = "%s"%(projName)
xfer = Xfer()
xfer.setFtpParams(ftpHost, ftpUser, ftpPass,ftpPort)
files = xfer.lst()
# print files
# remoteNewPath = "%s/v%s_release"%(projName,versionstr)
# if remoteNewPath in files:
# 	LOG("已经存在版本 %s 的release版本，请检查！"%remotePath)
# 	# exit(0)
# 	remotePath = remoteNewPath
xfer.upload(releasePath,remotePath)














