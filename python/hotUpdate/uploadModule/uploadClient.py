#!/usr/bin/env python
import requests

import os
import zipfile

def zipdir(path):
	ziph = zipfile.ZipFile('Depressed.zip','w',zipfile.ZIP_DEFLATED)
	for root,dirs,files in os.walk(path):
		for file in files:
			ziph.write(os.path.join(root,file))
	ziph.close()

#1.zip files
#2.use http post method to start http request.
def uploadfile(uploadurl):
    r = requests.post(uploadurl, files={'Depressed.zip': open('Depressed.zip', 'rb')})
    print r.text


zipdir("../testDir")
uploadfile("http://27.126.181.90:10000")
# uploadfile("http://localhost:10000")