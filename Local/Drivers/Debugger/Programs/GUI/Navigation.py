#====================================================================#
# File Information
#====================================================================#
"""
    Navigation.py
    =============
    This file contains BRS Kontrol's Debugger application top
    navigation bar and navigation drawer. It contains classes and
    functions allowing you to quickly get an uniformed tool bar to
    use for your drivers.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from msilib.schema import Icon
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("AppLoading.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import os
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Shadow
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, CardTransition, SlideTransition, SwapTransition, ShaderTransition
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import("KivyMD")
from kivymd.uix.navigationdrawer import MDNavigationDrawer,MDNavigationDrawerDivider,MDNavigationDrawerHeader,MDNavigationDrawerItem,MDNavigationDrawerLabel,MDNavigationDrawerMenu,MDNavigationLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, OneLineListItem, OneLineIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.button import MDFillRoundFlatIconButton, MDIconButton
#endregion
LoadingLog.Import("Local")
#====================================================================#
# Functions
#====================================================================#
# ----------------------------------------------------------------
def GoTo_Quit(*args):
    """
        GoTo_Quit:
        ==========
        Summary:
        --------
        This callback function is executed when the user presses
        on the Account button inside the navigation drawer.
        This should take them to the Account screen or an error
        pop up in case it fails for X reason.
    """
    Debug.Start("GoTo_Quit")
    from Local.Drivers.Debugger.Driver import Quit
    Quit()
    Debug.End()
# ----------------------------------------------------------------
def GoTo_BrSpand(*args):
    """
        GoTo_BrSpand:
        =================
        Summary:
        --------
        This callback function is executed when the user presses
        on the BrSpand button inside the navigation drawer.
        This should take them to the BrSpand screen or an error
        pop up in case it fails for X reason.
    """
    Debug.Start("GoTo_BrSpand")
    from Local.Drivers.Debugger.Pages.DebuggerBrSpand import DebuggerBrSpand_Screens
    DebuggerBrSpand_Screens._callerTransition = SlideTransition
    DebuggerBrSpand_Screens._callerDirection = "right"
    DebuggerBrSpand_Screens.Call()
    Debug.End()
# ----------------------------------------------------------------
def GoTo_About(*args):
    """
        GoTo_About:
        ===========
        Summary:
        --------
        This callback function is executed when the user presses
        on the about button inside the navigation drawer.
        This should take them to the about screen or an error
        pop up in case it fails for X reason.
    """
    Debug.Start("GoTo_About")
    Debug.End()
# ----------------------------------------------------------------
def GoTo_Kontrol(*args):
    """
        GoTo_Kontrol:
        ===========
        Summary:
        --------
        This callback function is executed when the user presses
        on the Kontrol button inside the navigation drawer.
        This should take them to the Kontrol screen or an error
        pop up in case it fails for X reason.
    """
    Debug.Start("GoTo_Kontrol")
    Debug.End()
# ----------------------------------------------------------------
def GoTo_Bluetooth(*args):
    """
        GoTo_Bluetooth:
        ===============
        Summary:
        --------
        This callback function is executed when the user presses
        on the Bluetooth button inside the navigation drawer.
        This should take them to the Bluetooth screen or an error
        pop up in case it fails for X reason.
    """
    Debug.Start("GoTo_Bluetooth")
    Debug.End()
# ----------------------------------------------------------------
def GoTo_Account(*args):
    """
        GoTo_Account:
        ===============
        Summary:
        --------
        This callback function is executed when the user presses
        on the Account button inside the navigation drawer.
        This should take them to the Account screen or an error
        pop up in case it fails for X reason.
    """
    Debug.Start("GoTo_Account")
    Debug.End()
# ----------------------------------------------------------------
def GoTo_Devices(*args):
    """
        GoTo_Devices:
        ===============
        Summary:
        --------
        This callback function is executed when the user presses
        on the Device button inside the navigation drawer.
        This should take them to the Device screen or an error
        pop up in case it fails for X reason.
    """
    Debug.Start("GoTo_Devices")
    Debug.End()
# ----------------------------------------------------------------
def GoTo_Network(*args):
    """
        GoTo_Network:
        ===============
        Summary:
        --------
        This callback function is executed when the user presses
        on the Network button inside the navigation drawer.
        This should take them to the Network screen or an error
        pop up in case it fails for X reason.
    """
    Debug.Start("GoTo_Network")
    Debug.End()
#====================================================================#
# Classes
#====================================================================#
LoadingLog.Class("DebugNavigationBar")
class DebugNavigationBar():
    """
        NavigationBar:
        ==============
        Summary:
        --------
        This class handles the application page's top navigation bar
        and navigation drawer for the main menus
    """
    #region ---------------------------------------------- Constructor
    LoadingLog.Method("__init__")
    def __init__(self, pageTitle:str = "", **kwargs):
        super(DebugNavigationBar, self).__init__(**kwargs)
        Debug.Start("DebugNavigationBar -> __init__")
        #region ------------------------------------------ WIDGETS
        Debug.Log("WIDGETS")
        self.NavDrawer = MDNavigationDrawer(pos_hint = {'top': 1, 'left': 0})
        self.DrawerLayout = MDBoxLayout(pos_hint = {'top': 1, 'left': 0})
        self.RecyleBoxLayout = RecycleBoxLayout(default_size=(None,56),
                                                default_size_hint=(1, None),
                                                size_hint=(1, None),
                                                orientation='vertical',
                                                spacing = 10)
        self.recycleView = MDRecycleView(pos_hint = {'top': 1, 'left': 0})
        #endregion
        #region ------------------------------------------ RecycleView
        Debug.Log("RecycleView")
        self.RecyleBoxLayout.bind(minimum_height=self.RecyleBoxLayout.setter("height"))
        self.recycleView.add_widget(self.RecyleBoxLayout)
        self.recycleView.viewclass = MDFillRoundFlatIconButton

        #region ----------------------------------------- FILLING
        Debug.Log("FILLING")
        self.recycleView.data = [{'icon': data["icon"],
                                  'font_style' : "H5",
                                   'on_release':data["function"],
                                   'text' : data["name"],
                                   'valign' : "center",
                                   'halign' : "left"}
                                    for data in SettingMenuButtons
                                    ]
        #endregion
        #endregion
        #region ------------------------------------------ NavDrawer
        Debug.Log("NavDrawer")
        self.NavDrawer.add_widget(MDIconButton(icon = "bug", halign = "center", icon_size = 60))
        self.NavDrawer.add_widget(self.recycleView)
        self.NavDrawer.orientation = "vertical"
        self.NavDrawer.elevation = Shadow.Elevation.default
        self.NavDrawer.shadow_softness = Shadow.Smoothness.default
        self.NavDrawer.shadow_radius = Shadow.Radius.default
        #endregion
        #region ------------------------------------------ ToolBar
        Debug.Log("Creating MDToolBar")
        self.ToolBar = MDTopAppBar(pos_hint = {'top': 1, 'left': 0})
        self.ToolBar.title = pageTitle
        self.ToolBar.headline_text = "Headline"
        self.ToolBar.anchor_title = "left"
        self.ToolBar.left_action_items = [["menu", lambda x: self.NavDrawer.set_state("open"), "Menu", "Overflow"]]
        self.ToolBar.elevation = Shadow.Elevation.default
        self.ToolBar.shadow_softness = Shadow.Smoothness.default
        self.ToolBar.shadow_radius = Shadow.Radius.default
        #endregion
        self.NavDrawer.set_state("close")
        Debug.End()
    #endregion
    #region -------------------------------------------------- Members
    LoadingLog.Member("ToolBar")
    ToolBar:MDTopAppBar = None

    LoadingLog.Member("NavDrawer")
    NavDrawer:MDNavigationDrawer = None
    #endregion
    #region -------------------------------------------------- Methods
    LoadingLog.Method("Callback")
    def Callback(self, *args):
        pass
    # ----------------------------------------------------------------
    #endregion
#====================================================================#
# Structure
#====================================================================#
LoadingLog.GlobalVariable("SettingMenuButtons")
SettingMenuButtons = [
    {
        "name" : _("Network"),
        "icon" : "wifi-cog",
        "function" : GoTo_Network
    },
    {
        "name" : _("Bluetooth"),
        "icon" : "bluetooth-settings",
        "function" : GoTo_Bluetooth
    },
    {
        "name" : _("Devices"),
        "icon" : "devices",
        "function" : GoTo_Devices
    },
    {
        "name" : _("BrSpand"),
        "icon" : "expansion-card-variant",
        "function" : GoTo_BrSpand
    },
    {
        "name" : _("Kontrol"),
        "icon" : "alpha-k",
        "function" : GoTo_Kontrol
    },
    {
        "name" : _("Account"),
        "icon" : "account-edit",
        "function" : GoTo_Account
    },
    {
        "name" : _("About"),
        "icon" : "help",
        "function" : GoTo_About
    },
    {
        "name" : _("Quit"),
        "icon" : "logout-variant",
        "function" : GoTo_Quit
    }
]
#====================================================================#
LoadingLog.End("Navigation.py")