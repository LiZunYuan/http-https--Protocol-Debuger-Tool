#coding=utf-8

#打包命令 : python setup2exe.py py2app

__author__ = 'zunyuan.li'


from distutils.core import setup
import py2exe

options = {"py2exe":{"compressed": 1, #压缩
                     "optimize": 2,
                     "bundle_files": 1 #所有文件打包成一个exe文件
        }}
setup(console=["http_https_Protocol_DebugerTool.py"],options=options,zipfile=None)