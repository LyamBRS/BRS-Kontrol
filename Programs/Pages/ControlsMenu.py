#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("ControlMenu.py")
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
LoadingLog.Class("ControlMenu_Screens")
class ControlMenu_Screens:
    """
        ControlMenu_Screens:
        ================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`ControlMenu`.

        Description:
        ------------
        This class holds the different types of callers of the ControlMenu
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
        ControlMenu_Screens._exitClass = screenClass
        ControlMenu_Screens._exitName  = screenName

        ControlMenu_Screens._exitTransition = transition
        ControlMenu_Screens._exitDuration = duration
        ControlMenu_Screens._exitDirection = direction
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
        ControlMenu_Screens._callerClass = screenClass
        ControlMenu_Screens._callerName  = screenName

        ControlMenu_Screens._callerTransition = transition
        ControlMenu_Screens._callerDuration = duration
        ControlMenu_Screens._callerDirection = direction
        return False

    def _Exit() -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("ControlMenu_Screens -> _Exit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(ControlMenu_Screens._exitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(ControlMenu_Screens._exitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                ControlMenu_Screens._exitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(ControlMenu_Screens._exitClass(name=ControlMenu_Screens._exitName))
        except:
            Debug.Error("ControlMenu_Screens -> Exception occured.")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = ControlMenu_Screens._exitTransition()
        AppManager.manager.transition.duration = ControlMenu_Screens._exitDuration
        AppManager.manager.transition.direction = ControlMenu_Screens._exitDirection

        # try:
        AppManager.manager.current = ControlMenu_Screens._exitName
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
            AppManager.manager.add_widget(ControlMenu(name="ControlMenu"))
        except:
            Debug.Error("Exception occured while handling Call()")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = ControlMenu_Screens._callerTransition()
        AppManager.manager.transition.duration = ControlMenu_Screens._callerDuration
        AppManager.manager.transition.direction = ControlMenu_Screens._callerDirection

        # try:
        AppManager.manager.current = "ControlMenu"
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
LoadingLog.Class("ControlMenu")
class ControlMenu(Screen):
    """
        ControlMenu:
        -----------
        This class handles the screen of the account menu which shows
        to the user some actions that they can do with their user profiles
    """
    #region   --------------------------- MEMBERS
    ToolBar:AppNavigationBar = None
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("ControlMenu -> __init__")
        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
        """
        Debug.Start("ControlMenu -> on_pre_enter")

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
        self.cardBox = MDBoxLayout(size_hint=(1,1), pos_hint = {'top': 1, 'left': 0}, orientation='horizontal', spacing="100sp", padding = (50,50,50,50), size_hint_x=None)
        self.cardBox.bind(minimum_width = self.cardBox.setter('width'))

        # Create the scroll view and add the box layout to it
        self.scroll = MDScrollView(pos_hint = {'top': 1, 'left': 0}, scroll_type=['bars','content'], size_hint = (1,1))
        self.scroll.smooth_scroll_end = 10

        # Add widgets
        self.add_widget(background)
        self.scroll.add_widget(self.cardBox)
        #endregion
        #region ---------------------------- ToolBar
        self.ToolBar = AppNavigationBar(pageTitle=_("Controls & Keybinds"))
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
        Debug.Start("ControlMenu -> on_enter")
        Debug.End()
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            Function called before the screen is fully left. This gives
            us time to animate the screen leaving before destroying the
            objects and instances it created.
        """
        Debug.Start("ControlMenu -> on_pre_leave")
        Debug.End()
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully out of view.
        """
        Debug.Start("ControlMenu -> on_leave")
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

LoadingLog.End("ControlMenu.py")