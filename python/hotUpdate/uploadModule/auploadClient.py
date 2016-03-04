#!/usr/bin/env python
import requests

import os
import zipfile
import sys


tempZip='Depressed.zip'

def zipdir(path):
	ziph = zipfile.ZipFile(tempZip,'w',zipfile.ZIP_DEFLATED)

	if os.path.isdir(path):
		for root,dirs,files in os.walk(path):
			for file in files:
				ziph.write(os.path.join(root,file))
		ziph.close()
	else:
		ziph.write(path)
		ziph.close()

#1.zip files
#2.use http post method to start http request.
def uploadfile(uploadurl):
    r = requests.post(uploadurl, files={tempZip: open(tempZip,'rb')})
    print "Success!Upload Complete."

zipdir(sys.argv[1])
uploadfile("http://27.126.181.90:10000")
# uploadfile("http://localhost:10000")