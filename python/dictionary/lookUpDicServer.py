#!/usr/bin/env python
#-*- coding:utf-8 -*-
import datetime
import pymysql
import SocketServer

def queryDB(word):
	cnx = pymysql.connect(user='root',passwd='athens',port=3306,host='localhost',db='EnglishDic')
	cursor = cnx.cursor()
	query = ("SELECT wordType,definition FROM `entries` WHERE word=%s")
	cursor.execute(query,word)
	result = cursor.fetchall()
	cursor.close()
	cnx.close()
	return str(result)


class MyTCPHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		self.data = self.request.recv(1024).strip()
		self.request.sendall(queryDB(self.data))

HOST,PORT="0.0.0.0",13206
server = SocketServer.TCPServer((HOST,PORT),MyTCPHandler)
server.serve_forever()