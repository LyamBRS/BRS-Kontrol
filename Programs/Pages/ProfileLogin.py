#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("ProfileLogin.py")
#====================================================================#
# Imports
#====================================================================#
import os
from random import randint, random
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import FilesFinder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, CardTransition,SlideTransition
# -------------------------------------------------------------------
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton,MDRectangleFlatButton,MDFillRoundFlatButton,MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, CardTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
# -------------------------------------------------------------------
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Shadow
from Libraries.BRS_Python_Libraries.BRS.GUI.Inputs.buttons import Get_RaisedButton,TextButton
from Libraries.BRS_Python_Libraries.BRS.GUI.Status.ValueDisplay import OutlineDial, LineGraph
from Libraries.BRS_Python_Libraries.BRS.GUI.Status.Indicators import SVGDisplay
from Libraries.BRS_Python_Libraries.BRS.GUI.Containers.cards import WidgetCard,ProfileCard
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Rounding,Shadow
from Libraries.BRS_Python_Libraries.BRS.Utilities.states import StatesColors,States
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Programs.Local.FileHandler.Profiles import LoadedProfile, ProfileGenericEnum, structureEnum
# from Programs.Pages.ProfileMenu import ProfileMenu
# -------------------------------------------------------------------
from ..Local.FileHandler import Profiles
from ..Pages.PopUps import PopUpTypeEnum, PopUpsHandler,PopUps_Screens
#====================================================================#
# Functions
#====================================================================#
#====================================================================#
# Screen class
#====================================================================#
LoadingLog.Log("ProfileLogin_Screens")
class ProfileLogins_Screens:
    """
        ProfileLogins_Screens:
        ================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`ProfileLogin`.

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
        ProfileLogins_Screens._goodExitClass = screenClass
        ProfileLogins_Screens._goodExitName  = screenName

        ProfileLogins_Screens._goodExitTransition = transition
        ProfileLogins_Screens._goodExitDuration = duration
        ProfileLogins_Screens._goodExitDirection = direction
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
        ProfileLogins_Screens._badExitClass = screenClass
        ProfileLogins_Screens._badExitName  = screenName

        ProfileLogins_Screens._badExitTransition = transition
        ProfileLogins_Screens._badExitDuration = duration
        ProfileLogins_Screens._badExitDirection = direction
        return False

    def SetCaller(screenClass, screenName:str, transition=SlideTransition, duration:float=0.5, direction:str="up") -> bool:
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
        ProfileLogins_Screens._callerClass = screenClass
        ProfileLogins_Screens._callerName  = screenName

        ProfileLogins_Screens._callerTransition = transition
        ProfileLogins_Screens._callerDuration = duration
        ProfileLogins_Screens._callerDirection = direction
        return False

    def _BadExit() -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetBadExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("ProfileLogin -> _BadExit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(ProfileLogins_Screens._badExitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(ProfileLogins_Screens._badExitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                ProfileLogins_Screens._badExitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(ProfileLogins_Screens._badExitClass(name=ProfileLogins_Screens._badExitName))
        except:
            Debug.Error("PopUps: _Exit() -> Failed in add_widget")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = ProfileLogins_Screens._badExitTransition()
        AppManager.manager.transition.duration = ProfileLogins_Screens._badExitDuration
        AppManager.manager.transition.direction = ProfileLogins_Screens._badExitDirection

        # try:
        AppManager.manager.current = ProfileLogins_Screens._badExitName
        # except:
            # Debug.Error("Startup_Screens: _Exit() -> AppManager.manager.current FAILED")
            # Debug.End()
            # return True
        Debug.End()
        return False

    def _GoodExit() -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetGoodExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("ProfileLogin -> _GoodExit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(ProfileLogins_Screens._goodExitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(ProfileLogins_Screens._goodExitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                ProfileLogins_Screens._goodExitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(ProfileLogins_Screens._goodExitClass(name=ProfileLogins_Screens._goodExitName))
        except:
            Debug.Error("PopUps: _Exit() -> Failed in add_widget")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = ProfileLogins_Screens._goodExitTransition()
        AppManager.manager.transition.duration = ProfileLogins_Screens._goodExitDuration
        AppManager.manager.transition.direction = ProfileLogins_Screens._goodExitDirection

        # try:
        AppManager.manager.current = ProfileLogins_Screens._goodExitName
        # except:
            # Debug.Error("Startup_Screens: _Exit() -> AppManager.manager.current FAILED")
            # Debug.End()
            # return True
        Debug.End()
        return False

    def Call() -> bool:
        """
            Attempt to go to the main screen that is being handled by this class.

            Returns:
                bool: `True`:  Something went wrong and the screen can't be loaded. `False`: Success
        """
        Debug.Start("ProfileLogin -> Call")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking caller class")
            if(ProfileLogins_Screens._callerClass == None):
                Debug.Error("No caller class specified.")
                Debug.End()
                return True

            Debug.Log("Checking caller name")
            if(ProfileLogins_Screens._callerName == None):
                Debug.Error("No caller name specified.")
                Debug.End()
                return True

            Debug.Log("Adding widget")
            AppManager.manager.add_widget(ProfileLogin(name="ProfileLogin"))
        except:
            Debug.Error("Exception occured while handling Call()")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = ProfileLogins_Screens._callerTransition()
        AppManager.manager.transition.duration = ProfileLogins_Screens._callerDuration
        AppManager.manager.transition.direction = ProfileLogins_Screens._callerDirection

        # try:
        AppManager.manager.current = "ProfileLogin"
        # except:
            # Debug.Error("Failed to add ProfileLogin as current screen.")
            # Debug.End()
            # return True

        Debug.End()
        return False
    #endregion

#====================================================================#
# Classes
#====================================================================#
class ProfileLogin(Screen):
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
        Debug.Start("ProfileLogin")
        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
            Builds the login screen entirely.
            The login screen consists of a "Login" message as well as
            a card containing a username and password textfields.
        """
        try:
            self.padding = 25
            self.spacing = 25

            # Login card
            self.MainLayout = MDBoxLayout(spacing=10, padding=("300sp","20sp","300sp","20sp"), orientation="vertical")
            self.Card = MDCard(
                                elevation = Shadow.Elevation.default,
                                shadow_softness = Shadow.Smoothness.default,
                                radius=Rounding.default,
                                padding = 25,
                                orientation = "vertical"
                                )

            self.UsernameTitle = MDLabel(text=_("Username") + ":")
            self.PasswordTitle = MDLabel(text=_("Password") + ":")
            self.Username = MDTextField(text=LoadedProfile.rawJson.jsonData[structureEnum.Generic][ProfileGenericEnum.Username])
            self.Password = MDTextField()
            self.PasswordTitle.font_style = "H5"
            self.UsernameTitle.font_style = "H5"

            # Page title
            self.LoginTitle = MDLabel(text=_("Login"), font_style = "H1", halign = "center", size_hint_y = 0.25)

            # Button Layout
            self.ButtonLayout = MDBoxLayout(spacing=20)
            self.CancelLayout = MDFloatLayout()
            self.LoginLayout = MDFloatLayout()

            self.Login = MDIconButton(text="check", icon="check")
            self.Cancel = MDIconButton(text="close-circle", icon="close-circle")
            self.Login.icon_size = "100sp"
            self.Cancel.icon_size = "100sp"
            self.Login.pos_hint={"center_x": 0.5, "center_y": 0.5}
            self.Cancel.pos_hint={"center_x": 0.5, "center_y": 0.5}

            # Set back function
            self.Cancel.on_release = self.GoBack
            self.Login.on_release = self.LoginAttempt

            # Add widgets
            self.CancelLayout.add_widget(self.Cancel)
            self.LoginLayout.add_widget(self.Login)
            self.ButtonLayout.add_widget(self.LoginLayout)
            self.ButtonLayout.add_widget(self.CancelLayout)
            self.Card.add_widget(self.UsernameTitle)
            self.Card.add_widget(self.Username)
            self.Card.add_widget(self.PasswordTitle)
            self.Card.add_widget(self.Password)
            self.Card.add_widget(self.ButtonLayout)

            self.MainLayout.add_widget(self.LoginTitle)
            self.MainLayout.add_widget(self.Card)
            self.add_widget(self.MainLayout)
        except:
            PopUpsHandler.Clear()
            PopUpsHandler.Add(PopUpTypeEnum.FatalError, Message=_("An error occured while trying to load this profile. No repairs can be done to fix this corrupted profile as no information can be retreived."))
            PopUps_Screens.SetExiter(ProfileLogins_Screens._badExitClass, ProfileLogins_Screens._badExitName, direction="down")
            PopUps_Screens.Call()
        pass
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            Animate all the widgets into view once the screen is fully present.
        """
        print("Login: on_enter")


        # Start Animation
        # self.animation.stop_all(self)
        # self.animation = Animation(progress = 1, duration = 0.5)
        # self.animation.bind(on_progress = self._Animating)
        # self.animation.start(self)
        pass
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully left.
        """
        Debug.Start("Login -> on_leave")
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
        print("Login: on_pre_leave")
# ------------------------------------------------------------------------
    def _Animating(self, *args):
        """
            Call back function called each time an animation tick happens.
            We use it to add/remove the shadow of cards when entering or
            leaving the application.
        """
        pass
# ------------------------------------------------------------------------
    def GoBack(self, *args):
        """
            Function to go back to `ProfileMenu.py`
        """
        # AppManager.manager.transition.direction = "down"
        # AppManager.manager.current = "ProfileMenu"
        ProfileLogins_Screens._BadExit()
# ------------------------------------------------------------------------
    def LoginAttempt(self, *args):
        """
            Function called when attempting to log in with the specified
            password and username
        """
        username = LoadedProfile.rawJson.jsonData["Generic"]["Username"]
        password = LoadedProfile.rawJson.jsonData["Generic"]["Password"]

        if(username != self.Username.text):
            self.Username.error = True

        if(password != self.Password.text):
            self.Password.error = True

        if(self.Username.error or self.Password.error):
            pass
        else:
            ProfileLogins_Screens._GoodExit()

LoadingLog.End("ProfileLogin.py")