#!/usr/bin/env python
#
# This a simple exercise to learn a bit about wxWidgets and PIL
# Author: Ruben Martinez-Cantin <rmcantin@unizar.es>
#

import os
import wx
import numpy as np # NumPy
from PIL import Image,ImageFilter       # PIL

class MainWindow(wx.Frame):
    def __init__(self, parent=None, title='My Photo Editor'):
        super(wx.Frame).__init__(self,parent,title)
        self.panel = wx.Panel(self.frame)
        self.PhotoMaxSize = 300
        self.createWidgets()

     def createWidgets(self):
        """ Creates the layout of the frame """
        
        instructions = 'Browse for an image'
        size = self.PhotoMaxSize
        img = wx.EmptyImage(size,size)

        # Interactive elements
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.BitmapFromImage(img))

        self.imageCtrl2 = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                          wx.BitmapFromImage(img))
        self.photoTxt = wx.TextCtrl(self.panel, size=(200,-1))
        
        instructLbl = wx.StaticText(self.panel, label=instructions)

        # Buttons
        browseBtn = wx.Button(self.panel, label='Browse')
        browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)

        edgesBtn = wx.Button(self.panel, label='Edges')
        edgesBtn.Bind(wx.EVT_BUTTON, self.onEdges)

        medianBtn = wx.Button(self.panel, label='Median')
        medianBtn.Bind(wx.EVT_BUTTON, self.onMedian)

        # Layout
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
        self.panel.SetAutoLayout(True)
        self.mainSizer.Fit(self.frame)
 
        self.panel.Layout()

        
 
class PhotoEditor(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='My Photo Editor')
 
        self.panel = wx.Panel(self.frame)
 
        self.PhotoMaxSize = 300
       
        # Setting up the menu.
        filemenu= wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
 
        # Set events.
        self.frame.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.frame.Bind(wx.EVT_MENU, self.OnExitApp, menuExit) 

        self.frame.Show()

        self.frame.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

 
   
    def OnAbout(self, event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self.frame, "A small photo editor", "About Sample Editor", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExitApp(self, event):
        self.frame.Close(True)  # Close the frame.


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
