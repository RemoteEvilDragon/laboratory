#!/usr/bin/python
#coding=utf-8
__author__ = 'dacxu'
__mail__ = 'xudacheng06.com'
__date__ = '2013-10-29'
__version = 1.0

import sys
import os
import json
from ftplib import FTP
# from progressbar import *

_XFER_FILE = 'FILE'
_XFER_DIR = 'DIR'

class Xfer(object):
    '''
    @note: upload local file or dirs recursively to ftp server
    '''
    def __init__(self):
        self.ftp = None
    
    def __del__(self):
        pass
    
    def setFtpParams(self, ip, uname, pwd, port = 21, timeout = 60):        
        self.ip = ip
        self.uname = uname
        self.pwd = pwd
        self.port = port
        self.timeout = timeout
        self.fullsize = 0
        self.upsize = 0
        self.pbar = None
    
    def initEnv(self):
        if self.ftp is None:
            self.ftp = FTP()
            print '### connect ftp server: %s ...'%self.ip
            self.ftp.connect(self.ip, self.port, self.timeout)
            self.ftp.login(self.uname, self.pwd) 
            print self.ftp.getwelcome()
    
    def clearEnv(self):
        if self.ftp:
            self.ftp.close()
            print '### disconnect ftp server: %s!'%self.ip 
            self.ftp = None
    
    def uploadDir(self, localdir='./', remotedir='./'):
        if not os.path.isdir(localdir):  
            return
        # try:  
        #     for fs in os.listdir(remotedir):
        #         try:  
        #             self.ftp.mkd(fs)  
        #         except:  
        #             sys.stderr.write('the dir is exists %s\n'%fs)
        # except:  
        #     sys.stderr.write('the dir is exists %s\n'%remotedir)
        dirlist = remotedir.split('/')
        crtDir = "."
        for d in dirlist:
            crtDir = crtDir +'/'+ d
            try:
                sys.stderr.write('create sub dir %s\n'%d)
                self.ftp.mkd(crtDir)  
            except:  
                sys.stderr.write('the dir is exists %s\n'%d)            

        # self.ftp.cwd(remotedir) 
        for fs in os.listdir(localdir):
            src = os.path.join(localdir, fs)
            if os.path.isfile(src):
                self.uploadFile(src, remotedir)
            elif os.path.isdir(src):
                # try:  
                #     self.ftp.mkd(fs)  
                # except:  
                #     sys.stderr.write('the dir is exists %s\n'%fs)
                self.uploadDir(src, remotedir +'/'+fs)
        # self.ftp.cwd('..')
    
    def callback(self,p):

        self.upsize = self.upsize + len(p)
        percent = self.upsize * 100 / self.fullsize

        # self.pbar.update(percent)
        # sys.stdout.write("uploading : [%s%s] %i%%\r" % ('#' * percent , ' ' * (100 - percent) , percent))
        # sys.stdout.flush()

    def rename(self, oldname, newname):
        self.initEnv()
        self.ftp.rename(oldname,newname)

    def delete(self, path):
        self.initEnv()
        ispath = True
        try:
            # print "try change path : %s"%path
            self.ftp.cwd(path)
            files = self.ftp.nlst()
            print files
            for i in files:
                # print "delete sub : %s"%i
                self.delete(i)
        except:
            ispath = False
            # raise
        if ispath:
            self.ftp.cwd("../")
        try:
            if ispath :
                # print "delete dir : %s"%path
                self.ftp.rmd(path)
            else:    
                # print "delete : %s"%path
                self.ftp.delete(path)
        except:
            pass

    def lst(self,remotepath = './'):
        self.initEnv()
        self.ftp.cwd(remotepath) 
        files = self.ftp.nlst()
        return files

    def lstr(self,remotepath = './'):
        self.initEnv()
        
        print "cwd %s"%remotepath
        try:

            self.ftp.cwd(remotepath)
        except:
            return []
        print "cwd %s OK"%remotepath
        res = []
        files = self.ftp.nlst()

        for i in files:
            res.append(os.path.join(remotepath,i))

        for i in files:
            # subpath = os.path.join(remotepath,i)
            sunfiles = self.lstr(i)
            for j in sunfiles:
                res.append(os.path.join(remotepath,j))
            self.ftp.cwd('../')
        return res

    def downloadFile(self, localpath, remotepath):
        self.initEnv()
        self.ftp.set_debuglevel(0) 
        #print ftp.getwelcome()#显示ftp服务器欢迎信息 
        filedir = os.path.dirname(remotepath)
        print filedir
        self.ftp.cwd(filedir) #选择操作目录 
        files = self.ftp.nlst()
        # print files 
        filename = os.path.basename(remotepath)
        if not filename in files:
            print("FTP download error , NO FILE : %s"%(remotepath))
            return
        bufsize = 1024 
        file_handler = open(localpath,'wb') #以写模式在本地打开文件 
        self.fullsize = self.ftp.size(filename)
        self.upsize = 0
        self.ftp.retrbinary('RETR %s' % filename,file_handler.write,bufsize)#接收服务器上文件并写入本地文件 
        self.ftp.set_debuglevel(0) 
        file_handler.close() 
        self.ftp.quit() 
        print ("FTP download %s OK"%(remotepath))
        pass

    def uploadFile(self, localpath, remotepath='./'):
        self.initEnv()
        if not os.path.isfile(localpath):  
            return
        self.fullsize = os.path.getsize(localpath)
        self.upsize = 0
        print '+++ upload %s to %s:%s'%(localpath, self.ip, remotepath)

        # self.pbar = ProgressBar().start()
        filedir = os.path.dirname(remotepath)
        try:  
            self.ftp.mkd(filedir)  
        except:  
            sys.stderr.write('the dir is exists %s'%filedir)
        # self.ftp.cwd(remotepath) 
        basename = os.path.basename(localpath)
        # print( 'STOR ' + remotepath + '/'+basename)
        self.ftp.storbinary('STOR ' + remotepath + '/'+basename, open(localpath, 'rb'),8192, self.callback)
    
    def __filetype(self, src):
        if os.path.isfile(src):
            index = src.rfind('\\')
            if index == -1:
                index = src.rfind('/')                
            return _XFER_FILE, src[index+1:]
        elif os.path.isdir(src):
            return _XFER_DIR, ''        
    
    def upload(self, src , remotedir = './'):
        filetype, filename = self.__filetype(src)
        
        self.initEnv()
        if filetype == _XFER_DIR:
            print("...upload dir " + src +'\n')
            self.srcDir = src            
            self.uploadDir(self.srcDir,remotedir)
        elif filetype == _XFER_FILE:
            # print('aaaaaaaaaaa\n')
            # print(src+'\n')
            # print(remotedir+'\n')
            self.uploadFile(src,remotedir)
        self.clearEnv() 
               

if __name__ == '__main__':
    srcDir = r"C:\sytst"
    srcFile = r'C:\sytst\sar.c'
    xfer = Xfer()
    xfer.setFtpParams('192.x.x.x', 'jenkins', 'pass')
    xfer.upload(srcDir)    
    xfer.upload(srcFile)