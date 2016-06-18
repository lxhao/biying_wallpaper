#!/usr/bin/python
import os,random,commands
import os.path as op

basedir = op.join(op.abspath(op.dirname(__file__)), 'wallpapers')
filename = basedir + '/' +  random.choice(os.listdir(basedir))
print filename
commands.getstatusoutput('DISPLAY=:0 gsettings set org.gnome.desktop.background picture-uri file://"%s"' % (filename))
