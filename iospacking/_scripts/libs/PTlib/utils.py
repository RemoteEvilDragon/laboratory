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
import md5
import json
import glob
import hashlib
import os,sys
from xml.etree import ElementTree
from ftplib import FTP
import zipfile
import socket
import struct
import binascii 
import filecmp 
# from PIL import Image 

reload(sys)
sys.setdefaultencoding('utf-8')

filepath = sys.path[0]
sys.path.append(os.path.join(filepath,"../thrift"))

from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport

USE_LOG = True
LINE_WIDTH = 120
charHeader = ' '
stepSplit = '_'
logheaderlen = 0

def getArg(index):
	argCount = len(sys.argv)
	return sys.argv[index] if index < argCount else "NULL"

def pressAnyKey():
	x = raw_input("press any key to close")
	exit(0) 



def LOG_B():
	global logheaderlen
	logheaderlen = logheaderlen + 2

def LOG_E():
	global logheaderlen
	logheaderlen = logheaderlen - 2

def LOG_(astr):
	global logheaderlen
	print "" +charHeader * logheaderlen + " " + astr

def LOG_ERR_H(e = False):
	print "+" * 100
	if e:
		exit(1)

def LOG_ERR(astr, border = True):
	global logheaderlen
	if border:
		print "+" * 100
	print "+ !!! ERROR !!! " +  astr
	if border:
		print "+" * 100
	if border:
		exit(1)

def LOG_WORN(astr, border = True):
	global logheaderlen
	# if border:
	# 	print "+" * 100
	print "+ --- WORNING --- " +  astr
	# if border:
	# 	print "+" * 100

def Log(on):
	USE_LOG = on

def LOG(str):
	if not USE_LOG :
		return
	space = 12
	# print '-'*140
	print "" +charHeader * space+" " + str
def LOGS(str):
	if not USE_LOG :
		return 
	space = 12
	print "" +charHeader * space+" " + str
def LOGERR(str):
	if not USE_LOG :
		return 
	# print '-'*140
	space = 12
	print "" +charHeader * space+"!!! " + str
	# print ''
def LOGSTEP(step , name):
	if not USE_LOG :
		return 
	space = 4
	print '' +stepSplit*LINE_WIDTH +'\n'
	print '' +charHeader * space+' step %d : %s'%(step,name)
	# print '*'*140 

def LOGCHANNEL(step , name):
	if not USE_LOG :
		return 
	space = 1
	print '' +stepSplit*LINE_WIDTH +'\n'
	print '' +charHeader * space+' channel %d : %s'%(step,name)
	# print '*'*140 



def LOGSUBSTEP(name):
	if not USE_LOG :
		return 
	space = 8
	print '' +stepSplit*LINE_WIDTH+'\n'
	print '' +charHeader * space+' %s'%(name)
	# print '-'*140
	print ''

def LOGSTEPEND():
	if not USE_LOG :
		return 
	print '' +charHeader*LINE_WIDTH

def CALL(cmd):
	p=subprocess.Popen(cmd, shell=True)  
	a = p.wait()
	if a != 0 :
		LOGERR("An error occured when call command : %s , STOPPED!!!"%cmd)
		exit(1)
	return 0
	
def GET_MACRO_DEF(key,level,k):
	key = key.replace('/','_')
	key = key.replace('.','_')
	key = key.replace('-','_')
	key = key.replace('\\','_')
	key = key.replace(' ','_')
	key = key.replace("'",'_')
	key = key.upper()
	macro = '#define    %s%-50s "%s"\n'%("        " * (level+1), key , k)
	return macro

def GET_LUA_DEF(key,level,k):
	key = key.replace('/','_')
	key = key.replace('.','_')
	key = key.replace('-','_')
	key = key.replace('\\','_')
	key = key.replace(' ','_')
	key = key.replace("'",'_')
	key = key.upper()
	macro = '%s%s = "%s"\n'%("        " * (level+1), key , k)
	return macro

def getPlistValue(resfile , tree):
	# print resfile,tree
	if not os.path.exists(resfile):
	    LOGERR("File not exists : " + resfile)


	pl = plistlib.readPlist(resfile)

	for i in tree:
		if i == 'Root':
			continue
		if pl.has_key(i):
			pl = pl[i]
		else:
			return False , None
	return True , pl

def exportResDefPath(out,outlist,outlua ,path,rootPath,level):
	files = os.listdir(path)
	# print files
	for f in files:
		fs = path+'/'+f
		if not '.DS_Store' == f:
			relPath = os.path.relpath(fs,rootPath)
			# relPathname = relPath.replace('.','_')
			# relPathname = relPathname.replace(' ','_')
			# relPathname = relPathname.replace('/','_')
			# relPathname = relPathname.replace('\\','_')
			# relPathname = relPathname.replace('-','_')
			# relPathname = relPathname.upper()
