#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("DriverMenu.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
import os
#endregion
#region --------------------------------------------------------- BRS
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import FilesFinder, AppendPath
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
from Libraries.BRS_Python_Libraries.BRS.GUI.Containers.cards import DriverCard
#endregion
#region -------------------------------------------------------- Kivy
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, CardTransition
#endregion
#region ------------------------------------------------------ KivyMD
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDTextButton
#endregion
#region ------------------------------------------------------ Kontrol
from ..Local.GUI.Navigation import AppNavigationBar
from ..Local.FileHandler.deviceDriver import GetDrivers, CheckIntegrity
#endregion
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class DriverMenu(Screen):
    """
        DriverMenu:
        -----------
        This class handles the screen of the driver menu which shows
        to the user their downloaded device drivers as selectable cards.
    """
    #region   --------------------------- MEMBERS
    ToolBar:AppNavigationBar = None
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("DriverMenu -> __init__")
        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
            Load the JSONs available, and create 1 profile card
            per available profiles.
        """
        Debug.Start("DriverMenu -> on_pre_enter")

        self.padding = 0
        self.spacing = 0

        #region ---------------------------- Layouts
        # self.TopLayout = MDBoxLayout(spacing=0, padding=(0,0,0,0), orientation="vertical")
        self.Layout = MDFloatLayout()
        # Create a horizontal box layout offset by half the screen to center the first profile in view.
        self.driversBox = MDBoxLayout(size_hint=(1,1), pos_hint = {'top': 1, 'left': 0}, orientation='horizontal', spacing="400sp", padding = (50,50,50,50), size_hint_x=None)
        self.driversBox.bind(minimum_width = self.driversBox.setter('width'))

        # Create the scroll view and add the box layout to it
        self.scroll = MDScrollView(pos_hint = {'top': 1, 'left': 0}, scroll_type=['bars','content'], size_hint = (1,1))
        self.scroll.smooth_scroll_end = 10

        # Add widgets
        self.scroll.add_widget(self.driversBox)
        #endregion
        #region ---------------------------- ToolBar
        self.ToolBar = AppNavigationBar(pageTitle=_("Devices Driver"))
        #endregion
        #region ---------------------------- Drivers
        path = AppendPath(os.getcwd(), "/Local/Drivers")
        drivers = GetDrivers()

        self.driversBox.add_widget(MDTextButton())

        for driver in drivers:
            card = DriverCard(AppendPath(path, f"/{driver}"),
                            AppendPath(path, f"/{driver}/Config.json"),
                            CheckIntegrity)
            self.driversBox.add_widget(card)

        # card = MDCard()
        # card.size_hint_min = (1000,1)
        # card.size_hint = (1,1)
        # card.add_widget(MDTextButton(text="WTF"))
        # self.driversBox.add_widget(card)
        # card = MDTextButton(text="WTF")
        # self.driversBox.add_widget(card)
        #endregion

        self.Layout.add_widget(self.scroll)
        self.Layout.add_widget(self.ToolBar.ToolBar)
        self.Layout.add_widget(self.ToolBar.NavDrawer)
        self.add_widget(self.Layout)
        Debug.End()
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            Function called when the screen is fully entered in view.
            In this case, once the view is fully loaded, the cards
            will slowly elevate to the wanted value.
        """
        Debug.Start("DriverMenu -> on_enter")
        Debug.End()
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            Function called before the screen is fully left. This gives
            us time to animate the screen leaving before destroying the
            objects and instances it created.
        """
        Debug.Start("DriverMenu -> on_pre_leave")
        Debug.End()
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully out of view.
        """
        Debug.Start("ProfileMenu -> on_leave")
        Debug.Log("Attempting to remove self from AppManager's widgets")
        self.clear_widgets()
        AppManager.manager.remove_widget(self)
        Debug.End()
        self.clear_widgets()
# ------------------------------------------------------------------------
    def _Animating(self, *args):
        """
            Call back function called each time an animation tick happens.
            We use it to add/remove the shadow of cards when entering or
            leaving the application.
        """
        pass
# ------------------------------------------------------------------------

LoadingLog.End("DriverMenu.py")