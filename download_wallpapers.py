#!/usr/bin/python
#coding=utf-8

import sys
sys.path.append("/usr/lib/python2.7")

import urllib2
import xml.etree.ElementTree as ET
import os
import os.path as op
import socket
import commands
import json
def download_picture():
	basedir = op.join(op.abspath(op.dirname(__file__)), 'wallpapers')
        print "wallpapers will be storaged in" + basedir
	if not op.exists(basedir):
		os.mkdir(basedir)
	validpath = ''
        #只下载最新的，如果改为降-1改为16，可以下载最近17天的照片
        #默认只下载明天的壁纸
	for i in range(-1, -2, -1):
                json_url = 'http://cn.bing.com/HPImageArchive.aspx?format=js&n=1&idx=%d' % (i)
		#this url supports ipv6, but cn.bing.com doesn't
		try:
                        page=urllib2.urlopen(json_url)
                        data=page.read()
                        #解析json数据，得到日期和图片下载地址
                        ddata=json.loads(data)
                        imgurl=ddata['images'][0]['url']
                        datestr=ddata['images'][0]['enddate']
		except socket.timeout:
			print 'timeout downloading image information.'
			continue

		# datestr = root[0].text
		imgpath = op.join(basedir, '%s.jpg' % (datestr))
		if not op.exists(imgpath):
			try:
                                print imgurl
				imgdata = urllib2.urlopen(imgurl, timeout = 10).read()
				if len(imgdata) < 100 * 1024:#if tunet not authorized
					pass
				else:
					imgfile = file(imgpath, 'wb')
					imgfile.write(imgdata)
					imgfile.close()
					validpath = imgpath
			except socket.timeout:
				print 'timeout downloading wallpapers.'
				continue
		else:
			validpath = imgpath
	return validpath

def set_wallpaper(picpath):
	if sys.platform == 'win32':
		import win32api, win32con, win32gui
		k = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, 'Control Panel\Desktop', 0, win32con.KEY_ALL_ACCESS)
		curpath = win32api.RegQueryValueEx(k, 'Wallpaper')[0]
		if curpath == picpath:
			pass
		else:
			# win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2")#2 for tile,0 for center
			# win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
			win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, picpath, 1+2)
		win32api.RegCloseKey(k)
	else:
		curpath = commands.getstatusoutput('gsettings get org.gnome.desktop.background picture-uri')[1][1:-1]
		if curpath == picpath:
			pass
		else:
                    commands.getstatusoutput('DISPLAY=:0 gsettings set org.gnome.desktop.background picture-uri file://"%s"' % (picpath))


picpath = download_picture()
if picpath != '':
	set_wallpaper(picpath)
else:
	pass
