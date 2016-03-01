#!/usr/bin/env python

import time
import ftplib
import os
import sys

server="27.126.181.90"
username="athenking"
password="freedom"

myFtp = ftplib.FTP(server,username,password)

myFtp.cwd("pngLib")
