#!/usr/bin/env python
import requests


def uploadfile(filepath, uploadurl, fileformelementname="upfile"):
    '''
    This will invoke an upload to the webserver
    on the VM
    '''
 
    files = {fileformelementname : open(filepath,'rb')}
    r = requests.post(uploadurl, files=files)
    return r.status_code
 
uploadStatus = uploadfile(currentFile.fullpath, UPLOADURL, "upfile")