#			relPath = relPath.replace('/','//')
			relPathname = relPath
			if os.path.isfile(fs):
				relPathname = 'FILE_'+relPathname
			else:
				relPathname = 'DIR_'+relPathname

			macro = GET_MACRO_DEF(relPathname,level,relPath)#'#define    %s%-50s "%s"\n'%("        " * level,relPathname , relPath)
				
			out.write(macro)
			luamacro = GET_LUA_DEF(relPathname,level,relPath)
			outlua.write(luamacro)
			# out.write('\n')
			
			if os.path.isfile(fs):
				outlist.write(relPath)
				outlist.write('\n')
			else:
				outlist.write('### ' + relPath)
				outlist.write('\n')

			fileBaseName = os.path.basename(fs)
			#材质资源，解析所有的frame
			if '.PLIST' in fs.upper() :
				#解析所有frame
				ok , frames = getPlistValue(fs,['Root','frames'])
				# print frames
				if ok :
					for (k,v) in frames.items():
						frameName = 'FRAME_'+k.upper()
						macro = GET_MACRO_DEF(frameName,level+1,k) #'#define    %s%-50s "%s"\n'%("        " * (level+1), frameName , k)
						out.write(macro)
						luamacro = GET_LUA_DEF(frameName,level+1,k)
						outlua.write(luamacro)

			#疑似菜单文件，解析所有动画
			if '.EXPORTJSON' in fs.upper() :
				# LOG(fs)
				f = file(fs);
				s = json.load(f)
				if s.has_key("animation"):
					animations = s["animation"]
					if animations.has_key("actionlist"):
						actionlist = animations["actionlist"]
						for action in actionlist:
							macro = GET_MACRO_DEF(fileBaseName+"_UIANIM_"+action["name"],level+1,action["name"])
							out.write(macro)
							luamacro = GET_LUA_DEF(fileBaseName+"_UIANIM_"+action["name"],level+1,action["name"])
							outlua.write(luamacro)
			if '.JSON' in fs.upper() :
				# LOG(fs)
				anim = json.load(open(fs,'r'))
				if anim.has_key('animations') :
					anims = anim['animations']
					for k,v in anims.items():
						macro = GET_MACRO_DEF(fileBaseName+"_ACT_"+k,level+1,k)
						out.write(macro)
						luamacro = GET_LUA_DEF(fileBaseName+"_ACT_"+k,level+1,k)
						outlua.write(luamacro)


			#疑似动画文件，解析所有动作名
			# if '.EXPORTJSON' in fs.upper() :
			# 	f = file(fs);
			# 	s = json.load(f)
			# 	# 导出所有骨骼名
			# 	if s.has_key("armature_data"):
			# 		armaturedata = s["armature_data"]
			# 		for ad in armaturedata:
			# 			bones = ad["bone_data"]
			# 			for bd in bones:
			# 				name = bd["name"]
			# 				macro = GET_MACRO_DEF(fileBaseName+"_BONE_"+name,level+1,name)
			# 				out.write(macro)
			# 	#导出所有动作名
			# 	if s.has_key("animation_data"):
			# 		animationdata = s["animation_data"]
			# 		for ad in animationdata:
			# 			# print ad
			# 			movs = ad["mov_data"]
			# 			for m in movs:
			# 				name = m["name"]
			# 				macro = GET_MACRO_DEF(fileBaseName+"_ACTION_"+name,level+1,name)
			# 				out.write(macro)
			# if '.XML' in fs.upper():
			# 	root = ElementTree.parse(fs)
			# 	node_findall = root.findall("armatures/armature/b")
			# 	for b in node_findall:
			# 		name = b.attrib["name"]
			# 		macro = GET_MACRO_DEF(fileBaseName+"_BONE_"+name,level+1,name)
			# 		out.write(macro)

			# 	node_findall = root.findall("animations/animation/mov")
			# 	for m in node_findall:
			# 		name = m.attrib["name"]
			# 		macro = GET_MACRO_DEF(fileBaseName+"_ACTION_"+name,level+1,name)
			# 		out.write(macro)





		
		if not os.path.isfile(fs) and not '.DS_Store' == f:
			exportResDefPath(out,outlist,outlua,fs,rootPath,level+1)

