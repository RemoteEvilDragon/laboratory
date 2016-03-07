#!/usr/bin/env python

# a truly minimal HTTP proxy

import SocketServer
import SimpleHTTPServer
import urllib
import socks
import socket

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1",1080)
socket.socket = socks.socksocket

PORT = 1234
import os

class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        # self.copyfile(os.system("proxychains wget %s"%(self.path)), self.wfile)
        # proxies = {"socks5":"localhost:1080"}
        # self.copyfile(urllib.urlopen(self.path,proxies=proxies), self.wfile)
        self.copyfile(urllib.urlopen(self.path), self.wfile)

httpd = SocketServer.ForkingTCPServer(('', PORT), Proxy)
print "serving at port", PORT
httpd.serve_forever()

# CONNECT www.google.com.hk:443 HTTP/1.1" 501 socks.py 367

# 127.0.0.1 - - [05/Mar/2016 03:54:44] code 501, message Unsupported method ('CONNECT')
# 127.0.0.1 - - [05/Mar/2016 03:54:44] "CONNECT www.google.com.hk:443 HTTP/1.1" 501 -