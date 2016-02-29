#-*- coding:utf-8 -*-
import xlrd
import xml.etree.ElementTree as ET
import os
import shutil
import subprocess
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def CALL(cmd):
	p=subprocess.Popen(cmd, shell=True)  
	a = p.wait()
	if a != 0 :
		print ("An error occured when call command : %s , STOPPED!!!"%cmd)
		exit(1)
	return 0


CALL("cd ~/Desktop/project_bandari")
CALL("git pull")


def transfer(_file):
	output_file = ET.Element('Musics')
	book = xlrd.open_workbook(_file)
	sh = book.sheet_by_index(0)
	for rx in range(sh.nrows):
		if rx <= 1:
			pass
		else:
			subEle = ET.SubElement(output_file,'music')
			for cx in range(sh.ncols):
				value = sh.cell_value(rowx=rx, colx=cx)
				try:
					value = int(value)
				except ValueError:
					pass

				subEle.set(sh.cell_value(rowx=1, colx=cx),unicode(value).encode('utf8'))

	output_path = os.path.dirname(_file)+"/"+sh.name+".xml"
	print output_path

	ET.ElementTree(output_file).write(output_path,encoding="UTF-8",xml_declaration=True)
	subDirectory = os.path.basename(os.path.dirname(_file))
	shutil.copy(output_path,des_path+"/MusicConfig.xml")

root_path = os.path.join(os.getcwd(),"../../project_bandari/resource/res/dataConfigs/musicProperty")
root_path = os.path.abspath(root_path)

des_path = os.path.join(os.getcwd(),"../../Bandari/insect/res/config/musiConfig")
des_path = os.path.abspath(des_path)

for root,dirs,files in os.walk(root_path):
	for file in files:
		if file.endswith('xlsx'):
			path = os.path.join(root,file)
			print path
			transfer(path)

# copy these xmls into des directories.
