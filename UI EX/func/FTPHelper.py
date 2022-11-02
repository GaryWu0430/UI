#!/usr/bin/python  
# -*- coding: utf-8 -*-  
  
from ftplib import FTP  
import os

class FTPHelper:
    def __init__(self, debuglevel=0):
        self.__ftp = None
        self.__debuglevel = debuglevel
        
    def Connect(self, ftpserver='172.26.6.51', username='sel', password='sel', port=21):
        self.__ftp = FTP()
        self.__ftp.set_debuglevel(self.__debuglevel)  # 打开调试级别，显示详细信息
        self.__ftp.connect(ftpserver, port)  # 连接
        self.__ftp.login(username, password)  # 登录，如果匿名登录则用空串代替即可
        # return self.__ftp  
          
    def Download(self, remotepath, localpath):
        self.Connect()  
        # print self.__ftp.getwelcome() #显示self.__ftp服务器欢迎信息  
        bufsize = 1024  # 设置缓冲块大小
        
        fp = open(localpath, 'wb')
        self.__ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)  # 接收服务器上文件并写入本地文件  
        fp.close()  
        self.__ftp.quit()  # 退出self.__ftp服务器  

    def Upload(self, remotepath, localpath):
        ret=False
        try:
            self.Connect()
            index = remotepath.rfind('/')    
            remotefolder = remotepath[0:index]
            self.mkdir(remotefolder)
            bufsize = 1024  
            fp = open(localpath, 'rb')  
            self.__ftp.storbinary('STOR ' + remotepath , fp, bufsize)  # 上传文件 
            fp.close()  # 关闭文件  
            self.__ftp.quit()
            ret=True 
        except Exception:
            print Exception.message
        finally:    
            return ret

    def RemotePathExist(self, remotepath):
        index = remotepath.rfind('/')    
        remotefolder = remotepath[0:index]
        filename = remotepath[index + 1:]
        
        self.Connect()  
        self.__ftp.cwd(remotefolder)
        files = self.__ftp.nlst()
        self.__ftp.quit()  # 退出self.__ftp服务器  
        if filename in files:
            return True
        else:
            return False
            
    def Delete(self, remotepath):
        if self.RemotePathExist(remotepath):
            self.Connect()
            self.__ftp.delete(remotepath)
            return not self.RemotePathExist(remotepath)
        else:
            return False
        
    def mkdir(self, remotepath):
        try:
            self.__ftp.cwd(remotepath)
        except:
            try:
                self.__ftp.mkd(remotepath)
                self.__ftp.cwd(remotepath) 
            except:
                meg = 'You have no authority to make directory: %s' % remotepath
                print meg

if __name__ == '__main__':
    ftp = FTPHelper()
    ftp.Download('/EY3.PNG', r'd:\test.bmp')
    ftp.Upload('/XE3/EY3.PNG', r'd:\test.jpg')
    checkresult = ftp.RemotePathExist('/XE3/EY3.PNG')
    if not checkresult:
        print '文件不存在'
        
    print ftp.Delete('/XE3/1.txt')


