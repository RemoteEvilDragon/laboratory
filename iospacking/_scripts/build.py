#coding=utf-8
import os
import platform
import sys
import filecmp
import time
import shutil
import pickle
from shutil import rmtree
import zipfile
from ftplib import FTP
import json
import subprocess
# from biplist import * 

reload(sys)
sys.setdefaultencoding('utf-8')
filepath = sys.path[0]
# sys.path.append(os.path.join(filepath,"../../../../../nvnlib/_tools/script"))

from PTlib.utils import *


is_Release_InHouse = False
# is_Release_InHouse = True

# 首先读取配置文件
if not is_Release_InHouse:
	configFilePath = os.path.join(filepath,'build_config.json')
else:
	configFilePath = os.path.join(filepath,'build_config_InHouse.json')

print('读取打包配置文件: '+configFilePath)
config = loadJson(configFilePath)
if config == None :
	exit(0)


# print(config)

ProvisioningProfile = config['ProvisioningProfile']
CodeSigningIdentity = config['CodeSigningIdentity']
ProjectPath = config['ProjectPath']
ProjectPath = os.path.join(filepath,ProjectPath)
_project_dir = os.path.dirname(ProjectPath)
Target = config['Target']
BuildType = 'Release'
ProjName = config['Name']


# 备份KeychainAccess.plist
kcaPlistPath = os.path.join(filepath,'../../../Bandari/insect/frameworks/runtime-src/proj.ios_mac/KeychainAccess.plist')

if not is_Release_InHouse:
	kcaPlistConfigPath = os.path.join(filepath,'keychain/KeychainAccess.plist')
else:
	kcaPlistConfigPath = os.path.join(filepath,'keychain/KeychainAccess_InHouse.plist')

# CALL("cp -rf %s %s"%(kcaPlistPath,kcaPlistBakPath))
CALL("cp -rf %s %s"%(kcaPlistConfigPath,kcaPlistPath))

strbuild = "xcodebuild -project \"%s\" -configuration \"%s\" -target \"%s\" CODE_SIGN_IDENTITY=\"%s\" PROVISIONING_PROFILE=\"%s\""%(ProjectPath,BuildType,Target,CodeSigningIdentity,ProvisioningProfile)
# print strbuild
CALL(strbuild)

appPath = os.path.join(_project_dir,"build/%s-iphoneos/%s.app"%(BuildType,Target))
ipaPath = os.path.join(_project_dir,"build/%s-iphoneos/%s.ipa"%(BuildType,Target))

versionpath = os.path.join(filepath,"../VERSION")
with open(versionpath, 'rb') as f:
	version = pickle.load(f)
versionstr = str(version["version.1"])+'.'+str(version["version.2"])+'.'+str(version["version.3"])

CALL("rm -rf " + ipaPath)
CALL('xcrun -sdk iphoneos PackageApplication -v "%s" -o "%s"'%(appPath , ipaPath))

releasePath = os.path.join(filepath,"../_VERSIONS_RELEASE/v%s/ios"%(versionstr))
releaseRootPath = os.path.join(filepath,"../_VERSIONS_RELEASE")
# CALL("rm -rf %s"%releaseRootPath)
CALL("rm -rf " + releasePath)
if not os.path.exists(releasePath):
	os.makedirs(releasePath)

nowtime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
ipaReleasePath = os.path.join(releasePath , "%s_%s_10000_%s.ipa"%(ProjName,versionstr,nowtime))
buildnum = "NULL"
if buildnum != "NULL" :
	ipaReleasePath = os.path.join(releasePath , "%s_v%s_b%s_%s.ipa"%(ProjName,versionstr,buildnum,nowtime))


CALL('cp -rf "%s" "%s"'%(ipaPath,ipaReleasePath))
LOGSUBSTEP("package %s done!"%ipaReleasePath)


# 上传FTP
# CALL("python upload_version.py")

exit(0)

