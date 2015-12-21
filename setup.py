#coding=utf-8

#打包命令 : python setup.py py2app

__author__ = 'zunyuan.li'

import sys
reload(sys)
sys.setdefaultencoding('utf8')


from setuptools import setup

APP = ['http_https_Protocol_DebugerTool.py']
OPTIONS = {
    #'includes': ['about.png'],
    'iconfile': 'debugerTool.icns',
    'plist': {'CFBundleShortVersionString': '0.1', }
}
DATA_FILES = ['about.png', 'avatar.jpg']

setup(
    app = APP,
    name= 'http https Protocol DebugerTool',
    data_files = DATA_FILES,
    options = {'py2app' : OPTIONS},
    setup_requires=['py2app']
)