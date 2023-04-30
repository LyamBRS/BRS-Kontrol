#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution, FileIntegrity
from Programs.Local.FileHandler.Profiles import ProfileThemeEnum
from Programs.Local.Updating.LaunchHandling import CreateLaunchNewAppPopUp, CreateTransferDataPopUp
from Programs.Pages.ProfileMenu import ProfileMenu_Screens
LoadingLog.Start("DownloadProgress.py")
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
from Programs.Local.GUI.Cards import DeviceDriverInstallerCard
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, CardTransition, SlideTransition
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
from ..Local.GUI.Navigation import AppNavigationBar
from ..Local.GUI.Cards import DeviceDriverCard
from ..Pages.PopUps import PopUpsHandler, PopUps_Screens, PopUpTypeEnum
#endregion
#====================================================================#
# thread class
#====================================================================#
class DownloadProgressHandler():
    """
        DownloadProgressHandler:
        ========================
        Summary:
        --------
        This class's purpose is to hold static instances of functions
        and members which will be used throughout threads and
        asynchronous functions executed throughout download processes.
        This allows your KivyMD application to keep track of the
        download progress and execute fails or good function depending
        on the results of the download.
    """
    downloadResult = None
    """
        Variable which holds the result of the download attempt.
        if set to `Execution.Passed`, the download passed.
        if set to `Execution.Failed`, the download didnt work.
        Defaults to `None`
    """

    def GoodDownload() -> Execution:
        """
            DownloadWorked:
            ===============
            Function to execute if the download succeeds
            replace it with your own function before calling the
            downloadprogress_screens class.
        """
        PopUpsHandler.Clear()
        PopUpsHandler.Add(Icon="check-decagram",
                      Message=_("The download was successful and has installed successfully."),
                      ButtonAText="Ok",
                      Type=PopUpTypeEnum.Remark)
        PopUps_Screens.SetCaller(DownloadProgress, "DownloadProgress")
        PopUps_Screens.SetExiter(ProfileMenu_Screens, "ProfileMenu")

        CreateTransferDataPopUp()
        CreateLaunchNewAppPopUp()

        PopUps_Screens.Call()
        pass

    def FailedDownload() -> Execution:
        """
            DownloadFailed:
            ===============
            Function to execute if the download succeeds
            replace it with your own function before calling the
            downloadprogress_screens class.
        """
        PopUpsHandler.Clear()
        PopUpsHandler.Add(Icon="check-decagram",
                        Message=_("The download failed and couldn't complete."),
                        ButtonAText="Damn",
                        Type=PopUpTypeEnum.Remark)
        PopUps_Screens.SetCaller(DownloadProgress, "DownloadProgress")
        PopUps_Screens.SetExiter(ProfileMenu_Screens, "ProfileMenu")
        PopUps_Screens.Call()
        pass
