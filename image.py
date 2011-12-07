#!/usr/bin/env python
#
# This a simple exercise to learn a bit about wxWidgets and PIL
# Author: Ruben Martinez-Cantin <rmcantin@gmail.com>
#

import os
import wx
import numpy as np # NumPy
from PIL import Image,ImageFilter       # PIL

 
class PhotoEditor(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='My Photo Editor')
 
        self.panel = wx.Panel(self.frame)
 
        self.PhotoMaxSize = 300
 
        self.createWidgets()
        self.frame.Show()
 
    def createWidgets(self):
        """ Creates the layout of the frame """
        
        instructions = 'Browse for an image'
        size = self.PhotoMaxSize
        img = wx.EmptyImage(size,size)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.BitmapFromImage(img))

        self.imageCtrl2 = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                          wx.BitmapFromImage(img))

        instructLbl = wx.StaticText(self.panel, label=instructions)
        self.photoTxt = wx.TextCtrl(self.panel, size=(200,-1))
        browseBtn = wx.Button(self.panel, label='Browse')
        browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)

        edgesBtn = wx.Button(self.panel, label='Edges')
        edgesBtn.Bind(wx.EVT_BUTTON, self.onEdges)

        medianBtn = wx.Button(self.panel, label='Median')
        medianBtn.Bind(wx.EVT_BUTTON, self.onMedian)
 
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        box = wx.StaticBox(self.panel, -1, "Photos")
        self.photoSizer = wx.StaticBoxSizer(box,wx.HORIZONTAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
 
        self.photoSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        self.photoSizer.Add(self.imageCtrl2, 0, wx.ALL, 5)
        self.mainSizer.Add(self.photoSizer, 0, wx.ALL, 5)
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)
        self.mainSizer.Add(instructLbl, 0, wx.ALL, 5)
        self.sizer.Add(self.photoTxt, 0, wx.ALL, 5)
        self.sizer.Add(browseBtn, 0, wx.ALL, 5)
        self.sizer.Add(edgesBtn, 0, wx.ALL, 5)
        self.sizer.Add(medianBtn, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)
 
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
 
        self.panel.Layout()

    # Buttons  #################################
    def onBrowse(self, event):
        """ Browse for file """
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTxt.SetValue(dialog.GetPath())
        dialog.Destroy()
        self.onView()

    def onEdges(self, event):
        """ Find edges """
        filepath = self.photoTxt.GetValue()
        img = Image.open(filepath)
        pil = self.edges(img)
        self.drawImage(self.PilImageToWxImage(pil),False)

    def onMedian(self, event):
        """ Median value of pixels """
        filepath = self.photoTxt.GetValue()
        img = Image.open(filepath)
        pil = img.filter(ImageFilter.MedianFilter(3))
        self.drawImage(self.PilImageToWxImage(pil),False)
    #################################


    # Drawing operations
    def onView(self):
        filepath = self.photoTxt.GetValue()
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        self.drawImage(img,True)
        
    def drawImage(self,img,original):
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW,NewH)

        if original:
            self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        else:
            self.imageCtrl2.SetBitmap(wx.BitmapFromImage(img))
        self.panel.Refresh()


    # Image operations
    def PilImageToWxImage(self, myPilImage ):
        myWxImage = wx.EmptyImage( myPilImage.size[0], myPilImage.size[1] )
        myWxImage.SetData( myPilImage.convert( 'RGB' ).tostring() )
        return myWxImage

    def edges(self, img):
        src = np.array(img.convert('L'), dtype=int)

        s_vedges = (src[:,1:] - src[:,:-1])
        s_hedges = (src[1:] - src[:-1])
        # Some clipping to remove lower values and remove features
        s_vedges[s_vedges < 0] = 0
        s_hedges[s_vedges < 0] = 0

        edges = np.sqrt(s_vedges[:-1]**2 + s_hedges[:,:-1]**2)
        height, width = edges.shape
        b = np.empty((height, width), dtype = np.uint8)
        b = edges * (255 / edges.max())

        return Image.fromarray(b)

        

 
if __name__ == '__main__':
    app = PhotoEditor()
    app.MainLoop()
