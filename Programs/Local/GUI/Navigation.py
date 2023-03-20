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
#endregion
#region --------------------------------------------------------- BRS
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Shadow
#endregion
#region -------------------------------------------------------- Kivy
#endregion
#region ------------------------------------------------------ KivyMD
from kivymd.uix.navigationdrawer import MDNavigationDrawer,MDNavigationDrawerDivider,MDNavigationDrawerHeader,MDNavigationDrawerItem,MDNavigationDrawerLabel,MDNavigationDrawerMenu,MDNavigationLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, OneLineListItem, OneLineIconListItem
#endregion
#====================================================================#
# Functions
#====================================================================#

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

        self.NavDrawer = MDNavigationDrawer()

        # Add a list to the navigation drawer
        nav_list = MDList()
        nav_list.orientation = "tb-rl"
        
        nav_list.add_widget(OneLineIconListItem(text="Option 1"))
        nav_list.add_widget(OneLineIconListItem(text="Option 2"))
        nav_list.add_widget(OneLineIconListItem(text="Option 3"))
        nav_list.add_widget(OneLineIconListItem(text="Option 4"))
        self.NavDrawer.add_widget(nav_list)
        self.NavDrawer.orientation = "vertical"
        self.NavDrawer.elevation = Shadow.Elevation.default
        self.NavDrawer.shadow_softness = Shadow.Smoothness.default
        self.NavDrawer.shadow_radius = Shadow.Radius.default

        Debug.Log("Creating MDToolBar")
        self.ToolBar = MDTopAppBar()
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