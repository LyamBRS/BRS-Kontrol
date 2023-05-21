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
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.networks import GetWifiIcon
from Libraries.BRS_Python_Libraries.BRS.Network.WiFi.WiFi import WiFiStatusUpdater
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
from kivy.uix.screenmanager import SlideTransition
from kivy.clock import Clock
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import("KivyMD")
from kivymd.uix.navigationdrawer import MDNavigationDrawer,MDNavigationDrawerDivider,MDNavigationDrawerHeader,MDNavigationDrawerItem,MDNavigationDrawerLabel,MDNavigationDrawerMenu,MDNavigationLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, OneLineListItem, OneLineIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.button import MDFillRoundFlatIconButton
#endregion
# LoadingLog.Import("Local")
#====================================================================#
# Functions
#====================================================================#
def GoTo_Network(*args):
    """
        GoTo_Network:
        =================
        Summary:
        --------
        This callback function is executed when the user presses
        on the Network button inside the navigation drawer.
        This should take them to the Network screen or an error
        pop up in case it fails for X reason.
    """
    Debug.Start("GoTo_Network")
    from ...Pages.NetworkMenu import NetworkMenu_Screens
    NetworkMenu_Screens._callerTransition = SlideTransition
    NetworkMenu_Screens._callerDirection = "right"
    NetworkMenu_Screens.Call()
    Debug.End()
# ----------------------------------------------------------------
def GoTo_Bluetooth(*args):
    """
        GoTo_Bluetooth:
        =================
        Summary:
        --------
        This callback function is executed when the user presses
        on the Bluetooth button inside the navigation drawer.
        This should take them to the Bluetooth screen or an error
        pop up in case it fails for X reason.
    """
    Debug.Start("GoTo_Bluetooth")
    from ...Pages.BluetoothMenu import BluetoothMenu_Screens
    BluetoothMenu_Screens._callerTransition = SlideTransition
    BluetoothMenu_Screens._callerDirection = "right"
    BluetoothMenu_Screens.Call()
    Debug.End()
# ----------------------------------------------------------------
def GoTo_Devices(*args):
    """
        GoTo_Devices:
        =================
        Summary:
        --------
        This callback function is executed when the user presses
        on the Devices button inside the navigation drawer.
        This should take them to the Devices screen or an error
        pop up in case it fails for X reason.
    """
    Debug.Start("GoTo_Devices")
    from ...Pages.DriverMenu import DriverMenu_Screens
    DriverMenu_Screens._callerTransition = SlideTransition
    DriverMenu_Screens._callerDirection = "right"
    DriverMenu_Screens.Call()
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
    from ...Pages.BrSpandMenu import BrSpandMenu_Screens
    BrSpandMenu_Screens._callerTransition = SlideTransition
    BrSpandMenu_Screens._callerDirection = "right"
    BrSpandMenu_Screens.Call()
    Debug.End()
# ----------------------------------------------------------------
def GoTo_Controls(*args):
    """
        GoTo_Controls:
        =================
        Summary:
        --------
        This callback function is executed when the user presses
        on the Controls button inside the navigation drawer.
        This should take them to the Controls screen or an error
        pop up in case it fails for X reason.
    """
    Debug.Start("GoTo_Controls")
    from ...Pages.ControlsMenu import ControlMenu_Screens
    ControlMenu_Screens._callerTransition = SlideTransition
    ControlMenu_Screens._callerDirection = "right"
    ControlMenu_Screens.Call()
    Debug.End()
# ----------------------------------------------------------------
def GoTo_Account(*args):
    """
        GoTo_Account:
        =============
        Summary:
        --------
        This callback function is executed when the user presses
        on the Account button inside the navigation drawer.
        This should take them to the Account screen or an error
        pop up in case it fails for X reason.
    """
    Debug.Start("GoTo_Account")
    from ...Pages.AccountMenu import AccountMenu_Screens
    AccountMenu_Screens._callerTransition = SlideTransition
    AccountMenu_Screens._callerDirection = "right"
    AccountMenu_Screens.Call()
    Debug.End()
# ----------------------------------------------------------------
def GoTo_About(*args):
    """
        GoTo_About:
        ===========
        Summary:
        --------
        This callback function is executed when the user presses
        on the About button inside the navigation drawer.
        This should take them to the About screen or an error
        pop up in case it fails for X reason.
    """
    Debug.Start("GoTo_About")
    from ...Pages.AboutMenu import AboutMenu_Screens
    AboutMenu_Screens._callerTransition = SlideTransition
    AboutMenu_Screens._callerDirection = "right"
    AboutMenu_Screens.Call()
    Debug.End()
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
    Debug.End()

#====================================================================#
# Classes
#====================================================================#
LoadingLog.Class("AppNavigationBar")
class AppNavigationBar():
    """
        NavigationBar:
        --------------
        This class handles the application page's top navigation bar
        and navigation drawer for the main menus (NOT DRIVERS)
    """
    #region ---------------------------------------------- Constructor
    LoadingLog.Method("__init__")
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
        self.ToolBar.right_action_items = [["earth-off", self.Callback, _("No internet")], ["wifi-strength-outline", self.Callback, _("No WiFi")]]

        self.UpdateNetworkIcons()

        self.ToolBar.elevation = Shadow.Elevation.default
        self.ToolBar.shadow_softness = Shadow.Smoothness.default
        self.ToolBar.shadow_radius = Shadow.Radius.default

        Clock.schedule_once(self.UpdateNetworkIcons, 0)

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

    def UpdateNetworkIcons(self, *args):
        """
            UpdateNetworkIcons:
            ===================
            Summary:
            --------
            Callback function executed each 5 seconds
            that attempts to update the icons displayed
            in the toolbar that says if we have internet
            access.
        """
        try:
            networkInfo = WiFiStatusUpdater.GetConnectionStatus()

            networkName:str = networkInfo[0]
            hasInternet:bool = networkInfo[1]
            signalStrength:int = networkInfo[2]

            internetIcon:str = "web-off"
            internetToolTip:str = _("No internet")
            wifiIcon:str = "wifi-strength-outline"
            wifiToolTip:str = _("No wifi")

            if(hasInternet):
                internetIcon = "web-check"
                internetToolTip = _("Internet connected")

            if(networkName != "ERROR"):

                if(networkName == None or networkName == ""):
                    wifiIcon = "wifi-strength-off-outline"
                    wifiToolTip = _("WiFi disconnected")
                else:
                    wifiToolTip = networkName
                    wifiIcon = GetWifiIcon(signalStrength, None)
            else:
                internetIcon = "web-cancel"
                wifiIcon = "wifi-cancel"
                wifiToolTip = _("error")
                internetToolTip = _("error")

            self.ToolBar.right_action_items = [[internetIcon, self.Callback, internetToolTip], [wifiIcon, self.Callback, wifiToolTip]]
            Clock.schedule_once(self.UpdateNetworkIcons, 5)
        except:
            Debug.Error("TOOLBAR ERROR FAILED TO ADD RIGHT ICON WIDGETS")
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
        "name" : _("Controls & Keybinds"),
        "icon" : "controller",
        "function" : GoTo_Controls
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
        "icon" : "power",
        "function" : GoTo_Quit
    }
]
#====================================================================#
LoadingLog.End("Navigation.py")