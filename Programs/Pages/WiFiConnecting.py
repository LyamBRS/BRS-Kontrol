#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
LoadingLog.Start("WiFiConnecting.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
from Libraries.BRS_Python_Libraries.BRS.Network.WiFi.WiFi import Linux_ConnectWiFi, Linux_VerifyInternetConnection
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.clock import Clock
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import("KivyMD")
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.progressbar import MDProgressBar
#endregion
#region ------------------------------------------------------ Kontrol
LoadingLog.Import("Local")
from ..Pages.PopUps import PopUpsHandler, PopUps_Screens, PopUpTypeEnum
from ..Pages.DriverMenu import DriverMenu_Screens
from ..Local.Hardware.RGB import KontrolRGB
#endregion
#====================================================================#
# thread class
#====================================================================#

#====================================================================#
# Screen class
#====================================================================#

LoadingLog.Class("WiFiConnecting_Screens")
class WiFiConnecting_Screens:
    """
        WiFiConnecting_Screens:
        ================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`DriverMenu`.

        Description:
        ------------
        This class holds the different types of callers of the AppLoading
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

    _ssid:str = None
    _password:str = None

    currentSSIDAttempt:int = 0
    currentInternetAttempt:int = 0
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
        WiFiConnecting_Screens._exitClass = screenClass
        WiFiConnecting_Screens._exitName  = screenName

        WiFiConnecting_Screens._exitTransition = transition
        WiFiConnecting_Screens._exitDuration = duration
        WiFiConnecting_Screens._exitDirection = direction
        return False

    def SetCaller(screenClass, screenName:str, ssid:str, password:str, transition=SlideTransition,  duration:float=0, direction:str="down") -> bool:
        """
            SetCaller:
            ==========
            Summary:
            --------
            Function which sets the screen to load if an error occured. This is used to "go back" to whoever attempted
            to call this screen.

            Args:
            -----
                `downloadName (str)`: name of the download
                `downloadFunction (str)`: Function which will be executed to download whatever. NEEDS A CALLBACK FUNCTION AS INPUT PARAMETER.
                `screenClass (_type_)`: The screen class of the screen that wants to transition to this one.
                `screenName (str)`: The name of the screen class. It needs to be the same as :ref:`screenClass`.
                `transition`: Optional kivy transition class. Defaults as `WipeTransition`
                `duration (float)`: Optional specification of the transition's duration. Defaults to 0.5 seconds
                `direction (str)`: Optional direction which the transition should go. Defaults as `"up"`.

            Returns:
                bool: `True`: Something went wrong. `False`: Success
        """
        # Attempt to add the screen class as a widget of the AppManager
        WiFiConnecting_Screens._callerClass = screenClass
        WiFiConnecting_Screens._callerName  = screenName

        WiFiConnecting_Screens._ssid = ssid
        WiFiConnecting_Screens._password = password

        WiFiConnecting_Screens._callerTransition = transition
        WiFiConnecting_Screens._callerDuration = duration
        WiFiConnecting_Screens._callerDirection = direction
        return False

    def _Exit(*args) -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("WiFiConnecting_Screens -> _Exit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(WiFiConnecting_Screens._exitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(WiFiConnecting_Screens._exitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                WiFiConnecting_Screens._exitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(WiFiConnecting_Screens._exitClass(name=WiFiConnecting_Screens._exitName))
        except:
            Debug.Error("AppLoading -> Exception occured.")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = WiFiConnecting_Screens._exitTransition()
        AppManager.manager.transition.duration = WiFiConnecting_Screens._exitDuration
        AppManager.manager.transition.direction = WiFiConnecting_Screens._exitDirection

        # try:
        AppManager.manager.current = WiFiConnecting_Screens._exitName
        # except:
            # return True
        Debug.End()
        return False

    def Call(*args) -> bool:
        """
            Attempt to go to the main screen that is being handled by this class.

            Returns:
                bool: `True`:  Something went wrong and the screen can't be loaded. `False`: Success
        """
        Debug.Start("WiFiConnecting_Screens -> Call()")

        WiFiConnecting_Screens.currentSSIDAttempt = 0
        WiFiConnecting_Screens.currentInternetAttempt = 0

        # Attempt to add the screen class as a widget of the AppManager
        # try:
        # Check if caller class was specified
        Debug.Log("Checking caller class")
        if(WiFiConnecting_Screens._callerClass == None):
            Debug.Error("No caller class specified.")
            Debug.End()
            return True

        Debug.Log("Checking caller name")
        if(WiFiConnecting_Screens._callerName == None):
            Debug.Error("No caller name specified.")
            Debug.End()
            return True

        Debug.Log("Attempting to add widget")
        AppManager.manager.add_widget(WiFiConnecting(name="WiFiConnecting"))
        # except:
        Debug.Error("Exception occured while handling Call()")
        Debug.End()
            # return True

        # Attempt to call the added screen
        AppManager.manager.transition = WiFiConnecting_Screens._callerTransition()
        AppManager.manager.transition.duration = WiFiConnecting_Screens._callerDuration
        AppManager.manager.transition.direction = WiFiConnecting_Screens._callerDirection

        # try:
        AppManager.manager.current = "WiFiConnecting"
        Debug.Log("Screen successfully changed")
        # except:
            # Debug.Error("Failed to add WiFiConnecting as current screen.")
            # Debug.End()
            # return True
        Debug.End()
        return False
    #endregion

#====================================================================#
# Classes
#====================================================================#

LoadingLog.Class("WiFiConnecting")
class WiFiConnecting(Screen):
    """
        WiFiConnecting:
        =================
        Summary
        -------
        Screen class handling the construction and deleting of a
        download screen which displays the current download time
        left to a download function through callbacks and threadings.
    """
    #region   --------------------------- MEMBERS
    progressBar:MDProgressBar = None
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
        Debug.Start("WiFiConnecting -> on_pre_enter")

        self.padding = 0
        self.spacing = 0

        #region ---- Background
        import os
        from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
        from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
        path = os.getcwd()
        background = GetBackgroundImage(AppendPath(path, "/Libraries/Backgrounds/Login/Dark.png"),
                                        AppendPath(path, "/Libraries/Backgrounds/Login/Light.png"))
        #endregion

        #region ---------------------------- Layouts
        self.Layout = MDBoxLayout()
        self.Layout.orientation = "vertical"
        #endregion

        #region ---------------------------- Spinner
        self.spinner = MDSpinner()
        self.spinner.size_hint = (0.25, 0.25)
        self.spinner.pos_hint = {"center_x":0.5, "center_y":0.5}
        self.spinner.line_width = 5
        #endregion

        #region ---------------------------- Label
        self.WhatsHappenningLabel = MDLabel(halign = "center", pos_hint = {'center_x': 0.5,'center_y': 0.125}, size_hint = (1, 0.25))
        self.WhatsHappenningLabel.font_style = "H5"
        #endregion

        Clock.schedule_once(self.CheckCurrentWiFi, 1)

        self.add_widget(background)
        self.Layout.add_widget(self.spinner)
        self.Layout.add_widget(self.WhatsHappenningLabel)
        self.add_widget(self.Layout)
        Debug.End()
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            Function called when the screen is fully entered in view.
            In this case, once the view is fully loaded, the cards
            will slowly elevate to the wanted value.
        """
        Debug.Start("WiFiConnecting -> on_enter")
        KontrolRGB.ApploadingAnimation()
        Debug.Log("Starting WiFi threads")

        Linux_ConnectWiFi.StartConnecting(WiFiConnecting_Screens._ssid, WiFiConnecting_Screens._password)
        Linux_VerifyInternetConnection.StartPinging()
        Clock.schedule_once(self.CheckCurrentWiFi, 1)

        Debug.End()
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            Function called before the screen is fully left. This gives
            us time to animate the screen leaving before destroying the
            objects and instances it created.
        """
        Debug.Start("WiFiConnecting -> on_pre_leave")
        Debug.End()
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully out of view.
        """
        Debug.Start("WiFiConnecting -> on_leave")
        Debug.Log("Attempting to remove self from AppManager's widgets")
        self.clear_widgets()
        AppManager.manager.remove_widget(self)

        Linux_ConnectWiFi.StopConnecting()
        Linux_VerifyInternetConnection.StopPinging()
        Debug.End()
        self.clear_widgets()
# ------------------------------------------------------------------------
    def CheckCurrentWiFi(self, *args):
        """
            CheckCurrentWiFi
            =============
            Summary:
            --------
            Checks if the current WiFi has internet
            access and connects at all.
        """
        # Debug.Start("CheckCurrentWiFi")

        internetConnection = Linux_VerifyInternetConnection.GetConnectionStatus()
        ssidConnection = Linux_ConnectWiFi.GetConnectionStatus()

        if(ssidConnection[0] == True):
            if(internetConnection[0] == False):
                self.WhatsHappenningLabel.text = f"[{WiFiConnecting_Screens.currentInternetAttempt} / 10] " + _("Time taken to connect to the internet") + f": {internetConnection[2]} seconds"
                WiFiConnecting_Screens.currentInternetAttempt = WiFiConnecting_Screens.currentInternetAttempt + 1
                if(WiFiConnecting_Screens.currentInternetAttempt > 10):
                    Information.CanUse.Internet = False
                    Information.CanUse.WiFi = True
                    PopUpsHandler.Clear()
                    PopUpsHandler.Add(PopUpTypeEnum.FatalError,
                                    Message=_("Failed to connect to the internet after") + f" {internetConnection[2]} " + _("seconds") + ". " + _("The wifi is connected successfully but does not provide internet access."))
                    PopUps_Screens.SetCaller(DriverMenu_Screens, "DriverMenu")
                    PopUps_Screens.SetExiter(DriverMenu_Screens, "DriverMenu")
                    PopUps_Screens.Call()

                    Linux_ConnectWiFi.StopConnecting()
                    Linux_VerifyInternetConnection.StopPinging()
                    return
            else:
                PopUpsHandler.Clear()
                PopUpsHandler.Add(PopUpTypeEnum.Remark,
                                Message=_("Successfully connected to, and verified internet access of") + ": " + WiFiConnecting_Screens._ssid)
                PopUps_Screens.SetCaller(DriverMenu_Screens, "DriverMenu")
                PopUps_Screens.SetExiter(DriverMenu_Screens, "DriverMenu")
                PopUps_Screens.Call()
                Information.CanUse.Internet = True
                Information.CanUse.WiFi = True

                Linux_ConnectWiFi.StopConnecting()
                Linux_VerifyInternetConnection.StopPinging()
                return
        else:
            self.WhatsHappenningLabel.text = f"[{WiFiConnecting_Screens.currentSSIDAttempt} / 120] " + _("Time taken to connect to") + " " + WiFiConnecting_Screens._ssid + f": {ssidConnection[2]} seconds"
            WiFiConnecting_Screens.currentSSIDAttempt = WiFiConnecting_Screens.currentSSIDAttempt + 1
            if(WiFiConnecting_Screens.currentSSIDAttempt > 120):
                PopUpsHandler.Clear()
                PopUpsHandler.Add(PopUpTypeEnum.FatalError,
                                  Message=_("Failed to connect to") + ": " + WiFiConnecting_Screens._ssid + " " + _("after") + f" {ssidConnection[2]} " + _("seconds"))
                PopUps_Screens.SetCaller(DriverMenu_Screens, "DriverMenu")
                PopUps_Screens.SetExiter(DriverMenu_Screens, "DriverMenu")
                PopUps_Screens.Call()

                Information.CanUse.Internet = False
                Information.CanUse.WiFi = False

                Linux_ConnectWiFi.StopConnecting()
                Linux_VerifyInternetConnection.StopPinging()
                return

        Clock.schedule_once(self.CheckCurrentWiFi, 1)
        # Debug.End()
LoadingLog.End("DriverMenu.py")