def exportResDef(datadir , srcdir , ex = ""):
	# LOG(datadir)
	# LOG(srcdir)
	if not os.path.exists(srcdir):
		os.makedirs(srcdir)


	outlist = open(srcdir + '/RESLIST'+ ex +'.txt','w')
	out = open(srcdir + '/NEW_RESDEF'+ ex +'.h','w')
	if not os.path.exists(srcdir+'/lua'):
		os.makedirs(srcdir+'/lua')
	outlua = open(srcdir + '/lua/RESDEF'+ ex +'.lua','w')

	out.write('#pragma once\r')
	# outlua.write('RESDEFS = {')
	exportResDefPath(out,outlist,outlua,datadir,datadir,0)
	# outlua.write('}')
	out.close()
	outlist.close()
	outlua.close()
	
	f1 = srcdir + '/NEW_RESDEF'+ ex +'.h'
	f2 = srcdir + '/RESDEF'+ ex +'.h'

	LOGSUBSTEP("generate res def file")
	LOG("out src dir : %s"%(srcdir))
	LOG("generate done : %s"%(f2))
	
	md51 = GetFileMd5(f1)
	md52 = GetFileMd5(f2)
	if md51 == md52:
		LOG('same res def file , ignore copy')
		# exit(0)
	else:
		# print f2
		# print md51
		# print md52
		CALL("cp -rf %s %s"%(f1,f2))
		# exit(0)
	f1f = open(f1,'r')
	# if not os.path.exists (f2) or not (md5.new(f1f.read()).digest() == md5.new(open(f2,'r').read()).digest()):
	# 	f1f.close()
	# 	CALL("cp -rf %s %s"%(f1,f2))

	# 	exit(0)
	# else:
	# 	LOG('same res def file , ignore copy')
	# 	exit(0)
	CALL("rm -rf %s"%(f1))


def processResFileDir(sdir , ddir , files , recursive):
	if not os.path.exists(ddir):
		os.makedirs(ddir)
	for f in files:
		src = os.path.join(sdir,f)

		if not os.path.exists(ddir):
			os.makedirs(ddir)

		cpycmd = "cp -rf %s %s"%(src,ddir)
		LOGS("copy %20s      -->      %s"%(f,ddir))
		fs = glob.glob(src)
		# print fs
		if len(fs) > 0:
			CALL(cpycmd)
		else:
			LOGS("there is NO file with ext : %s , so skipped !"%(f))

	if recursive :
		subfiles = os.listdir(sdir)
		for subfile in subfiles:
			subsdir = os.path.join(sdir,subfile)
			subddir = os.path.join(ddir,subfile)
			if not os.path.isdir(subsdir):
				continue
			if '.Dir' in subsdir:
				continue
			processResFileDir(subsdir,subddir, files,recursive)

def processResFile(resfile , packPng = False , ex = ""):
	# if len(sys.argv) >= 2:
	# 	resfile = os.path.join(filepath,sys.argv[1])
	filepath = os.path.dirname(os.path.abspath(resfile))

	if not os.path.exists(resfile):
	    LOGERR("File not exists : " + resfile)

	# with open(resfile, 'r') as f:
	# 	data = f.read()
	# 	# r = re.compile('[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]')
	# 	# data = r.sub("",data)
	# 	pl = plistlib.readPlistFromString(data)

	pl = plistlib.readPlist(resfile)

	#获得root路径

	if pl.has_key("root"):
		root = pl['root']
		rootsrcdir = os.path.join(filepath,root["srcdir"])
		LOG("root src dir : %s"%rootsrcdir)
		if not os.path.exists(rootsrcdir):
			LOGERR("Dir Not Exists : %s , STOPPED!!!"%rootsrcdir)
			sys.exit(1)

		rootdstdir = os.path.join(filepath,root["dstdir"])
		rootoutsrcdir = os.path.join(filepath,root["outsrcdir"])
		# LOG("rootoutsrcdir : %s"%rootoutsrcdir)

		realrootdstdir = rootdstdir
		if packPng :
			rootdstdir = rootdstdir+"_tmp";
			CALL("rm -rf %s"%(rootdstdir))

		LOG("root dst dir : %s"%realrootdstdir)

		
		# if clean :
		# 	CALL("rm -rf %s"%rootdstdir)
		# 	return
		if not os.path.exists(rootdstdir):
			os.makedirs(rootdstdir)

	items = pl['items']

	for i in items:
		sdir = i["srcdir"]
		sdir = os.path.join(rootsrcdir,sdir)
		ddir = i["dstdir"]
		ddir = os.path.join(rootdstdir,ddir)
		LOG("process dir %s"%sdir)

		cmd=""
		if i.has_key("cmd"):
			cmd = i["cmd"]
		files = i["files"]
		# print files
		recursive = False
		if i.has_key("recursive"):
			recursive = i["recursive"]

		

		if cmd != "":
			cmdfile = os.path.join(sdir,cmd)
			if not os.path.exists(cmdfile):
				LOGS("cmd file %s not exists ,skipped !!!"%cmdfile)
			else:
				os.chdir(sdir)
				CALL("python %s %s %s"%(cmd,rootdstdir,rootoutsrcdir))	
				os.chdir(filepath)

		processResFileDir(sdir,ddir,files,recursive)

		# if cmd != "":
		# 	cmdfile = os.path.join(sdir,cmd)
		# 	if not os.path.exists(cmdfile):
		# 		LOGS("cmd file %s not exists ,skipped !!!"%cmdfile)
		# 	else:
		# 		os.chdir(sdir)
		# 		CALL("python %s %s %s"%(cmd,rootdstdir,rootoutsrcdir))	
		# 		os.chdir(filepath)

		# for f in files:
		# 	src = os.path.join(sdir,f)

		# 	if not os.path.exists(ddir):
		# 		os.makedirs(ddir)

		# 	cpycmd = "cp -rf %s %s"%(src,ddir)
		# 	LOGS("copy %20s      -->      %s"%(f,ddir))
		# 	fs = glob.glob(src)
		# 	# print fs
		# 	if len(fs) > 0:
		# 		CALL(cpycmd)
		# 	else:
		# 		LOGS("there is NO file with ext : %s , so skipped !"%(f))


	exportResDef(rootdstdir,rootoutsrcdir,ex)
	if packPng :
		# packpng

		if not os.path.exists(realrootdstdir):
			os.makedirs(realrootdstdir) 
		# LOG("rootdstdir : %s"%rootdstdir)
		# LOG("realrootdstdir : %s"%realrootdstdir)
		CALL("cp -rf %s/* %s"%(rootdstdir,realrootdstdir))
		CALL("rm -rf %s"%(rootdstdir))

