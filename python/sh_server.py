#!/usr/bin/env python
#-*- coding:utf-8 -*-


import SocketServer

class MyTcpHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		self.data = self.rfile.readline().strip()

		self.wfile.write("Server_received.")

HOST,PORT="0.0.0.0",12345
server = SocketServer.TCPServer((HOST,PORT),MyTcpHandler)
server.serve_forever()