#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Libraries.BRS_Python_Libraries.BRS.Network.WiFi.WiFi import ConnectToAWiFiNetwork
from Programs.Local.FileHandler.Profiles import ProfileHandler
from Programs.Local.Hardware.RGB import KontrolRGB
from Programs.Pages.DriverMenu import DriverMenu_Screens
LoadingLog.Start("WiFiLogin.py")
#====================================================================#
# Imports
#====================================================================#
import os
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen, SlideTransition
# -------------------------------------------------------------------
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from Libraries.BRS_Python_Libraries.BRS.GUI.Inputs.textfield import VirtualKeyboardTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
# -------------------------------------------------------------------
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Shadow
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Rounding,Shadow
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
from Programs.Pages.WiFiConnecting import WiFiConnecting_Screens
# -------------------------------------------------------------------
from .PopUps import PopUpTypeEnum, PopUpsHandler,PopUps_Screens
#====================================================================#
# Functions
#====================================================================#
#====================================================================#
# Screen class
#====================================================================#
LoadingLog.Log("WiFiLogin_Screens")
class WiFiLogin_Screens:
    """
        WiFiLogin_Screens:
        ================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`WiFiLogin`.

        Description:
        ------------
        This class holds the different types of callers of the PopUps
        screen as well as the different exit screens that this transitional
        screen can go to. You must specify the names of the wanted exit screens
        prior to calling the transition function.

        An exit screen is basically which screens should be loaded if something
        happens in the transition screen.

        Members:
        ------------
        This class contains the following screens:
        - `caller:str = ""`: The name of the screen which called this one.
        - `SetExiter(screenClass,screenName:str) -> bool`: set the screen to go to on exit. Returns `True` if an error occured
        - `Call() -> bool`: Attempt to go to the specified screen. Returns `True` if an error occured.
    """
    #region ---- Members
    _callerClass = None
    _goodExitClass = None
    _badExitClass = None

    _callerName = None
    _goodExitName = None
    _badExitName = None

    _callerTransition = SlideTransition
    _goodExitTransition = SlideTransition
    _badExitTransition = SlideTransition

    _callerDirection = "up"
    _goodExitDirection = "up"
    _badExitDirection = "down"

    _callerDuration = 0.5
    _goodExitDuration = 0.5
    _badExitDuration = 0.5

    savedSSID = ""
    """
        savedSSID:
        ==========
        Summary:
        --------
        This member holds which SSID to use for
        the WiFi connection attempt.
        This is set in the `SetCaller` method.
    """
    #endregion
    #region ---- Methods
    def SetGoodExiter(screenClass, screenName:str, transition=SlideTransition, duration:float=0.5, direction:str="up") -> bool:
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
        WiFiLogin_Screens._goodExitClass = screenClass
        WiFiLogin_Screens._goodExitName  = screenName

        WiFiLogin_Screens._goodExitTransition = transition
        WiFiLogin_Screens._goodExitDuration = duration
        WiFiLogin_Screens._goodExitDirection = direction
        return False

    def SetBadExiter(screenClass, screenName:str, transition=SlideTransition, duration:float=0.5, direction:str="up") -> bool:
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
        WiFiLogin_Screens._badExitClass = screenClass
        WiFiLogin_Screens._badExitName  = screenName

        WiFiLogin_Screens._badExitTransition = transition
        WiFiLogin_Screens._badExitDuration = duration
        WiFiLogin_Screens._badExitDirection = direction
        return False

    def SetCaller(screenClass, screenName:str, ssid:str,  transition=SlideTransition, duration:float=0.5, direction:str="up") -> bool:
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
        WiFiLogin_Screens._callerClass = screenClass
        WiFiLogin_Screens._callerName  = screenName

        WiFiLogin_Screens._callerTransition = transition
        WiFiLogin_Screens._callerDuration = duration
        WiFiLogin_Screens._callerDirection = direction

        WiFiLogin_Screens.savedSSID = ssid
        return False

    def _BadExit(*args) -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetBadExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("WiFiLogin -> _BadExit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(WiFiLogin_Screens._badExitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(WiFiLogin_Screens._badExitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                WiFiLogin_Screens._badExitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(WiFiLogin_Screens._badExitClass(name=WiFiLogin_Screens._badExitName))
        except:
            Debug.Error("PopUps: _Exit() -> Failed in add_widget")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = WiFiLogin_Screens._badExitTransition()
        AppManager.manager.transition.duration = WiFiLogin_Screens._badExitDuration
        AppManager.manager.transition.direction = WiFiLogin_Screens._badExitDirection

        # try:
        AppManager.manager.current = WiFiLogin_Screens._badExitName
        # except:
            # Debug.Error("Startup_Screens: _Exit() -> AppManager.manager.current FAILED")
            # Debug.End()
            # return True
        Debug.End()
        return False

    def _GoodExit(*args) -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetGoodExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("WiFiLogin -> _GoodExit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(WiFiLogin_Screens._goodExitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(WiFiLogin_Screens._goodExitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                WiFiLogin_Screens._goodExitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(WiFiLogin_Screens._goodExitClass(name=WiFiLogin_Screens._goodExitName))
        except:
            Debug.Error("PopUps: _Exit() -> Failed in add_widget")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = WiFiLogin_Screens._goodExitTransition()
        AppManager.manager.transition.duration = WiFiLogin_Screens._goodExitDuration
        AppManager.manager.transition.direction = WiFiLogin_Screens._goodExitDirection

        # try:
        AppManager.manager.current = WiFiLogin_Screens._goodExitName
        # except:
            # Debug.Error("Startup_Screens: _Exit() -> AppManager.manager.current FAILED")
            # Debug.End()
            # return True
        Debug.End()
        return False

    def Call(*args) -> bool:
        """
            Attempt to go to the main screen that is being handled by this class.

            Returns:
                bool: `True`:  Something went wrong and the screen can't be loaded. `False`: Success
        """
        Debug.Start("WiFiLogin -> Call")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking caller class")
            if(WiFiLogin_Screens._callerClass == None):
                Debug.Error("No caller class specified.")
                Debug.End()
                return True

            Debug.Log("Checking caller name")
            if(WiFiLogin_Screens._callerName == None):
                Debug.Error("No caller name specified.")
                Debug.End()
                return True

            Debug.Log("Adding widget")
            AppManager.manager.add_widget(WiFiLogin(name="WiFiLogin"))
        except:
            Debug.Error("Exception occured while handling Call()")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = WiFiLogin_Screens._callerTransition()
        AppManager.manager.transition.duration = WiFiLogin_Screens._callerDuration
        AppManager.manager.transition.direction = WiFiLogin_Screens._callerDirection

        # try:
        AppManager.manager.current = "WiFiLogin"
        # except:
            # Debug.Error("Failed to add WiFiLogin as current screen.")
            # Debug.End()
            # return True

        Debug.End()
        return False
    #endregion

#====================================================================#
# Classes
#====================================================================#
class WiFiLogin(Screen):
    #region   --------------------------- MEMBERS
    progress = 0
    """The animation's progress from 0 to 1"""
    animation = Animation()
    """Animation object"""
    elevation = 0
    softness = 0
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("WiFiLogin")
        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
            on_pre_enter:
            =============
            Summary:
            -------
            Builds the WiFi login screen entirely.
            The login screen consists of a "ConnectButton" message as well as
            a card containing an SSID and password textfields.

            The login screen consists of a card with "login" written above it.
            The card contains a confirm and a cancel button as well as
            2 fields labeled SSID and password.

            username is set by default.
        """

        #region ---- Background
        from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
        from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
        path = os.getcwd()

        background = GetBackgroundImage(AppendPath(path, "/Libraries/Backgrounds/Login/Dark.png"),
                                        AppendPath(path, "/Libraries/Backgrounds/Login/Light.png"))
        #endregion

        self.padding = 25
        self.spacing = 25

        # ConnectButton card
        self.MainLayout = MDBoxLayout(spacing=10, padding=50, orientation="vertical")
        self.Card = MDCard(
                            elevation = Shadow.Elevation.default,
                            shadow_softness = Shadow.Smoothness.default,
                            radius=Rounding.default,
                            padding = 25,
                            orientation = "vertical"
                            )

        self.LockIcon = MDIconButton(text="lock", icon="wifi-lock", halign = "center", disabled=True)
        self.LockIcon.icon_size = "100sp"
        self.LockIcon.pos_hint={"center_x": 0.5, "center_y": 0.5}
        self.Password = VirtualKeyboardTextField()
        self.Password.font_size = 30
        self.Password.hint_text = _("Password")

        self.SSIDTextField = VirtualKeyboardTextField()
        self.SSIDTextField.font_size = 30
        self.SSIDTextField.hint_text = _("SSID")
        self.SSIDTextField.text = WiFiLogin_Screens.savedSSID

        # Button Layout
        self.ButtonLayout = MDBoxLayout(spacing=20)
        self.CancelLayout = MDFloatLayout()
        self.LoginLayout = MDFloatLayout()

        self.ConnectButton = MDIconButton(text="check", icon="check")
        self.CancelButton = MDIconButton(text="close-circle", icon="close-circle")
        self.ConnectButton.icon_size = "100sp"
        self.CancelButton.icon_size = "100sp"
        self.ConnectButton.pos_hint={"center_x": 0.5, "center_y": 0.5}
        self.CancelButton.pos_hint={"center_x": 0.5, "center_y": 0.5}

        # Set back function
        self.CancelButton.on_release = self.CancelConnection
        self.ConnectButton.on_release = self.TryToConnect

        # Add widgets
        self.add_widget(background)
        self.CancelLayout.add_widget(self.CancelButton)
        self.LoginLayout.add_widget(self.ConnectButton)
        self.ButtonLayout.add_widget(self.LoginLayout)
        self.ButtonLayout.add_widget(self.CancelLayout)

        self.Card.add_widget(self.LockIcon)
        self.Card.add_widget(self.SSIDTextField)
        self.Card.add_widget(self.Password)
        self.Card.add_widget(self.ButtonLayout)

        self.MainLayout.add_widget(self.Card)
        self.add_widget(self.MainLayout)
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            Animate all the widgets into view once the screen is fully present.
        """
        KontrolRGB.DisplayDefaultColor()

        password = ProfileHandler.GetSavedSSIDPassword(self.SSIDTextField.text)
        if(password != None):
            self.Password.text = password

        pass
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            on_leave:
            =========
            Summary:
            --------
            Function called when the screen is fully left.
            This removes any instances of the screen
            from the application and
            clears all widgets from it before doing so.
        """
        Debug.Start("ConnectButton -> on_leave")
        Debug.Log("Attempting to remove self from AppManager's widgets")
        self.clear_widgets()
        AppManager.manager.remove_widget(self)
        Debug.End()
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            Function called before the screen is fully left. This gives
            us time to animate the screen leaving before destroying the
            objects and instances it created.
        """
        pass
# ------------------------------------------------------------------------
    def CancelConnection(self, *args):
        """
            Function to go back to `ProfileMenu.py`
        """
        # AppManager.manager.transition.direction = "down"
        # AppManager.manager.current = "ProfileMenu"
        WiFiLogin_Screens._BadExit()
# ------------------------------------------------------------------------
    def TryToConnect(self, *args):
        """
            TryToConnect:
            =============
            Summary:
            --------
            Function that tries to connect
            to a given WiFi network based
            on a specific given SSID and a
            typed in password.

            `Attention`:
            ----------
            Make sure that the pop up screen handler is already
            set by the previous transitional screen caller.
        """
        Debug.Start("TryToConnect")

        password = self.Password.text
        ssid     = self.SSIDTextField.text

        # Save the password into the current profile for next loading.
        ProfileHandler.SetNewSSIDPassword(ssid, password)

        if(Information.platform == "Windows"):
            result = ConnectToAWiFiNetwork(ssid, password)
            if(result):
                PopUpsHandler.Clear()
                PopUpsHandler.Add(
                                    Type = PopUpTypeEnum.Custom,
                                    Icon = "wifi-check",
                                    Message=_("You successfully connected to: ") + ssid,
                                    ButtonBText="None"
                                )
                PopUps_Screens.Call()
            else:
                PopUpsHandler.Clear()
                PopUpsHandler.Add(
                                    Type = PopUpTypeEnum.Custom,
                                    Icon = "wifi-cancel",
                                    Message=_("An error occurred while attempting to connect to: ") + ssid + _(" with password: ") + password,
                                    ButtonBHandler=WiFiLogin_Screens.Call,
                                    ButtonAText=_("Cancel"),
                                    ButtonBText=_("Retry")
                                )
                WiFiLogin_Screens._goodExitDirection = "down"
                WiFiLogin_Screens._badExitDirection = "down"
                WiFiLogin_Screens._callerDirection = "down"
                PopUps_Screens.Call()
        else:
            WiFiConnecting_Screens.SetCaller(WiFiLogin_Screens, "WiFiLogin", ssid, password)
            WiFiConnecting_Screens.SetExiter(DriverMenu_Screens, "DriverMenu")
            WiFiConnecting_Screens.Call()

        Debug.End()

LoadingLog.End("WiFiLogin.py")