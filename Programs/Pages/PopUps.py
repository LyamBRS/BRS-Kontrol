#====================================================================#
# File Information
#====================================================================#
"""
    PopUps.py
    =============
    This is a strike page which allows daisy chains of pop ups to display
    one after the other.

    Before calling this function, you need to set the pop up list.
    Remember that this is not to display a pop up *above* a screen, but
    to create daisy chains of pop ups after an event.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("PopUps.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
import os
from enum import Enum
from functools import partial
#endregion
#region --------------------------------------------------------- BRS
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
from Libraries.BRS_Python_Libraries.BRS.Network.Web.web import IsWebsiteOnline
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
#endregion
#region -------------------------------------------------------- Kivy
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, CardTransition,SlideTransition
#endregion
#region ------------------------------------------------------ KivyMD
from kivymd.uix.floatlayout import MDFloatLayout
#endregion
LoadingLog.Log("Import success")
#====================================================================#
# Enums
#====================================================================#
LoadingLog.Log("PopUpTypeEnum")
class PopUpTypeEnum(Enum):
    """
        PopUpTypeEnum:
        ------------
        This enumeration holds all the names of the different pop
        up styles that your pop up can be.
    """
    Remark:int = 0
    FatalError:int = 1
    Question:int = 2
    Warning:int = 3
LoadingLog.Log("Keys")
class Keys(Enum):
    """
        Keys:
        ------------
        This enumeration holds all the names of the different pop
        up styles that your pop up can be.
    """
    Icon:int = 0
    Message:int = 1
    Type:int = 2
    CanContinue:int = 3
#====================================================================#
# Pop up structure
#====================================================================#
PopUpStructure = {
    Keys.Icon : "exclamation",
    Keys.Message : "Message",
    Keys.Type : PopUpTypeEnum.Remark,
    Keys.CanContinue : True
}
"""
    the template structure used to build pop ups
"""
#====================================================================#
# Functions
#====================================================================#
LoadingLog.Log("PopUpsHandler")
class PopUpsHandler:
    """Class that handles the creation of the popups to display"""
    #region   --------------------------- MEMBERS
    PopUps:list = {}
    #endregion
    #region   --------------------------- METHODS
    def Clear():
        """
            Clear:
            ------
            Clears all pop ups in the pop up list.
        """
        Debug.Start("PopUps -> Clear")
        PopUpsHandler.PopUps.clear()
        Debug.End()
    # -------------------------------------------
    def Add(Type:Keys, Icon:str, Message:str, CanContinue:bool=True):
        """
            Add:
            ----
            Adds a pop up to the list of daisy chain pop ups that will
            be displayed to the user.
        """
        Debug.Start("Add")
        PopUpsHandler.PopUps.append({
            Keys.Icon : Icon,
            Keys.Message : Message,
            Keys.Type : Type,
            Keys.CanContinue : CanContinue
        })
        Debug.End()
    #endregion
#====================================================================#
# Screen class
#====================================================================#
LoadingLog.Log("PopUps_Screens")
class PopUps_Screens:
    """
        PopUps_Screens:
        ================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`PopUps`.

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

    def SetExiter(screenClass, screenName:str, transition=SlideTransition, duration:float=0.5, direction:str="up") -> bool:
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
        PopUps_Screens._exitClass = screenClass
        PopUps_Screens._exitName  = screenName

        PopUps_Screens._exitTransition = transition
        PopUps_Screens._exitDuration = duration
        PopUps_Screens._exitDirection = direction
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
        PopUps_Screens._callerClass = screenClass
        PopUps_Screens._callerName  = screenName

        PopUps_Screens._callerTransition = transition
        PopUps_Screens._callerDuration = duration
        PopUps_Screens._callerDirection = direction
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
            if(Startup_Screens._exitClass == None):
                return True
            if(Startup_Screens._exitName == None):
                return True

            AppManager.manager.add_widget(Startup_Screens._exitClass(name=Startup_Screens._exitName))
        except:
            Debug.Error("Startup_Screens: _Exit() -> Failed in add_widget")
            return True
        
        # Attempt to call the added screen
        AppManager.manager.transition = PopUps_Screens._exitTransition()
        AppManager.manager.transition.duration = PopUps_Screens._exitDuration
        AppManager.manager.transition.direction = PopUps_Screens._exitDirection

        # try:
        AppManager.manager.current = PopUps_Screens._exitName
        # except:
            # Debug.Error("Startup_Screens: _Exit() -> AppManager.manager.current FAILED")
            # return True
        return False
    
    def Call() -> bool:
        """
            Attempt to go to the main screen that is being handled by this class.

            Returns:
                bool: `True`:  Something went wrong and the screen can't be loaded. `False`: Success
        """
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            if(PopUps_Screens._callerClass == None):
                return True
            if(PopUps_Screens._callerName == None):
                return True

            AppManager.manager.add_widget(Startup(name="PopUps"))
        except:
            return True
        
        # Attempt to call the added screen
        AppManager.manager.transition = PopUps_Screens._callerTransition()
        AppManager.manager.transition.duration = PopUps_Screens._callerDuration
        AppManager.manager.transition.direction = PopUps_Screens._callerDirection

        try:
            AppManager.manager.current = PopUps_Screens._callerName
        except:
            return True
        return True
#====================================================================#
# Main Function
#====================================================================#
LoadingLog.Log("PopUps")
class PopUps(Screen):
    """
        PopUps:
        ================
        Summary:
        --------
        class used to display daisy chained pop ups after a major loading
        event.

        Description:
        ------------
        This class holds the standard `ScreenManager` classes used by screen
        classes to display widgets and unload them or perform various screen
        specific actions.

        This `PopUps` screen class is used to display daisy chained pop up
        screens. If you do not set the pop up windows prior to calling the
        screen, it will skip to the good exiter immediately. There is multiple
        types of screens available for each pop up.

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
        Debug.Start("ProfileMenu")
        Debug.End()
    #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
            on_pre_enter:
            =============
            Function which "builds" the :ref:`PopUps` screen.
            This function is called before the screen is actually shown and
            loads all the widgets that will be displayed before :ref:`on_enter` is called.

            Screen specific actions:
            ------------------------
            The :ref:`Startup` is solely a short animation, nothing more, nothing less.
        """
        Debug.Start("PopUps: on_pre_enter")
        self.padding = 25
        self.spacing = 25

        #region ---- Main Layout
        self.Layout = MDFloatLayout()
        #endregion

        #region ---- B R S & Kontrol images
        #endregion

        #region ---- Initial status of Images
        # Set the images as they are prior to the startup
        self.B.pos_hint={'center_x': 0.17, 'center_y':self.letterYStart}
        self.R.pos_hint={'center_x': 0.5,  'center_y':self.letterYStart}
        self.S.pos_hint={'center_x': 0.83, 'center_y':self.letterYStart}
        self.KontrolText.pos_hint={'center_x': 0.5, 'center_y':0}
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
        """
        Debug.Start("PopUps: on_enter")
        # First animation of letters
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
        Debug.Start("PopUps: on_pre_leave")
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
        Debug.Start("PopUps: on_leave")
        self.clear_widgets()
        Debug.End()
# ------------------------------------------------------------------------

#====================================================================#
LoadingLog.End("PopUps.py")