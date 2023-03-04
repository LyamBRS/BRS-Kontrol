#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("AppLoading.py")
#====================================================================#
# Imports
#====================================================================#
import os
from kivy.core.window import Window
from random import randint, random
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import FilesFinder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.graphics import Canvas, Color, Rectangle, PushMatrix, PopMatrix, Rotate
# -------------------------------------------------------------------
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, CardTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDIconButton
# -------------------------------------------------------------------
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Shadow
from Libraries.BRS_Python_Libraries.BRS.GUI.Inputs.buttons import Get_RaisedButton,TextButton
from Libraries.BRS_Python_Libraries.BRS.GUI.Status.ValueDisplay import OutlineDial, LineGraph
from Libraries.BRS_Python_Libraries.BRS.GUI.Status.Indicators import SVGDisplay
from Libraries.BRS_Python_Libraries.BRS.GUI.Containers.cards import WidgetCard,ProfileCard,CreateCard
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Programs.Local.FileHandler.Profiles import LoadedProfile,CheckIntegrity
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
# -------------------------------------------------------------------
from .ProfileLogin import ProfileLogin
from .ProfileCreation import ProfileCreation_Step1
from ..Local.FileHandler import Profiles
#====================================================================#
# Screen Functions
#====================================================================#
class AppLoading_Screens:
    """
        AppLoading_Screens:
        ================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`AppLoading`.

        Description:
        ------------
        This class holds the different types of callers of the AppLoading
        screen as well as the different exit screens that this transitional
        screen can go to. You must specify the names of the wanted exit screens
        prior to calling the transition function.

        An exit screen is basically which screens should be loaded if something
        happens in the transition screen.
    """

    def SetExiter(screenClass, screenName:str, transition=WipeTransition, duration:float=0.5, direction:str="up") -> bool:
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
        AppLoading_Screens._exitClass = screenClass
        AppLoading_Screens._exitName  = screenName

        AppLoading_Screens._exitTransition = transition
        AppLoading_Screens._exitDuration = duration
        AppLoading_Screens._exitDirection = direction
        return False

    def SetCaller(screenClass, screenName:str, transition=WipeTransition, duration:float=0.5, direction:str="up") -> bool:
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
        AppLoading_Screens._callerClass = screenClass
        AppLoading_Screens._callerName  = screenName

        AppLoading_Screens._callerTransition = transition
        AppLoading_Screens._callerDuration = duration
        AppLoading_Screens._callerDirection = direction
        return False

    def _Exit() -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            if(AppLoading_Screens._exitClass == None):
                return True
            if(AppLoading_Screens._exitName == None):
                return True

            AppManager.manager.add_widget(AppLoading_Screens._exitClass(name=AppLoading_Screens._exitName))
        except:
            return True
        
        # Attempt to call the added screen
        AppManager.manager.transition = AppLoading_Screens._exitTransition()
        AppManager.manager.transition.duration = AppLoading_Screens._exitDuration
        AppManager.manager.transition.direction = AppLoading_Screens._exitDirection

        try:
            AppManager.manager.current = AppLoading_Screens._exitName
        except:
            return True
        return True
    
    def Call() -> bool:
        """
            Attempt to go to the main screen that is being handled by this class.

            Returns:
                bool: `True`:  Something went wrong and the screen can't be loaded. `False`: Success
        """
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            if(AppLoading_Screens._callerClass == None):
                return True
            if(AppLoading_Screens._callerName == None):
                return True

            AppManager.manager.add_widget(Startup(name="Startup"))
        except:
            return True
        
        # Attempt to call the added screen
        AppManager.manager.transition = AppLoading_Screens._callerTransition()
        AppManager.manager.transition.duration = AppLoading_Screens._callerDuration
        AppManager.manager.transition.direction = AppLoading_Screens._callerDirection

        try:
            AppManager.manager.current = AppLoading_Screens._callerName
        except:
            return True
        return True
#====================================================================#
# Classes
#====================================================================#
class AppLoading(Screen):
    """
        AppLoading:
        ================
        Summary:
        --------
        This class is a screen class used to display a specific screen.
        Please use :ref:`AppLoading_Screens` to call this class.

        Description:
        ------------
        This class holds the loading application's screen.
        It also loads the application while displaying each steps of the loading.

        Methods:
        ------------
        - :ref:`on_pre_enter`: Builds the widgets to display on screen
        - :ref:`on_enter`: Called once the screen is fully displayed
        - :ref:`on_pre_leave`: Called before the screen is left
        - :ref:`on_leave`: Last function called by this screen before dying. Unloads all widgets
    """
    #region   --------------------------- MEMBERS

    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("AppLoading")
        Debug.End()
    #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
            on_pre_enter:
            =============
            Function which "builds" the :ref:`Startup` screen.
            This function is called before the screen is actually shown and
            loads all the widgets that will be displayed before :ref:`on_enter` is called.

            Screen specific actions:
            ------------------------
            The :ref:`Startup` screen will check, verify and load the cached JSON of the application
            so that the application's last values will be loaded as they were before it closed.
            This means that anything like themes and languages will stay in memory and won't reset
            to default values each time the application is started.
            If no cached json is found, it will be created automatically and default values will be stored
            in it.
        """
        Debug.Start("AppLoading.py: on_pre_enter")
        self.padding = 25
        self.spacing = 25

        #region ---- Main Layout
        self.Layout = MDFloatLayout()
        #endregion

        #region ---- B R S & Kontrol images
        #endregion

        #region ---- Initial status of Images
        #endregion

        #region ---- add_widgets
        self.add_widget(self.Layout)
        #endregion

        Debug.End()
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            on_enter:
            =============
            Function called once the screen is fully loaded into view.

            Screen specific actions:
            ------------------------
            Starts the BRS logo's startup screen.
        """
        Debug.Start("AppLoading.py: on_enter")
        Debug.End()
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            on_pre_leave:
            =============
            Function called once the screen is about to leave.

            Screen specific actions:
            ------------------------
            NOT USED
        """
        Debug.Start("AppLoading.py: on_pre_leave")
        Debug.End()
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            on_leave:
            =============
            Function called once the screen has fully left. This function is used
            to remove all the widgets created when :ref:`on_pre_start` was called.
            Doing so hopefully clears out some memory used by the screen to help load
            the next one. Anything that must be deleted due to being no longer used
            needs to be done here.

            Screen specific actions:
            ------------------------
            calls `self.clear_widgets()`
        """
        Debug.Start("AppLoading.py: on_leave")
        self.clear_widgets()
        Debug.End()
# ------------------------------------------------------------------------
LoadingLog.End("AppLoading.py")