def getFilesWithExt(rootpath,ext,r=True):

	if not os.path.exists(rootpath):
		return []
	files = os.listdir(rootpath)
	# print files
	outfiles = []

	for f in files:
		fs = os.path.join(rootpath,f)

		if os.path.isfile(fs):
			fileext = os.path.splitext(fs)[-1]
			if fileext == ext or ext == "":
				outfiles.append(fs)
		else:
			if r :
				subfiles = getFilesWithExt(fs,ext,r)
				outfiles.extend(subfiles)

			# print outfiles

	return outfiles

def getSubDirs(rootpath):

	if not os.path.exists(rootpath):
		return []
	files = os.listdir(rootpath)
	# print files
	outfiles = []

	for f in files:
		fs = os.path.join(rootpath,f)

		if os.path.isfile(fs):
			pass
		else:
			outfiles.append(fs)

			# print outfiles

	return outfiles

def w2u(filepath):
	f = open(filepath, 'r') 
	lines = f.readlines()  
	f.close()

	f = open(filepath, 'w') 
	for i in lines:
		f.write(i)
	f.close()

def w2uForPath(apath):
	files = getFilesWithExt(apath,"")
	for i in files:
		w2u(i)

def fixLua(filepath,defaults = None,includes = None):
	# print (filepath)
	f = open(filepath, 'r') 
	lines = f.readlines()  
	f.close()

	inNew = False
	requiredend = False
	f = open(filepath, 'w') 
	crtStruct = ""
	moduleadded=False
	for i in lines:
		x = i.strip()
		if len(x)>1 and x[-1] == "=":
			f.write("-- "+i)
			continue
		astr = i 
		if "writeListBegin" in astr:
			astr = astr.replace("string.len"," getListSize ")
		if "writeMapBegin" in astr:
			astr = astr.replace("string.len"," getMapSize ")
		if "writeSetBegin" in astr:
			astr = astr.replace("string.len"," getSetSize ")

		if 'package.seeall' in astr:
			moduleadded = True

		if "Request = __TObject:new{" == astr.strip() and not moduleadded:
			# filaname = os.path.basename(filepath).replace(".lua",'')
			# astr = 'module("%s",package.seeall)\n'%(filaname) + astr
			pass

		if "_key" in astr and "iprot:read" in astr and not "local" in astr:
			astr = astr.replace("_key", "local _key")

		if "_val" in astr and "iprot:read" in astr and not "local" in astr:
			astr = astr.replace("_val", "local _val")

		if "_val" in astr and "= {}" in astr and not "local" in astr:
			astr = astr.replace("_val", "local _val")

		if "_val" in astr and "new" in astr and not "local" in astr:
			astr = astr.replace("_val", "local _val")

		if "_elem" in astr and "new{}" in astr and not "local" in astr:
			astr = astr.replace("_elem", "local _elem")
			
		if "_elem" in astr and "iprot:read" in astr and not "local" in astr:
			astr = astr.replace("_elem", "local _elem")

		if "_elem" in astr and "= {}" in astr and not "local" in astr:
			astr = astr.replace("_elem", "local _elem")

		if astr.strip() == '}' and inNew :
			inNew = False
		if inNew and astr.strip() != "" and not "nil" in astr and not "=" in astr:
			withdh = ',' in astr
			astr = astr.replace(',','')
			astr = astr.replace('\r','')
			astr = astr.replace('\n','')
			if defaults == None:
				astr = '  '+astr + ' = nil'
			else:
				astr = astr.strip()
				# thriftfilename = os.path.basename(filepath)
				# thriftfilename = thriftfilename.replace('_ttypes.lua','')
				key = crtStruct +'.'+astr
				# print defaults
				# print key
				if defaults.has_key(key):
					defaultvalue = str(defaults[key])
					astr = '  '+astr + ' = ' + defaultvalue
				else:
					astr = '  '+astr + ' = nil'
				# print thriftfilename
			if withdh :
				astr = astr + ',\n'
			else:
				astr = astr + '\n'

		if "__TObject:new{" in astr:
			inNew = True
			classname = astr.replace("__TObject:new{",'')
			classname = classname.replace("=",'')
			crtStruct = classname.strip()
			astr = astr + '\n\t __thriftClass = "%s",\n'%crtStruct

		if requiredend and not "require" in astr:
			requiredend = False
			if includes :
				thriftfilename = os.path.basename(filepath)
				thriftfilename = thriftfilename.replace('_ttypes.lua','')
				if includes.has_key(thriftfilename):
					files = includes[thriftfilename]
					if files:
						for afile in files:
							areq = 'require "%s_ttypes"\n'%(afile)
							f.write(areq)

		if "require" in astr:
			requiredend = True


		f.write(astr)
	# f.write('-- eof\r\n')
	# f.write('\r\n')
	f.close()

	# print match


