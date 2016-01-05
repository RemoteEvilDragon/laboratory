import xlrd
import xml.etree.ElementTree as ET
import os

def transfer(_file):
	output_file = ET.Element('Guankas')
	book = xlrd.open_workbook(_file)
	sh = book.sheet_by_index(0)
	for rx in range(sh.nrows):
		if rx <= 1:
			pass
		else:
			subEle = ET.SubElement(output_file,'Guanka')
			for cx in range(sh.ncols):
				value = sh.cell_value(rowx=rx, colx=cx)
				try:
					value = int(value)
				except ValueError:
					pass
				subEle.set(sh.cell_value(rowx=1, colx=cx),str(value))
	output_path = os.path.dirname(_file)+"/"+sh.name+".xml"
	print output_path
	ET.ElementTree(output_file).write(output_path)

for root,dirs,files in os.walk(os.curdir+"/config"):
	for file in files:
		if file.endswith('xlsx'):
			path = os.path.join(root,file)
			print path
			transfer(path)
