#!/usr/bin/env python
# -*- coding: utf8 -*-
import csv
with open('guankas.csv','wb') as csvfile:
	fieldnames=['关卡ID','关卡名称']
	writer = csv.DictWriter(csvfile,fieldnames=fieldnames)

	# writer.writeheader()

	maxLevel = 14
	maxDiff = 3
	for level in range(maxLevel):
		for diff in range(maxDiff):
			writer.writerow({'关卡ID':'gk'+str(level+1)+'_'+str(diff+1),'关卡名称':'单人'+str(level+1)+'_'+str(diff+1)})
			writer.writerow({'关卡ID':'gkd'+str(level+1)+'_'+str(diff+1),'关卡名称':'双人'+str(level+1)+'_'+str(diff+1)})