def fixLuaForPath(apath,globalDefaultValues=None,globalIncludeFiles = None):
	files = getFilesWithExt(apath,".lua")
	for i in files:
		fixLua(i,globalDefaultValues,globalIncludeFiles)

def serialize(thrift_object,file,protocol_factory=TBinaryProtocol.TBinaryProtocolFactory()):
	filepath = os.path.dirname(file)
	if not os.path.exists(filepath):
		os.makedirs(filepath)
	fileHandle = open ( file , 'w' )
	transport = TTransport.TFileObjectTransport(fileHandle)
	protocol = protocol_factory.getProtocol(transport)
	thrift_object.write(protocol)


def deserialize(base,file,protocol_factory=TBinaryProtocol.TBinaryProtocolFactory()):
	fileHandle = open ( file, 'r' )
	transport = TTransport.TFileObjectTransport(fileHandle)
	protocol = protocol_factory.getProtocol(transport)
	base.read(protocol)
	return base

def readXlsTable(xlspath):
	tables = {}
	wb = xlrd.open_workbook(xlspath)
	iCount = len(wb.sheets())
	# LOG('sheet count : %d'%iCount)
	sheets = wb.sheets()

	#


	for sheet in sheets:

		ids = {}
		idNames = []
		foundIds = False
		idRow = 0 
		table = {}
		table['name'] = sheet.name
		for rownum in range(sheet.nrows):
			rowcells = sheet.row_values(rownum)
			for i in range(len(rowcells)):
				cell = rowcells[i]
				if not cell == '':
					foundIds = True
					idRow = rownum
				if foundIds and (not cell == '') :
					ids[cell] = i
					idNames.append(cell)
			if foundIds:
				break


		# print idNames
		table['colNames'] = idNames
		rows = []
		for rownum in range(idRow + 1 ,sheet.nrows) :
			rowcells = sheet.row_values(rownum)
			arow = {}
			comment = False
			for (k,v) in ids.items():
				cell = rowcells[v]
				if '###' in str(cell):
					comment = True
					break
				arow[k] = cell
			if not comment:
				rows.append(arow)
		table['rows'] = rows

		tables[sheet.name] = table


	return tables


