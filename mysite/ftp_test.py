# coding: utf-8
from ftplib import FTP
import time
import tarfile
import os
# !/usr/bin/python
# -*- coding: utf-8 -*-

from ftplib import FTP

from myConfig import 两高楼宇采集host, 两高楼宇采集port, 两高楼宇采集username, 两高楼宇采集password


def ftpconnect(host,port, username, password):
    ftp = FTP()
    # ftp.set_debuglevel(2)
    ftp.connect(host, port)
    ftp.login(username, password)
    return ftp

#从ftp下载文件
def downloadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'wb')
    remotepath = remotepath.encode('utf-8').decode('unicode_escape')
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
    ftp.set_debuglevel(0)
    fp.close()

#从本地上传文件到ftp
def uploadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')
    remotepath = remotepath.encode('utf-8').decode('unicode_escape')
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()

if __name__ == "__main__":
    ftp = ftpconnect(两高楼宇采集host,两高楼宇采集port, 两高楼宇采集username, 两高楼宇采集password)
    downloadfile(ftp, "Faint.mp4", "C:/Users/Administrator/Desktop/test.mp4")
    #调用本地播放器播放下载的视频
    os.system('start "C:\Program Files\Windows Media Player\wmplayer.exe" "C:/Users/Administrator/Desktop/test.mp4"')
    uploadfile(ftp, "C:/Users/Administrator/Desktop/test.mp4", "test.mp4")

    ftp.quit()