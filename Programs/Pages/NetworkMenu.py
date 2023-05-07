#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Libraries.BRS_Python_Libraries.BRS.GUI.Status.WiFi import GetWiFiNotAvailableCard, WiFiSelectionCard
from Libraries.BRS_Python_Libraries.BRS.Network.WiFi.WiFi import CanDeviceUseWiFi, GetWiFiNetworks
LoadingLog.Start("NetworkMenu.py")
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
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import FilesFinder, AppendPath
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
from Libraries.BRS_Python_Libraries.BRS.GUI.Containers.cards import DriverCard
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, CardTransition, SlideTransition
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import("KivyMD")
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDTextButton
from kivy.animation import Animation
#endregion
#region ------------------------------------------------------ Kontrol
LoadingLog.Import("Local")
from ..Local.GUI.Navigation import AppNavigationBar
from ..Local.GUI.Cards import ButtonCard, DeviceDriverCard
from ..Local.FileHandler.deviceDriver import GetDrivers, CheckIntegrity
#endregion
#====================================================================#
# Functions
#====================================================================#
#====================================================================#
# Screen class
#====================================================================#
LoadingLog.Class("NetworkMenu_Screens")
class NetworkMenu_Screens:
    """
        NetworkMenu_Screens:
        ================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`NetworkMenu`.

        Description:
        ------------
        This class holds the different types of callers of the NetworkMenu
        screen as well as the different exit screens that this transitional
        screen can go to. You must specify the names of the wanted exit screens
        prior to calling the transition function.

        An exit screen is basically which screens should be loaded if something
        happens in the transition screen.
    """
    #region ---- Members
    _exitClass = None
    _callerClass = None

    _callerName = None
    _exitName = None

    _callerTransition = SlideTransition
    _exitTransition = SlideTransition

    _callerDirection = "up"
    _exitDirection = "up"

    _callerDuration = 0.5
    _exitDuration = 0.5
    #endregion
    #region ---- Methods
    def SetExiter(screenClass, screenName:str, transition=SlideTransition, duration:float=0, direction:str="up") -> bool:
        """
            Function which sets the screen that this screen should transition to on exit.
            This allows transitional screens to be reused by any screens at any time.

            Args:
                `screenClass (_type_)`: The screen class of the screen this handler should transition to on exit.
                `screenName (str)`: The name of the screen class. It needs to be the same as :ref:`screenClass`.
                `transition`: Optional kivy transition class. Defaults as `WipeTransition`
                `duration (float)`: Optional specification of the transition's duration. Defaults to 0.5 seconds
                `direction (str)`: Optional direction which the transition should go. Defaults as `"up"`.

            Returns:
                bool: `True`: Something went wrong. `False`: Success
        """
        # Attempt to add the screen class as a widget of the AppManager
        NetworkMenu_Screens._exitClass = screenClass
        NetworkMenu_Screens._exitName  = screenName

        NetworkMenu_Screens._exitTransition = transition
        NetworkMenu_Screens._exitDuration = duration
        NetworkMenu_Screens._exitDirection = direction
        return False

    def SetCaller(screenClass, screenName:str, transition=SlideTransition, duration:float=0, direction:str="up") -> bool:
        """
            Function which sets the screen to load if an error occured. This is used to "go back" to whoever attempted
            to call this screen.

            Args:
                `screenClass (_type_)`: The screen class of the screen that wants to transition to this one.
                `screenName (str)`: The name of the screen class. It needs to be the same as :ref:`screenClass`.
                `transition`: Optional kivy transition class. Defaults as `WipeTransition`
                `duration (float)`: Optional specification of the transition's duration. Defaults to 0.5 seconds
                `direction (str)`: Optional direction which the transition should go. Defaults as `"up"`.

            Returns:
                bool: `True`: Something went wrong. `False`: Success
        """
        # Attempt to add the screen class as a widget of the AppManager
        NetworkMenu_Screens._callerClass = screenClass
        NetworkMenu_Screens._callerName  = screenName

        NetworkMenu_Screens._callerTransition = transition
        NetworkMenu_Screens._callerDuration = duration
        NetworkMenu_Screens._callerDirection = direction
        return False

    def _Exit() -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("NetworkMenu_Screens -> _Exit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(NetworkMenu_Screens._exitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(NetworkMenu_Screens._exitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                NetworkMenu_Screens._exitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(NetworkMenu_Screens._exitClass(name=NetworkMenu_Screens._exitName))
        except:
            Debug.Error("NetworkMenu_Screens -> Exception occured.")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = NetworkMenu_Screens._exitTransition()
        AppManager.manager.transition.duration = NetworkMenu_Screens._exitDuration
        AppManager.manager.transition.direction = NetworkMenu_Screens._exitDirection

        # try:
        AppManager.manager.current = NetworkMenu_Screens._exitName
        # except:
            # return True
        Debug.End()
        return False

    def Call() -> bool:
        """
            Attempt to go to the main screen that is being handled by this class.

            Returns:
                bool: `True`:  Something went wrong and the screen can't be loaded. `False`: Success
        """
        Debug.Start("NetworkMenu_Screens -> Call()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if caller class was specified
            # Debug.Log("Checking caller class")
            # if(AccountMenu_Screens._callerClass == None):
                # Debug.Error("No caller class specified.")
                # Debug.End()
                # return True

            # Debug.Log("Checking caller name")
            # if(AccountMenu_Screens._callerName == None):
                # Debug.Error("No caller name specified.")
                # Debug.End()
                # return True

            Debug.Log("Attempting to add widget")
            AppManager.manager.add_widget(NetworkMenu(name="NetworkMenu"))
        except:
            Debug.Error("Exception occured while handling Call()")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = NetworkMenu_Screens._callerTransition()
        AppManager.manager.transition.duration = NetworkMenu_Screens._callerDuration
        AppManager.manager.transition.direction = NetworkMenu_Screens._callerDirection

        # try:
        AppManager.manager.current = "NetworkMenu"
        Debug.Log("Screen successfully changed")
        # except:
            # Debug.Error("Failed to add AppLoading as current screen.")
            # Debug.End()
            # return True
        Debug.End()
        return False
    #endregion
#====================================================================#
# Classes
#====================================================================#
LoadingLog.Class("NetworkMenu")
class NetworkMenu(Screen):
    """
        NetworkMenu:
        -----------
        This class handles the screen of the WiFi Selection which shows
        to the user some actions that they can do with the WiFi
    """
    #region   --------------------------- MEMBERS
    ToolBar:AppNavigationBar = None
    continueToUpdateWiFis:bool = False
    """
        continueToUpdateWiFis:
        ======================
        Summary:
        --------
        If `True`: the clock scheduler function will keep
        executing the function that updates wifis. otherwise,
        it will stop rescheduling itself.

        Defaults to `False`
    """
    WiFiObjectList:list = None
    """
        WiFiObjectList:
        ===============
        Summary:
        --------
        List of dictionaries of WiFi created.

        Dictionary layout:
        ------------------
        - `{"name": "ssid", "object": WiFiSelectionCard}`
    """
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("NetworkMenu -> __init__")
        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
        """
        Debug.Start("NetworkMenu -> on_pre_enter")

        self.padding = 0
        self.spacing = 0

        #region ---- Background
        import os
        from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
        from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
        path = os.getcwd()

        background = GetBackgroundImage(AppendPath(path, "/Libraries/Backgrounds/Menus/Dark.png"),
                                        AppendPath(path, "/Libraries/Backgrounds/Menus/Light.png"))
        #endregion

        #region ---------------------------- Layouts
        self.Layout = MDFloatLayout()
        # Create a horizontal box layout offset by half the screen to center the first profile in view.
        self.cardBox = MDBoxLayout(size_hint=(1,1), pos_hint = {'top': -1, 'left': 0}, orientation='vertical', spacing="50sp", padding = (50,100,50,50), size_hint_y=None)
        self.cardBox.bind(minimum_height = self.cardBox.setter('height'))

        # Create the scroll view and add the box layout to it
        self.scroll = MDScrollView(pos_hint = {'top': -1, 'left': 0}, scroll_type=['bars','content'], size_hint = (1,1))
        self.scroll.smooth_scroll_end = 10

        # Add widgets
        self.scroll.add_widget(self.cardBox)
        #endregion
        #region ---------------------------- ToolBar
        self.ToolBar = AppNavigationBar(pageTitle=_("Network Parameters"))
        #endregion

        self.add_widget(background)
        self.Layout.add_widget(self.scroll)
        self.Layout.add_widget(self.ToolBar.ToolBar)
        self.NoWiFiCard = GetWiFiNotAvailableCard(_("Failed to get wireless WiFi networks. Your device may not support WiFi. Please use Ethernet if available."))
        self.Layout.add_widget(self.NoWiFiCard)
        self.Layout.add_widget(self.ToolBar.NavDrawer)
        self.add_widget(self.Layout)

        self.continueToUpdateWiFis = False
        Debug.End()
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            Function called when the screen is fully entered in view.
            In this case, once the view is fully loaded, the cards
            will slowly elevate to the wanted value.
        """
        Debug.Start("NetworkMenu -> on_enter")

        Debug.Log("Trying to access WiFi interfaces")
        result = CanDeviceUseWiFi()

        if(result != True):
            Debug.Log("WiFi networks cannot be accessed.")
            anim = Animation(pos_hint = {"center_x":0.5, "center_y":0.45}, t="in_out_back")
            anim.start(self.NoWiFiCard)
        else:
            Debug.Log("Wifi can be accessed")
            Debug.Log("Getting WiFi networks")
            networks = GetWiFiNetworks()

            Debug.Log("Creating WiFi network cards.")
            for network in networks:
                WiFiCard = WiFiSelectionCard(network)
                self.cardBox.add_widget(WiFiCard)

        Clock.schedule_once(self.UpdateWiFis, 10)
        self.continueToUpdateWiFis = True

        self.animation2 = Animation(pos_hint = {'top': 1, 'left': 0}, t="out_sine", duration = 1)
        self.animation2.start(self.cardBox)

        self.animation = Animation(pos_hint = {'top': 1, 'left': 0}, t="out_sine", duration = 1)
        self.animation.start(self.scroll)

        Debug.End()
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            Function called before the screen is fully left. This gives
            us time to animate the screen leaving before destroying the
            objects and instances it created.
        """
        Debug.Start("NetworkMenu -> on_pre_leave")
        self.continueToUpdateWiFis = False
        Debug.End()
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully out of view.
        """
        Debug.Start("NetworkMenu -> on_leave")
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
    def UpdateWiFis(self, *args):
        """
            UpdateWiFis:
            ============
            Summary:
            --------
            This function updates the displayed WiFis with a list
            of new WiFis each 10 seconds.
        """
        Debug.Start("UpdateWiFis")

        if(self.continueToUpdateWiFis == True):
            Clock.schedule_once(self.UpdateWiFis, 10)

        Debug.End()
LoadingLog.End("NetworkMenu.py")