def readMultiTable(xlspath):
	groups = {}
	wb = xlrd.open_workbook(xlspath)
	iCount = len(wb.sheets())
	sheets = wb.sheets()

	tableposes = {} 

	for sheet in sheets:
		tablegroup = {}
		for rownum in range(sheet.nrows):
			rowcells = sheet.row_values(rownum)
			for i in range(len(rowcells)):
				if rowcells[i] == "TABLE":
					name = rowcells[i+1]
					tableposes[name] = (rownum , i)

		# print tableposes

		for (tn,t) in tableposes.items():
			table = {}
			(row,col) = t
			colHeaders = {}
			rowcells = sheet.row_values(row + 1)
			index = 0
			valid = False
			# for colname in rowcells:
			for colidx in range(col,len(rowcells)):
				colname = rowcells[colidx]
				if colname == "":
					if (valid):
						break
				else:
					valid = True
				colHeaders[colname] = col + index
				index = index + 1
			table["ColHeaders"] = colHeaders
			# print colHeaders
			rows = []
			for rownum in range(row + 2 , sheet.nrows):
				rowcells = sheet.row_values(rownum)
				if '#' in rowcells[col-1]:
					continue
				row = {}
				valid = False
				for (n,idx) in colHeaders.items():
					# print rowcells
					# print n,idx
					valid = valid or rowcells[idx] != "" 
					row[n] = rowcells[idx]
				if not valid :
					break
				rows.append(row)
			table["Rows"] = rows
			table['Name'] = tn

			tablegroup[tn] = table

		groups[sheet.name] = tablegroup

	# print groups
	return groups

def readThriftTable(xlspath):
	groups = {}
	wb = xlrd.open_workbook(xlspath)
	iCount = len(wb.sheets())
	sheets = wb.sheets()

	# tableposes = {} 
	# tableTypes = {}
	for sheet in sheets:
		tableposes = {} 
		tableTypes = {}
		# print sheet.name
		tablegroup = {}
		for rownum in range(sheet.nrows):
			rowcells = sheet.row_values(rownum)
			for i in range(len(rowcells)):
				if rowcells[i] == "{}":
					name = rowcells[i+1]
					tableposes[name] = (rownum , i)
					atype = rowcells[i+3]
					tableTypes[name] = atype

		# print tableposes
		tablenames = []
		# print  tablenames
		for (tn,t) in tableposes.items():
			table = {}
			table["type"] = tableTypes[tn]
			tablenames.append(tn)
			# print "append",tablenames
			if table["type"] == 'ENUM':
				(row,col) = t
				enumids = sheet.row_values(row + 1)
				enumvalues = sheet.row_values(row + 2)
				valid = False
				enumdata = {}
				for colidx in range(col+1,len(enumids)):
					colname = enumids[colidx]
					val = enumvalues[colidx]
					if colname == "":
						if (valid):
							break
					else:
						valid = True
					enumdata[colname] = val
				table['Name'] = tn
				table['ENUM'] = enumdata
				tablegroup[tn] = table
			else:
				(row,col) = t
				colHeaders = {}
				colHeaderInfos = {}
				rowcellindexes = sheet.row_values(row + 1)
				rowcells = sheet.row_values(row + 2)
				rowcellTypes = sheet.row_values(row + 3)
				rowcellDefaults = sheet.row_values(row + 4)
				rowcellComments = sheet.row_values(row + 5)
				index = 0
				valid = False
				colnames = []
				# for colname in rowcells:
				for colidx in range(col+1,len(rowcells)):
					colname = rowcells[colidx]
					if colname == "":
						if (valid):
							break
					else:
						valid = True
					colHeaders[colname] = col + 1 + index
					colnames.append(colname)
					colHeaderInfos[colname] = {"type":rowcellTypes[colidx],"comment":rowcellComments[colidx],"default":rowcellDefaults[colidx],"index":rowcellindexes[colidx]}
					index = index + 1
				table["ColHeaders"] = colHeaders
				table["colHeaderInfos"] = colHeaderInfos
				table["colnames"] = colnames
				# print colHeaders
				rows = []
				for rownum in range(row + 6 , sheet.nrows):
					rowcells = sheet.row_values(rownum)
					if '#' in rowcells[col-1]:
						continue
					row = {}
					valid = False
					for (n,idx) in colHeaders.items():
						# print rowcells
						# print n,idx
						valid = valid or rowcells[idx] != "" 
						row[n] = rowcells[idx]
					if not valid :
						break
					rows.append(row)
				table["Rows"] = rows
				table['Name'] = tn

				tablegroup[tn] = table

		tablegroup["nameindexes"] = tablenames
		# print sheet.name,tablenames
		groups[sheet.name] = tablegroup


	# print groups
	return groups

def readbinfile(file):
	res = ""
	fh = open(file,'rb')
	res = fh.read()
	return res

def readfile(file):
	res = ""
	for line in open(file):
		res = res+line
	return res

def readfileToList(file):
	res = []
	for line in open(file):
		res.append(line)
	return res

