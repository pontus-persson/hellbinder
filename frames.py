import wx
import config
from functions import *

class LocateSteamFrame(wx.Frame):
    """
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(LocateSteamFrame, self).__init__(*args, **kw, size = (800,400))

        # create a panel in the frame
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        path = get_settings_file()

        print(path)
        if path:
            self.settings_text = wx.StaticText(panel, label="Found settings file: "+path)
        else:
            self.settings_text = wx.StaticText(panel, label="Could not locate settings file")

        font = self.settings_text.GetFont()
        font.PointSize += 4
        font = font.Bold()
        self.settings_text.SetFont(font)

        # and create a sizer to manage the layout of child widgets
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.settings_text, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 5))

        buttons = wx.BoxSizer(wx.HORIZONTAL)

        self.btn = wx.Button(panel, -1, "Locate steam")
        # vbox.Add(self.btn,0,wx.ALIGN_CENTER)
        buttons.Add(self.btn, 0, wx.ALIGN_CENTER)
        self.btn.Bind(wx.EVT_BUTTON, self.OnOpen)

        sizer.Add(buttons, 0, wx.ALIGN_CENTER)

        panel.SetSizer(sizer)

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnOpen(self, event):

        # if self.contentNotSaved:
        #     if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
        #                     wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
        #         return

        with wx.FileDialog(self, "Locate the steam executable", wildcard="steam executable (steam.exe)|steam.exe",
                        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            steam_path = fileDialog.GetPath()
            print('found ' + steam_path)
            found_file = get_settings_file(steam_path)
            self.settings_text.SetLabel(label="Found settings file: "+found_file)