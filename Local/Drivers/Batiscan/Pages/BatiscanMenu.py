#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution, FileIntegrity
LoadingLog.Start("BatiscanMenu.py")
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
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
from kivy.uix.screenmanager import Screen, SlideTransition
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import("KivyMD")
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.floatlayout import MDFloatLayout
#endregion
#region ------------------------------------------------------ Kontrol
LoadingLog.Import("Local")
# from Programs.Local.GUI.Cards import ButtonCard, DeviceDriverCard
# from Programs.Pages.PopUps import PopUpsHandler, PopUps_Screens, PopUpTypeEnum
#endregion
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Screen class
#====================================================================#
LoadingLog.Class("BatiscanMenu_Screens")
class BatiscanMenu_Screens:
    """
        BatiscanMenu_Screens:
        ================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`BatiscanMenu`.

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
        BatiscanMenu_Screens._exitClass = screenClass
        BatiscanMenu_Screens._exitName  = screenName

        BatiscanMenu_Screens._exitTransition = transition
        BatiscanMenu_Screens._exitDuration = duration
        BatiscanMenu_Screens._exitDirection = direction
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
        BatiscanMenu_Screens._callerClass = screenClass
        BatiscanMenu_Screens._callerName  = screenName

        BatiscanMenu_Screens._callerTransition = transition
        BatiscanMenu_Screens._callerDuration = duration
        BatiscanMenu_Screens._callerDirection = direction
        return False

    def _Exit(*args) -> Execution:
        """
            Attempt to go to the specified screen that was set using :ref:`SetExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("BatiscanMenu_Screens -> _Exit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(BatiscanMenu_Screens._exitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(BatiscanMenu_Screens._exitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                BatiscanMenu_Screens._exitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(BatiscanMenu_Screens._exitClass(name=BatiscanMenu_Screens._exitName))
        except:
            Debug.Error("AppLoading -> Exception occured.")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = BatiscanMenu_Screens._exitTransition()
        AppManager.manager.transition.duration = BatiscanMenu_Screens._exitDuration
        AppManager.manager.transition.direction = BatiscanMenu_Screens._exitDirection

        # try:
        AppManager.manager.current = BatiscanMenu_Screens._exitName
        # except:
            # return True
        Debug.End()
        return False

    def Call(*args) -> Execution:
        """
            Attempt to go to the main screen that is being handled by this class.

            Returns:
                Execution
        """
        Debug.Start("BatiscanMenu_Screens -> Call()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if caller class was specified
            Debug.Log("Checking caller class")
            if(BatiscanMenu_Screens._callerClass == None):
                Debug.Error("No caller class specified.")
                Debug.End()
                return True

            Debug.Log("Checking caller name")
            if(BatiscanMenu_Screens._callerName == None):
                Debug.Error("No caller name specified.")
                Debug.End()
                return True

            Debug.Log("Attempting to add widget")
            AppManager.manager.add_widget(BatiscanMenu(name="BatiscanMenu"))
        except:
            Debug.Error("Exception occured while handling Call()")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = BatiscanMenu_Screens._callerTransition()
        AppManager.manager.transition.duration = BatiscanMenu_Screens._callerDuration
        AppManager.manager.transition.direction = BatiscanMenu_Screens._callerDirection

        # try:
        AppManager.manager.current = "BatiscanMenu"
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
LoadingLog.Class("BatiscanMenu")
class BatiscanMenu(Screen):
    """
        BatiscanMenu:
        -----------
        This class handles the screen of the Batiscan which shows
        the user the potential things they can debug about their
        Kontrol application.
    """
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("BatiscanMenu -> __init__")
        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
        """
        Debug.Start("BatiscanMenu -> on_pre_enter")

        self.padding = 0
        self.spacing = 0

        #region ---------------------------- Background
        from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
        path = os.getcwd()
        background = GetBackgroundImage(AppendPath(path, "/Local/Drivers/Batiscan/Libraries/Backgrounds/Menu/Dark.png"),
                                        AppendPath(path, "/Local/Drivers/Batiscan/Libraries/Backgrounds/Menu/Light.png"))
        #endregion

        #region ---------------------------- Layouts
        self.Layout = MDFloatLayout()

        self.bottomLayout = MDBoxLayout(orientation = "horizontal", size_hint = (1,0.25))

        self.LightButton        = MDIconButton(icon="car-light-high", halign = "center", valign = "center")
        self.FillBallastButton  = MDIconButton(icon="basket-fill", halign = "center", valign = "center")
        self.EmptyBallastButton = MDIconButton(icon="basket-unfill", halign = "center", valign = "center")
        self.SurfaceButton      = MDIconButton(icon="waves-arrow-up", halign = "center", valign = "center")
        self.CameraButton       = MDIconButton(icon="video-off", halign = "center", valign = "center")

        self.bottomLayout.add_widget(self.FillBallastButton)
        self.bottomLayout.add_widget(self.LightButton)
        self.bottomLayout.add_widget(self.SurfaceButton)
        self.bottomLayout.add_widget(self.CameraButton)
        self.bottomLayout.add_widget(self.EmptyBallastButton)
        #endregion


        #region ---------------------------- ToolBar
        from Local.Drivers.Batiscan.Programs.GUI.Navigation import DebugNavigationBar
        self.ToolBar = DebugNavigationBar(pageTitle=_("Batiscan"))
        #endregion

        self.Layout.add_widget(self.bottomLayout)
        self.Layout.add_widget(self.ToolBar.ToolBar)
        self.Layout.add_widget(self.ToolBar.NavDrawer)
        self.add_widget(background)
        self.add_widget(self.Layout)
        Debug.End()
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            Function called when the screen is fully entered in view.
            In this case, once the view is fully loaded, the cards
            will slowly elevate to the wanted value.
        """
        Debug.Start("BatiscanMenu -> on_enter")
        Debug.End()
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            Function called before the screen is fully left. This gives
            us time to animate the screen leaving before destroying the
            objects and instances it created.
        """
        Debug.Start("BatiscanMenu -> on_pre_leave")
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

LoadingLog.End("BatiscanMenu.py")