def savefile(file , buf):
	path = os.path.dirname(file)
	if not os.path.exists(path):
		os.makedirs(path)
	fileHandle = open ( file, 'w' ) 
	fileHandle.write ( buf ) 
	fileHandle.close() 


def lines2buf(lines):
	res = ""
	for line in lines:
		res = res + line
	return res

#大文件的MD5值
def GetFileMd5(filename):

	if not os.path.exists(filename):
		return "FILE_NOT_EXISTS"


	if not os.path.isfile(filename):
		return "NOT FILE"

	myhash = hashlib.md5()
	f = file(filename,'rb')
	while True:
		b = f.read(8096)
		if not b :
			break
		myhash.update(b)
	f.close()
	return myhash.hexdigest()


#简单的测试一个字符串的MD5值
def GetStrMd5(src):
    m0=hashlib.md5()
    m0.update(src)
    return  m0.hexdigest()


def ftp_download(host , port , user , password , filedir , filename , tmpfile): 

    ftp=FTP() 
    ftp.set_debuglevel(0) 
    ftp.connect(host,str(port)) 
    ftp.login(user,password) 
    #print ftp.getwelcome()#显示ftp服务器欢迎信息 
    ftp.cwd(filedir) #选择操作目录 
    files = ftp.nlst()
    # print files 
    if not os.path.basename(filename) in files:
    	LOG("FTP download error , NO FILE : %s"%(filename))
        return
    bufsize = 1024 
    file_handler = open(tmpfile,'wb') #以写模式在本地打开文件 
    ftp.retrbinary('RETR %s' % os.path.basename(filename),file_handler.write,bufsize)#接收服务器上文件并写入本地文件 
    ftp.set_debuglevel(0) 
    file_handler.close() 
    ftp.quit() 
    LOG("FTP download %s OK"%(filename))

def zipDir(dirname,zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        #print arcname
        zf.write(tar,arcname)
    zf.close()


def unzip(zip_path,save_path):
	zipfile.ZipFile(zip_path).extractall(save_path)

def getAllFile(resPath):
	res =[]
	for root, dirs, files in os.walk(resPath):
		for name in files:
			if '.DS_Store' in name:
				continue
			newfile = os.path.join(root, name)
			relPath = newfile.replace(resPath + '/','')	
			relPath = relPath.replace(resPath,'')	
			res.append(relPath)
	return res

def getFileCRC(_path): 
    try: 
        blocksize = 1024 * 64 
        f = open(_path,"rb") 
        str = f.read(blocksize) 
        crc = 0 
        while(len(str) != 0): 
            crc = binascii.crc32(str, crc) 
            str = f.read(blocksize) 
        f.close() 
    except: 
        print 'get file crc error!' 
        return 0 
    return crc 

def getPathDiff(basePath, resPath):
	# print resPath
	difffiles = []

	files = getAllFile(resPath)
	for f in files:
		basefile = os.path.join(basePath, f)
		newfile = os.path.join(resPath, f)
		diff = True
		if os.path.exists(basefile):
			basemd5 = GetFileMd5(basefile);
			newmd5 = GetFileMd5(newfile);
			diff = basemd5 != newmd5
			# diff = filecmp.cmp(basefile,newfile)
			if diff :
				LOG(basefile)
				LOG("basemd5 = %s"%(basemd5))
				LOG("newmd5 = %s"%(newmd5))
			# LOG("exists base file : %s "%(basefile))
		else:
			LOG("base file : %s not exists"%(basefile))
			pass
		if diff:
			difffiles.append(f)
	return difffiles

# def splitPlistFrames(plistfile , imagefile ,outdir , scale = 1):
# 	# plistfile = os.path.join(outdir,'plist')
# 	tgtfile = imagefile
# 	if os.path.exists(tgtfile):
# 		pl = plistlib.readPlist(plistfile)
# 		frames = pl['frames']
# 		img = Image.open(tgtfile)

# 		for key,val in frames.items():
# 			frame = val['frame']
# 			frame = frame.replace('{','')
# 			frame = frame.replace('}','')
# 			xywh = frame.split(',')
# 			x = (int)(xywh[0])
# 			y = (int)(xywh[1])
# 			w = (int)(xywh[2])
# 			h = (int)(xywh[3])
# 			box = (x,y,x+w,y+h)
# 			rotated = val['rotated']
# 			if rotated:
# 				box = (x,y,x+h,y+w)
# 			region = img.crop(box)
# 			if rotated:
# 				region = region.transpose(Image.ROTATE_90)
# 			if scale != 1 :
# 				w , h = region.size
# 				region = region.resize((int(w*scale),int(h*scale)))
# 			framepath = os.path.join(outdir,key)
# 			framedirpath = os.path.dirname(framepath)
# 			if not os.path.exists(framedirpath):
# 				os.makedirs(framedirpath)
# 			region.save(framepath)


def IsOpen(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,int(port)))
        s.shutdown(2)
        print '%d is open' % port
        return True
    except:
        print '%d is down' % port
        return False

