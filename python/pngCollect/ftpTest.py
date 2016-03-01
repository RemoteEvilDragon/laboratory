#!/usr/bin/env python
name  = 1

def changeName():
	global name
	name = 2

def changeTo():
	global name
	name = 3

changeName()
print name

changeTo()
print name
