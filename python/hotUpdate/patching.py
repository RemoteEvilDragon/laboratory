#!/usr/bin/env python
# -*- coding: utf8 -*-


#2.generate corresponding json files
import json
import os
import io
import shutil
from hashlib import md5
import uploadToFtp

projectPath = "/Users/putao/Desktop/Logis"
ignoreList=[".DS_Store"]
importList=["src","res"]

newDir = "update"
os.mkdir(newDir)

os.chdir(newDir)
os.mkdir("files")
os.mkdir("version")
os.chdir("..")

def isIgnored(item):
	for s in ignoreList:
		if item == s:
			return True
	return False

def generateMd5(path,_dict):
	files = os.listdir(path)
	# print files
	for f in files:
		if not isIgnored(f):
			fpath = os.path.join(path,f)
			if os.path.isfile(fpath):
				m = md5()
				b_file = open(fpath,'rb')
				m.update(b_file.read())
				b_file.close()

				key = fpath[len(projectPath)+1:]
				# print key
				_dict[key] = m.hexdigest()
			elif os.path.isdir(fpath):
				generateMd5(fpath,_dict)

version_manifest = {
	"packageUrl":"http://27.126.181.90/update/files/",
	"remoteVersionUrl":"http://27.126.181.90/update/version/version.manifest",
	"remoteManifestUrl":"http://27.126.181.90/update/version/project.manifest",
	"version":"1.0.0",
	"engineVersion":"QUICK-COCOS2DX-COMMUNITY-3.6"}

project_manifest = dict()
for (k,v) in version_manifest.items():
	project_manifest[k]=v
project_manifest["assets"] = dict()

root_files = os.listdir(projectPath)
for f in root_files:
	if f=="src" or f =="res":
		generateMd5(os.path.join(projectPath,f),project_manifest["assets"])


os.chdir("/Users/putao/Desktop/laboratory/python/hotUpdate")
# 输出version.manifest文件

json_str = json.dumps(version_manifest)
with io.open("update/version/version.manifest","w",encoding='utf-8') as f:
	f.write(unicode(json_str))

#输出project.manifest文件
json_str = json.dumps(project_manifest)
with io.open("update/version/project.manifest","w",encoding='utf-8') as f:
	f.write(unicode(json_str))


dst=os.path.join(os.getcwd(),"update/files")
for path in importList:
	src=os.path.join(projectPath,path)
	shutil.copytree(src,dst+"/"+path)

uploadToFtp.upload(newDir)

print "Finshed file uploading,begin removing local Dirs now."
shutil.rmtree(newDir)
# os.removedirs(newDir)