_DELTA = 0x9E3779B9  
  
def _long2str(v, w):  
    n = (len(v) - 1) << 2  
    if w:  
        m = v[-1]  
        if (m < n - 3) or (m > n): return ''  
        n = m  
    s = struct.pack('<%iL' % len(v), *v)  
    return s[0:n] if w else s  
  
def _str2long(s, w):  
    n = len(s)  
    m = (4 - (n & 3) & 3) + n  
    s = s.ljust(m, "\0")  
    v = list(struct.unpack('<%iL' % (m >> 2), s))  
    if w: v.append(n)  
    return v  
  
def encrypt(str, key):  
    if str == '': return str  
    v = _str2long(str, True)  
    k = _str2long(key.ljust(16, "\0"), False)  
    n = len(v) - 1  
    z = v[n]  
    y = v[0]  
    sum = 0  
    q = 6 + 52 // (n + 1)  
    while q > 0:  
        sum = (sum + _DELTA) & 0xffffffff  
        e = sum >> 2 & 3  
        for p in xrange(n):  
            y = v[p + 1]  
            v[p] = (v[p] + ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[p & 3 ^ e] ^ z))) & 0xffffffff  
            z = v[p]  
        y = v[0]  
        v[n] = (v[n] + ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[n & 3 ^ e] ^ z))) & 0xffffffff  
        z = v[n]  
        q -= 1  
    return _long2str(v, False)  
  
def decrypt(str, key):  
    if str == '': return str  
    v = _str2long(str, False)  
    k = _str2long(key.ljust(16, "\0"), False)  
    n = len(v) - 1  
    z = v[n]  
    y = v[0]  
    q = 6 + 52 // (n + 1)  
    sum = (q * _DELTA) & 0xffffffff  
    while (sum != 0):  
        e = sum >> 2 & 3  
        for p in xrange(n, 0, -1):  
            z = v[p - 1]  
            v[p] = (v[p] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[p & 3 ^ e] ^ z))) & 0xffffffff  
            y = v[p]  
        z = v[n]  
        v[0] = (v[0] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[0 & 3 ^ e] ^ z))) & 0xffffffff  
        y = v[0]  
        sum = (sum - _DELTA) & 0xffffffff  
    return _long2str(v, True)  

def LOG_FMT(obj):
	# tmp = str(obj)
	# tmp = tmp.replace('(','{')
	# tmp = tmp.replace(')','}')
	# obj2 = eval(tmp)

	# print obj2
	jsonDumpsIndentStr = json.dumps(obj, indent=4);
	print jsonDumpsIndentStr

def List2Dict(obj,idname):
	res = {}
	for i in obj:
		res[i.get(idname)] = i
	return res
def wordMulti(astr):
	astr = astr.strip()
	if astr.endswith('y'):
		tmp = list(astr)
		tmp[-1] = 'i'
		astr = ''.join(tmp)
	if astr.endswith('a') or astr.endswith('e') or astr.endswith('i') or astr.endswith('o') or astr.endswith('u') :
		return astr + "es"
	return astr + 's'

def space(num):
	return ' '*num

def loadJson(filepath):
	try:
		res = json.load(file(filepath))
		return res
	except Exception, e:
		LOG_("读取json文件 %s 发生错误，请检查文件格式是否正确"%(filepath))
		raise
	else:
		pass
	finally:
		pass
	return None

	

def getSvnRevision(aDir):
	trunkpath = aDir
	os.chdir(trunkpath)
	CALL("svn info > tmp.txt")
	tmpfile = os.path.join(aDir,"tmp.txt") 
	tmpstr = readfile(tmpfile)
	# print tmpstr
	regex = r'Last Changed Rev: ([0-9]+)'
	match = re.findall( regex , tmpstr ) 
	# print match
	trunkversion = 0
	for a in match:
		trunkversion = a

	regex = r'^URL: ([^\n\r]*)'
	match = re.findall( regex , tmpstr ,re.MULTILINE) 
	# print match
	url = ""
	for a in match:
		url = a
	CALL("rm tmp.txt")
	return int(trunkversion) , url
	# pass
# if __name__ == "__main__":  
#     print decrypt(encrypt('Hello XXTEA!', '16bytelongstring'), '16bytelongstring') 



