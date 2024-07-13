#!/usr/bin/env python
import wx
import config
from functions import *
from frames import LocateSteamFrame

class MainFrame(wx.Frame):
    """
    Main frame (heheh)
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(MainFrame, self).__init__(*args, **kw, size = (1024,640))

        path = get_settings_file()

        self.MakeFrameContent()

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Unauthorized use will be reported to the nearest Democracy Officer or Ministry of Truth official.")

    def GetConfig(self, event):
        wx.MessageBox(config.settings_file)
        settings = get_settings_obj()
        print(config.available_bindings)
        save_settings_obj(settings)

    def CreateBackup(self, event):
        new_file = make_config_backup()
        wx.MessageBox(
            "Saved backup: "+new_file,
            "Config backup created",
            wx.OK|wx.ICON_INFORMATION
        )
        # # btn = event.GetEventObject().GetLabel()
        # make_config_backup()
        # settings = get_settings_obj()
        # print(available_bindings)
        # save_settings_obj(settings)

    def LocateSteam(self, event):

        # if self.contentNotSaved:
        #     if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
        #                     wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
        #         return

        with wx.FileDialog(self, "Locate the Steam executable", wildcard="Steam executable (steam.exe)|steam.exe", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed finding helldivers from the path user picked
            steam_path = fileDialog.GetPath()
            found_file = get_settings_file(steam_path)
            if found_file:
                # self.settings_text.SetLabel(label="Found settings file: "+found_file)
                self.UpdateVisiblePanels()
                # self.MakeFrameContent()
            else:
                wx.MessageBox(
                    "Could not locate Helldivers 2, make sure you have it installed and cloud saves enabled.",
                    "Error",
                    wx.OK|wx.ICON_ERROR
                )

    def MakeFrameContent(self):
        # create panels
        self.not_found_panel = wx.Panel(self)
        self.found_panel = wx.Panel(self)

        self.buttons1 = wx.BoxSizer(wx.VERTICAL)
        self.buttons2 = wx.BoxSizer(wx.VERTICAL)

        # if config.settings_file:
        #     self.settings_text = wx.StaticText(self.found_panel, label="Found settings file: "+config.settings_file)
        # else:
        #     self.settings_text = wx.StaticText(self.not_found_panel, label="Could not locate settings file")

        not_found_text = wx.StaticText(self.not_found_panel, label="Could not locate settings file")
        font = not_found_text.GetFont()
        font.PointSize += 4
        font = font.Bold()
        not_found_text.SetFont(font)
        # self.sizer.Add(self.not_found_text, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 5))

        # not found
        self.buttons1.Add(not_found_text, 0, wx.ALIGN_CENTER)
        self.locate_steam_btn = wx.Button(self.not_found_panel, -1, "Locate steam")
        self.buttons1.Add(self.locate_steam_btn, 0, wx.ALIGN_CENTER)
        self.locate_steam_btn.Bind(wx.EVT_BUTTON, self.LocateSteam)

        self.not_found_panel.SetSizer(self.buttons1)

        # self.Add(self.not_found_panel, 0, wx.ALIGN_CENTER)

        # found
        self.read_file_btn = wx.Button(self.found_panel, -1, "Read file")
        self.buttons2.Add(self.read_file_btn, 0, wx.ALIGN_CENTER)
        self.read_file_btn.Bind(wx.EVT_BUTTON, self.GetConfig)

        self.backup_btn = wx.Button(self.found_panel, -1, "Backup config")
        self.buttons2.Add(self.backup_btn, 0, wx.ALIGN_CENTER)
        self.backup_btn.Bind(wx.EVT_BUTTON, self.CreateBackup)

        self.found_panel.SetSizer(self.buttons2)


        # self.Add(self.found_panel, 0, wx.ALIGN_CENTER)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.not_found_panel, 1, wx.EXPAND)
        self.sizer.Add(self.found_panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        # self.SetSizer(self.not_found_panel)
        # self.not_found_panel.SetSizer(self.sizer)
        # self.found_panel.SetSizer(self.buttons)

        self.UpdateVisiblePanels()
        # self.Layout()
        # self.Update()

    def UpdateVisiblePanels(self):
        if config.settings_file:
            self.found_panel.Show()
            self.not_found_panel.Hide()
        else:
            self.found_panel.Hide()
            self.not_found_panel.Show()
        self.Layout()
        # self.Update()

    def makeMenuBar(self):
        """
        """
        fileMenu = wx.Menu()
        exitItem = fileMenu.Append(wx.ID_EXIT)

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("Hellbinder, keybinder for Helldivers 2\nUse at your own risk\nReport any errors to your Democracy Officer (or at https://github.com/pontus-persson/hellbinder/issues)",
                      "About Hellbinder",
                      wx.OK|wx.ICON_INFORMATION)

if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = MainFrame(None, title='Hellbinder')
    frm.Show()
    # locate_steam = LocateSteamFrame(None, title='Locate steam')
    # locate_steam.Show()
    app.MainLoop()