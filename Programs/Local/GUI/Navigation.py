#====================================================================#
# File Information
#====================================================================#
"""
    Navigation.py
    =============
    This file contains BRS Kontrol's application top navigation bar
    and navigation drawer. It contains classes and functions allowing
    you to quickly get an uniformed tool bar to use for your drivers.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("AppLoading.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
import os
#endregion
#region --------------------------------------------------------- BRS
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Shadow
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
#endregion
#region -------------------------------------------------------- Kivy
from kivy.uix.recycleboxlayout import RecycleBoxLayout
#endregion
#region ------------------------------------------------------ KivyMD
from kivymd.uix.navigationdrawer import MDNavigationDrawer,MDNavigationDrawerDivider,MDNavigationDrawerHeader,MDNavigationDrawerItem,MDNavigationDrawerLabel,MDNavigationDrawerMenu,MDNavigationLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, OneLineListItem, OneLineIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.button import MDFillRoundFlatIconButton
#endregion
from ..FileHandler.deviceDriver import CheckIntegrity, GetDrivers
#====================================================================#
# Functions
#====================================================================#
def TryFunction(*args):
    Debug.Start("TryFunction")
    CheckIntegrity("Debugger")
    Debug.End()
#====================================================================#
# Structure
#====================================================================#
SettingMenuButtons = [
    {
        "name" : _("Network"),
        "icon" : "wifi-cog",
        "function" : TryFunction
    },
    {
        "name" : _("Bluetooth"),
        "icon" : "bluetooth-settings",
        "function" : TryFunction
    },
    {
        "name" : _("Devices"),
        "icon" : "devices",
        "function" : TryFunction
    },
    {
        "name" : _("BrSpand"),
        "icon" : "expansion-card-variant",
        "function" : TryFunction
    },
    {
        "name" : _("Controls & Keybinds"),
        "icon" : "controller",
        "function" : TryFunction
    },
    {
        "name" : _("Account"),
        "icon" : "account-edit",
        "function" : TryFunction
    },
    {
        "name" : _("Quit"),
        "icon" : "power",
        "function" : TryFunction
    }
]
#====================================================================#
# Classes
#====================================================================#
class AppNavigationBar():
    """
        NavigationBar:
        --------------
        This class handles the application page's top navigation bar
        and navigation drawer for the main menus (NOT DRIVERS)
    """
    #region ---------------------------------------------- Constructor
    def __init__(self, pageTitle:str = "", **kwargs):
        super(AppNavigationBar, self).__init__(**kwargs)
        Debug.Start("AppNavigationBar -> __init__")


        # Widgets
        self.NavDrawer = MDNavigationDrawer(pos_hint = {'top': 1, 'left': 0})
        self.DrawerLayout = MDBoxLayout(pos_hint = {'top': 1, 'left': 0})
        self.RecyleBoxLayout = RecycleBoxLayout(default_size=(None,56),
                                                default_size_hint=(1, None),
                                                size_hint=(1, None),
                                                orientation='vertical',
                                                spacing = 10)
        self.recycleView = MDRecycleView(pos_hint = {'top': 1, 'left': 0})
        # RecycleView
        self.RecyleBoxLayout.bind(minimum_height=self.RecyleBoxLayout.setter("height"))
        self.recycleView.add_widget(self.RecyleBoxLayout)
        self.recycleView.viewclass = MDFillRoundFlatIconButton

        # Recycle view filling
        self.recycleView.data = [{'icon': data["icon"],
                                  'font_style' : "H5",
                                   'on_release':data["function"],
                                   'text' : data["name"],
                                   'valign' : "center",
                                   'halign' : "left"}
                                    for data in SettingMenuButtons
                                    ]


        # Nav Drawer handler
        self.NavDrawer.add_widget(self.recycleView)
        self.NavDrawer.orientation = "vertical"
        self.NavDrawer.elevation = Shadow.Elevation.default
        self.NavDrawer.shadow_softness = Shadow.Smoothness.default
        self.NavDrawer.shadow_radius = Shadow.Radius.default

        Debug.Log("Creating MDToolBar")
        self.ToolBar = MDTopAppBar(pos_hint = {'top': 1, 'left': 0})
        self.ToolBar.title = pageTitle
        self.ToolBar.headline_text = "Headline"
        self.ToolBar.anchor_title = "left"
        self.ToolBar.left_action_items = [["menu", lambda x: self.NavDrawer.set_state("open"), "Menu", "Overflow"]]
        self.ToolBar.elevation = Shadow.Elevation.default
        self.ToolBar.shadow_softness = Shadow.Smoothness.default
        self.ToolBar.shadow_radius = Shadow.Radius.default

        self.NavDrawer.set_state("close")
        Debug.End()
    #endregion
    #region -------------------------------------------------- Members
    ToolBar:MDTopAppBar = None
    NavDrawer:MDNavigationDrawer = None
    #endregion
    #region -------------------------------------------------- Methods
    def Callback(self, *args):
        pass
    #endregion
#====================================================================#
LoadingLog.End("AppLoading.py")