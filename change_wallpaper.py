#!/usr/bin/python
import os,random,commands

basedir = "/mnt/code/code/python/cleanBingDesktop/wallpapers/";
filename = basedir + random.choice(os.listdir('/mnt/code/code/python/cleanBingDesktop/wallpapers'))
print filename
commands.getstatusoutput('DISPLAY=:0 gsettings set org.gnome.desktop.background picture-uri file://"%s"' % (filename))
