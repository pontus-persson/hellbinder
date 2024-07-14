import wx
import config
from functions import *

class LocateSteamFrame(wx.Frame):
    """
    """

    def __init__(self, *args, **kw):
        super(LocateSteamFrame, self).__init__(*args, **kw, size = (800,400))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)

    def OnExit(self, event):
        """Close the frame"""
        self.Close(True)