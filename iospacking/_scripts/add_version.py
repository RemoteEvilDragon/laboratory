import os
import platform
import sys
import filecmp 
import shutil
import pickle
import plistlib
import re

reload(sys)
sys.setdefaultencoding('utf-8')
filepath = sys.path[0]

from PTlib.utils import *

versionpickle = os.path.join(filepath,"../VERSION")
with open(versionpickle, 'rb') as f:
	version = pickle.load(f) 

versionvalue = (version["version.1"]) * 100 + (version["version.2"]) * 10 +(version["version.3"])
versionvalue = versionvalue + 1
v1 = int(versionvalue / 100)
v2 = int((versionvalue-(v1*100)) / 10)
v3 = int(versionvalue - (v1*100) - (v2*10))

version["version.1"] = (v1)
version["version.2"] = (v2)
version["version.3"] = (v3)
versionstr = str(version["version.1"])+'.'+str(version["version.2"])+'.'+str(version["version.3"])

print "...update ios version"

infoplistdir = "../../../Bandari/insect/frameworks/runtime-src/proj.ios_mac"
files = os.listdir(infoplistdir)
for f in files:
	ds = infoplistdir+'/'+f
	if os.path.isfile(ds) :
		continue
	files2 = os.listdir(ds)

	for f2 in files2:
		fs = ds+'/'+f2
	
		if "Info.plist" in fs:
			# LOG(fs)
			info = plistlib.readPlist(fs)

			info['CFBundleShortVersionString']=versionstr
			info['CFBundleVersion']=versionstr

			plistlib.writePlist(info, fs)


print "...update ios done"

# print "...update android version"

# androidPath = os.path.join(filepath,"android/projects")
# files = os.listdir(androidPath)
# for f in files:
# 	ds = androidPath+'/'+f
# 	if os.path.isfile(ds) :
# 		continue
# 	files2 = os.listdir(ds)

# 	for f2 in files2:
# 		fs = ds+'/'+f2
	
# 		if "AndroidManifest.xml" in fs:
# 			# LOG(fs)
# 			lines = readfile(fs)
# 			regex = r'(android\:versionCode\=\".*?\")'

# 			match = re.findall( regex , lines ) 
# 			for a in match:
# 				regex = a
# 				tgt = 'android:versionCode="%d"'%(versionvalue)
# 				# result = re.sub(regex, newstring, lines)
# 				LOG("replace %s -> %s"%(regex,tgt))
# 				lines = lines.replace(regex,tgt)

# 			regex = r'(android\:versionName\=\".*?\")'
# 			match = re.findall( regex , lines ) 
# 			for a in match:
# 				regex = a
# 				tgt = 'android:versionName="%s"'%(versionstr)
# 				# result = re.sub(regex, newstring, lines)
# 				LOG("replace %s -> %s"%(regex,tgt))
# 				lines = lines.replace(regex,tgt)

# 			savefile(fs,lines)


# print "...update version.lua"

# versionhpppath = os.path.join(filepath,"../_master_src/script/version.lua")
# f=open(versionhpppath,'w')
# # f.write("#ifndef _version_hpp\n")
# # f.write("#define _version_hpp\n")
# defstr = "APP_VERSION " + '="' + versionstr + '"\n'
# f.write(defstr)
# # f.write("#endif\n")
# f.close()

# versionhpppath = os.path.join(filepath,"../_master_src/client/version.h")
# f=open(versionhpppath,'w')
# f.write("#ifndef _version_hpp\n")
# f.write("#define _version_hpp\n")
# defstr = '#define APP_VERSION "' + versionstr + '"\n'
# f.write(defstr)
# f.write("#endif\n")
# f.close()

# print "...update version.lua done"

print version
with open(versionpickle, 'wb') as f:
	pickle.dump(version, f)

# updatepackinfo = os.path.join(filepath,"ios/updatePackBaseInfo.plist")
# upbase = plistlib.readPlist(updatepackinfo)
# upbase["LockRelease"] = False
# plistlib.writePlist(upbase,updatepackinfo)


