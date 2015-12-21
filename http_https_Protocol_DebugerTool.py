#coding=utf-8
__author__ = 'zunyuan.li'

# Python 标准库 urllib2 的使用细节
#                       http://www.cnblogs.com/yuxc/archive/2011/08/01/2123995.html
# httplib2
# http://www.cnblogs.com/qq78292959/archive/2013/04/01/2993133.html

# urplib2 proxy
# http://blog.csdn.net/wklken/article/details/7364390



import  sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2
import urllib
import json
import wx
from MyInfo import AboutMe
import os
import subprocess
import sqlite3

"""
主界面
"""

class AHFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self,
                          parent,
                          -1,
                          title,
                          wx.DefaultPosition,
                          wx.Size(500, 500)
                          #style=wx.DEFAULT_FRAME_STYLE
                          #style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        )
                          #style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX)
        #拖进到窗口中的文件列表
        self.filesList = []

        #创建状态栏
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetForegroundColour('red')
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-2, -1]) #大小比例2:1

        #创建工具栏
        toolbar = self.CreateToolBar()
        toolbar.AddSimpleTool(1, wx.Image('./about.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), "关于我", "")
        toolbar.AddSeparator()
        toolbar.Realize()  #准备显示工具栏
        wx.EVT_TOOL(self, 1, self.OnAboutMe)

        #创建panel
        self.panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # 第一行
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        # URL
        self.UUIDStringText = wx.StaticText(self.panel, -1 , u'URL' , style=wx.TE_WORDWRAP)
        hbox1.Add(self.UUIDStringText, 0, wx.EXPAND)
        # input URL
        self.urlTextCtrl = wx.TextCtrl(self.panel, -1)
        hbox1.Add(self.urlTextCtrl, 10 , wx.EXPAND)
        #port
        self.PortStringText = wx.StaticText(self.panel, -1 , u'Port' , style=wx.TE_WORDWRAP)
        hbox1.Add(self.PortStringText, 0, wx.EXPAND)
        # input port
        self.portTextCtrl = wx.TextCtrl(self.panel, -1)
        hbox1.Add(self.portTextCtrl, 1 , wx.EXPAND)

        self.vbox.Add(hbox1, 0, wx.EXPAND | wx.ALL, 5)


        # 第二行
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        # url param
        self.UrlParamStringText = wx.StaticText(self.panel, -1 , u'Param' , style=wx.TE_WORDWRAP)
        hbox2.Add(self.UrlParamStringText, 0, wx.EXPAND)
        # input Url Param
        self.urlParamTextCtrl = wx.TextCtrl(self.panel, -1)
        hbox2.Add(self.urlParamTextCtrl, 10 , wx.EXPAND)
        # method
        self.methodStringText = wx.StaticText(self.panel, -1 , u'Method' , style=wx.TE_WORDWRAP)
        hbox2.Add(self.methodStringText, 0, wx.EXPAND)
        # select method
        sampleList = ['GET', 'POST']
        self.methodChoice = wx.Choice(self.panel, -1, (85, 18), choices=sampleList)
        hbox2.Add(self.methodChoice,2,wx.EXPAND)
        # start
        self.startBtn = wx.Button(self.panel, -1, u'开始')
        self.startBtn.Bind(wx.EVT_BUTTON, self.startRequest)
        hbox2.Add(self.startBtn, 2, wx.EXPAND)
        # stop
        self.stopBtn = wx.Button(self.panel, -1, u'停止')
        self.stopBtn.Bind(wx.EVT_BUTTON, self.stopRequest)
        hbox2.Add(self.stopBtn, 2, wx.EXPAND)

        self.vbox.Add(hbox2, 0, wx.EXPAND | wx.ALL, 5)


        # 第三行
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        # Proxy
        self.ProxyStringText = wx.StaticText(self.panel, -1 , u'Proxy' , style=wx.TE_WORDWRAP)
        hbox3.Add(self.ProxyStringText, 0, wx.EXPAND)
        # input Proxy
        self.ProxyTextCtrl = wx.TextCtrl(self.panel, -1)
        hbox3.Add(self.ProxyTextCtrl, 10 , wx.EXPAND)
        # use proxy
        self.UseProxyCheckBox = wx.CheckBox(self.panel,-1,'use Proxy',(20,100),(100,-1))
        hbox3.Add(self.UseProxyCheckBox, 10 , wx.EXPAND)

        self.vbox.Add(hbox3, 0, wx.EXPAND | wx.ALL, 5)

        # 第四行
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        # output
        self.outputTextCtrl = wx.TextCtrl(self.panel, -1 ,style=wx.TE_MULTILINE)
        hbox4.Add(self.outputTextCtrl, 2, wx.EXPAND)

        self.vbox.Add(hbox4, 2, wx.EXPAND | wx.ALL, 5)
        self.panel.SetSizer(self.vbox)

        # 加一些默认值
        self.urlTextCtrl.SetValue("http://api.beibei.com/gateway/route.html?keyword=%25E5%258F%258C%25E7%25A6%25B9&gender_age=1&client_info=%7B%0A%20%20%22screen%22%20%3A%20%22375x667%22%2C%0A%20%20%22os%22%20%3A%20%229.1%22%2C%0A%20%20%22platform%22%20%3A%20%22iPhone%22%2C%0A%20%20%22model%22%20%3A%20%22iPhone%22%2C%0A%20%20%22udid%22%20%3A%20%22d41d8cd98f00b204e9800998ecf8427e689ac76a%22%2C%0A%20%20%22bd%22%20%3A%20%22App%20Store%22%2C%0A%20%20%22version%22%20%3A%20%223.6.0%22%0A%7D&sign=FFB1C6B49E2B6ECD0B4DE0F1838B8596&brand_ids=0&timestamp=1450663657&filter_sellout=0&session=1bab524926101700567296453fbe8&source=mainViewController&cat_ids=0&page=1&page_size=30&sort=hot&method=beibei.item.search")
        self.urlTextCtrl.SetValue("http://www.baidu.com")
        self.portTextCtrl.SetValue("80")




    # 开始请求网络
    def startRequest(self,event):
        self.outputTextCtrl.SetValue("Loading...")

        enable_proxy = False
        proxy_handler = urllib2.ProxyHandler({"http" : self.ProxyTextCtrl.GetValue()})
        null_proxy_handler = urllib2.ProxyHandler({})

        if self.UseProxyCheckBox.IsChecked():
            opener = urllib2.build_opener(proxy_handler)
        else:
            opener = urllib2.build_opener(null_proxy_handler)

        urllib2.install_opener(opener)

        response = urllib2.urlopen(self.urlTextCtrl.GetValue())
        html = response.read()

        # 转json
        try:
            # html = html.decode("GB2312").encode("gbk")
            jsonHtml = json.loads(html);
            formatHtml = json.dumps(jsonHtml, ensure_ascii=False, indent=4);
        except Exception,ex:
            formatHtml = html
            print "出错"

        # print formatHtml
        self.outputTextCtrl.SetValue(formatHtml)

        # format
        # opener = urllib2.build_opener(null_proxy_handler)
        # urllib2.install_opener(opener)
        # values = {
        #     'c':html,
        #     'o':'1'
        #
        # }
        # formatUrl = 'http://web.chacuo.net/formatxml?data=' + urllib.quote(html) + '&type=format&beforeSend=undefined'
        # formatUrl = 'http://www.atool.org/include/XmlFormat.php'
        #
        # req = urllib2.Request(formatUrl, urllib.urlencode(values))
        # response = urllib2.urlopen(req)
        #
        # formatHtml = response.read()

        # self.outputTextCtrl.write(formatHtml)

    def stopRequest(self,event):
        response = urllib2.urlopen(self.urlTextCtrl.GetValue())
        html = response.read()

    #显示关于我的界面
    def OnAboutMe(self, event):
        aboutMe = AboutMe(self)
        aboutMe.ShowModal()
        aboutMe.Destroy()

versions = '0.1'
if __name__ == '__main__':
    app = wx.App(redirect=False)
    frame = AHFrame(None, 'Http/Https Protocol Debuger' + ' v' + versions)
    frame.ShowWithEffect(True)
    app.MainLoop()
