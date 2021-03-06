#!/usr/bin/env python
# -*- coding: utf8 -*-


#2.generate corresponding json files
import json
import os
import io
import shutil
from hashlib import md5

projectPath = "/Users/putao/Desktop/Logis"
ignoreList=[".DS_Store"]
importList=["src","res"]

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

				v_dict = dict()
				v_dict["downloadState"] = 0
				v_dict["md5"] = m.hexdigest()
				_dict[key] = v_dict
			elif os.path.isdir(fpath):
				generateMd5(fpath,_dict)

version_manifest = {
	"packageUrl":"http://27.126.181.90:10000/update/files/",
	"remoteVersionUrl":"http://27.126.181.90:10000/update/version/version.manifest",
	"remoteManifestUrl":"http://27.126.181.90:10000/update/version/project.manifest",
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

os.chdir(projectPath)

#输出project.manifest文件
json_str = json.dumps(project_manifest)
with io.open(os.path.join(projectPath,"src/version/project.manifest"),"w",encoding='utf-8') as f:
	f.write(unicode(json_str))