#====================================================================#
# Screen class
#====================================================================#
LoadingLog.Class("DownloadProgress_Screens")
class DownloadProgress_Screens:
    """
        DownloadProgress_Screens:
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

    _downloadName:str = None
    _downloadFunction = None
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
        DownloadProgress_Screens._exitClass = screenClass
        DownloadProgress_Screens._exitName  = screenName

        DownloadProgress_Screens._exitTransition = transition
        DownloadProgress_Screens._exitDuration = duration
        DownloadProgress_Screens._exitDirection = direction
        return False

    def SetCaller(screenClass, screenName:str, downloadName:str, downloadFunction, transition=SlideTransition,  duration:float=0, direction:str="down") -> bool:
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
        DownloadProgress_Screens._callerClass = screenClass
        DownloadProgress_Screens._callerName  = screenName

        DownloadProgress_Screens._downloadName = downloadName
        DownloadProgress_Screens._downloadFunction = downloadFunction

        DownloadProgress_Screens._callerTransition = transition
        DownloadProgress_Screens._callerDuration = duration
        DownloadProgress_Screens._callerDirection = direction
        return False

    def _Exit(*args) -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("DownloadProgress_Screens -> _Exit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(DownloadProgress_Screens._exitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(DownloadProgress_Screens._exitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                DownloadProgress_Screens._exitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(DownloadProgress_Screens._exitClass(name=DownloadProgress_Screens._exitName))
        except:
            Debug.Error("AppLoading -> Exception occured.")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = DownloadProgress_Screens._exitTransition()
        AppManager.manager.transition.duration = DownloadProgress_Screens._exitDuration
        AppManager.manager.transition.direction = DownloadProgress_Screens._exitDirection

        # try:
        AppManager.manager.current = DownloadProgress_Screens._exitName
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
        Debug.Start("DownloadProgress_Screens -> Call()")
        # Attempt to add the screen class as a widget of the AppManager
        # try:
        # Check if caller class was specified
        Debug.Log("Checking caller class")
        if(DownloadProgress_Screens._callerClass == None):
            Debug.Error("No caller class specified.")
            Debug.End()
            return True

        Debug.Log("Checking caller name")
        if(DownloadProgress_Screens._callerName == None):
            Debug.Error("No caller name specified.")
            Debug.End()
            return True

        Debug.Log("Attempting to add widget")
        AppManager.manager.add_widget(DownloadProgress(name="DownloadProgress"))
        # except:
        Debug.Error("Exception occured while handling Call()")
        Debug.End()
            # return True

        # Attempt to call the added screen
        AppManager.manager.transition = DownloadProgress_Screens._callerTransition()
        AppManager.manager.transition.duration = DownloadProgress_Screens._callerDuration
        AppManager.manager.transition.direction = DownloadProgress_Screens._callerDirection

        # try:
        AppManager.manager.current = "DownloadProgress"
        Debug.Log("Screen successfully changed")
        # except:
            # Debug.Error("Failed to add DownloadProgress as current screen.")
            # Debug.End()
            # return True
        Debug.End()
        return False
    #endregion
#====================================================================#
# Classes
#====================================================================#

LoadingLog.Class("DownloadProgress")
class DownloadProgress(Screen):
    """
        DownloadProgress:
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
        Debug.Start("DownloadProgress -> on_pre_enter")

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
        self.Layout = MDBoxLayout()
        self.Layout.orientation = "vertical"
        #endregion

        #region ---------------------------- Spinner
        self.spinner = MDSpinner()
        self.spinner.size_hint = (0.25, 0.25)
        self.spinner.pos_hint = {"center_x":0.5, "center_y":0.5}
        #endregion

        #region ---------------------------- Progress bar
        self.progressBar = MDProgressBar()
        self.progressBar.value = 0
        self.progressBar.max = 100
        self.progressBar.type = "determinate"
        self.progressBar.size_hint = (1, None)
        self.progressBar.pos_hint = {"center_x":0.5, "center_y":0.5}
        #endregion

        Clock.schedule_once(self.CheckDownload, 1)

        self.add_widget(background)
        self.Layout.add_widget(self.spinner)
        self.Layout.add_widget(self.progressBar)
        self.add_widget(self.Layout)
        Debug.End()
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            Function called when the screen is fully entered in view.
            In this case, once the view is fully loaded, the cards
            will slowly elevate to the wanted value.
        """
        Debug.Start("DownloadProgress -> on_enter")
        Debug.Log("Starting specified download...")
        result = DownloadProgress_Screens._downloadFunction(self.progressBar, DownloadProgressHandler)
        if(result != Execution.Passed):
            Debug.Error("Failed to launch download")
        else:
            Debug.Log("Download started")
        Debug.End()
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            Function called before the screen is fully left. This gives
            us time to animate the screen leaving before destroying the
            objects and instances it created.
        """
        Debug.Start("DownloadProgress -> on_pre_leave")
        Debug.End()
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully out of view.
        """
        Debug.Start("DownloadProgress -> on_leave")
        Debug.Log("Attempting to remove self from AppManager's widgets")
        self.clear_widgets()
        AppManager.manager.remove_widget(self)
        Debug.End()
        self.clear_widgets()
# ------------------------------------------------------------------------
    def CheckDownload(self, *args):
        """
            CheckDownload
            =============
            Summary:
            --------
            Check if the download is finished at a constant interval.
            Will constantly reschedule itself until download is finished.
        """
        Debug.Start("CheckDownload")
        if(DownloadProgressHandler.downloadResult == Execution.Passed):
            DownloadProgressHandler.GoodDownload()
            DownloadProgressHandler.downloadResult = None
            return

        if(DownloadProgressHandler.downloadResult == Execution.Failed):
            DownloadProgressHandler.FailedDownload()
            DownloadProgressHandler.downloadResult = None
            return

        Clock.schedule_once(self.CheckDownload, 1)
        Debug.End()
LoadingLog.End("DriverMenu.py")