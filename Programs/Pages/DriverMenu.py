#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution, FileIntegrity
LoadingLog.Start("DriverMenu.py")
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
from ..Pages.PopUps import PopUpsHandler, PopUps_Screens, PopUpTypeEnum
#endregion
#====================================================================#
# Functions
#====================================================================#
def HandleDriverIntegrity(driverName, GetErrorMessageFunction) -> Execution:
    """
        HandleDriverIntegrity:
        ======================
        Summary:
        --------
        This function is made to remove some copy pasted lines of code
        and to make the program clearer to read. This function handles
        the integrity of a device driver.

        Function:
        ---------
        First attempts to get CheckIntegrity from driverName.
        If that fails, a pop up is called.
        Otherwise, it attempts to execute the integrity function.
        Popups are built depending on the integrity results.

        if everything is well with the integrity of the device driver,
        then `Execution.Passed` is returned.
    """
    Debug.Start("HandleDriverIntegrity")
    from ..Local.FileHandler.deviceDriver import GetFunction

    def CallPopUps(message:str):
        PopUpsHandler.Clear()
        PopUpsHandler.Add(Type = PopUpTypeEnum.FatalError,
                          Message=message)
        PopUps_Screens.SetCaller(DriverMenu_Screens, "DriverMenu")
        PopUps_Screens.SetExiter(DriverMenu_Screens, "DriverMenu")
        PopUps_Screens.Call()

    Debug.Log("[0]: Getting CheckIntegrity")
    try:
        function = GetFunction("CheckIntegrity", driverName)
        Debug.Log(">>> SUCCESS")
    except:
        Debug.Error("Failed to get function")
        CallPopUps(_("Kontrol failed to get the following function from this device driver: ") + "CheckIntegrity")
        Debug.End()
        return Execution.Crashed

    Debug.Log("[1]: Executing CheckIntegrity")
    try:
        integrity = function()
        Debug.Log(">>> SUCCESS")
    except:
        Debug.Error("Failed to execute the function.")
        CallPopUps(_("A fatal error occured while executing this device driver's function: ") + "CheckIntegrity")
        Debug.End()
        return Execution.Crashed

    Debug.Log("[2]: Getting error message")
    driverMessage = GetErrorMessageFunction()
    if driverMessage != None:
        driverMessage = " " + _("Driver error message: ") + driverMessage

    Debug.Log("[2]: Handling driver's integrity")
    if(integrity == FileIntegrity.Good):
        Debug.Log(">>> SUCCESS")
        Debug.End()
        return Execution.Passed

    if(integrity == Execution.ByPassed):
        Debug.Error("Function bypassed")

        message = _("The device driver is bypassing its Integrity check.") + " " + _("Kontrol cannot launch this device driver safely.")
        if driverMessage != None:
            message = message + driverMessage

        CallPopUps(message)
        Debug.End()
        return Execution.Failed

    if(integrity == Execution.Incompatibility):
        Debug.Error("Function Incompatibility")

        message = _("The device driver encountered an incompatibility issue while performing a self check.")
        if driverMessage != None:
            message = message + driverMessage

        CallPopUps(message)
        Debug.End()
        return Execution.Failed

    if(integrity == Execution.Failed):
        Debug.Error("Function failed")

        message = _("The device driver failed its self check.") + " " + _("Kontrol cannot launch this device driver safely.")
        if driverMessage != None:
            message = message + driverMessage

        CallPopUps(message)
        Debug.End()
        return Execution.Failed

    if(integrity == Execution.NoConnection):
        Debug.Error("Function failed due to no connection.")

        message = _("The device driver cannot work without a connection.")
        if driverMessage != None:
            message = message + driverMessage

        CallPopUps(message)
        Debug.End()
        return Execution.Failed

    if(integrity == Execution.Crashed):
        Debug.Error("Function crashed")

        message = _("The device driver crashed while attempting to self check.") + " " + _("Kontrol cannot launch this device driver safely.")
        if driverMessage != None:
            message = message + driverMessage

        CallPopUps(message)
        Debug.End()
        return Execution.Failed

    if(integrity == Execution.Unecessary):
        Debug.Error("Function unecessary")

        message = _("The device driver thinks it's unecessesary to perform a self check. The driver cannot launch until a proper integrity result is given.")
        if driverMessage != None:
            message = message + driverMessage

        CallPopUps(message)
        Debug.End()
        return Execution.Failed

    if(integrity == FileIntegrity.Outdated):
        Debug.Error("Driver is outdated")

        message = _("The device driver says it's Outdated.") + " " + _("Kontrol cannot launch this device driver safely.")
        if driverMessage != None:
            message = message + driverMessage

        CallPopUps(message)
        Debug.End()
        return Execution.Failed

    if(integrity == FileIntegrity.Error):
        Debug.Error("Driver is error")

        message = _("The device driver returned Error when performing its self check.") + " " + _("Kontrol cannot launch this device driver safely.")
        if driverMessage != None:
            message = message + driverMessage

        CallPopUps(message)
        Debug.End()
        return Execution.Failed

    if(integrity == FileIntegrity.Corrupted):
        Debug.Error("Driver is Corrupted")

        message = _("The device driver identified a corruption within itself.") + " " + _("Kontrol cannot launch this device driver safely.")
        if driverMessage != None:
            message = message + driverMessage

        CallPopUps(message)
        Debug.End()
        return Execution.Failed

    if(integrity == FileIntegrity.Blank):
        Debug.Error("Driver is blank")

        message = _("The device driver sees itself as empty.") + " " + _("Kontrol cannot launch this device driver safely.")
        if driverMessage != None:
            message = message + driverMessage

        CallPopUps(message)
        Debug.End()
        return Execution.Failed
    
    if(integrity == FileIntegrity.Ahead):
        Debug.Error("Driver is blank")

        message = _("The device driver returned Ahead when performing its self check.") + " " + _("Kontrol cannot launch this device driver safely.")
        if driverMessage != None:
            message = message + driverMessage

        CallPopUps(message)
        Debug.End()
        return Execution.Failed

    Debug.Error("Incorrect returned value from CheckIntegrity")
    message = _("The self check executed by the device driver returned an unkown result that Kontrol cannot comprehend.")
    message = message + " " + ("Returned value is: ") + str(integrity)
    CallPopUps(message)
    Debug.End()
    return Execution.Incompatibility
# ------------------------------------------------------------------
def HandleDriverLaunch(driverName, GetErrorMessageFunction) -> Execution:
    """
        HandleDriverLaunch:
        ======================
        Summary:
        --------
        This function is made to remove some copy pasted lines of code
        and to make the program clearer to read. This function handles
        the launch of a device driver.

        Function:
        ---------
        First attempts to get Launch from driverName.
        If that fails, a pop up is called.
        Otherwise, it attempts to execute the Launch function.
        Popups are built depending on the Execution results.

        if everything is well with the integrity of the device driver,
        then `Execution.Passed` is returned.
    """
    Debug.Start("HandleDriverLaunch")
    from ..Local.FileHandler.deviceDriver import GetFunction

    def CallPopUps(message:str):
        PopUpsHandler.Clear()
        PopUpsHandler.Add(Type = PopUpTypeEnum.FatalError,
                          Message=message)
        PopUps_Screens.SetCaller(DriverMenu_Screens, "DriverMenu")
        PopUps_Screens.SetExiter(DriverMenu_Screens, "DriverMenu")
        PopUps_Screens.Call()

    Debug.Log("[0]: Getting Launch")
    try:
        function = GetFunction("Launch", driverName)
        Debug.Log(">>> SUCCESS")
    except:
        Debug.Error("Failed to get function")
        CallPopUps(_("Kontrol failed to get the following function from this device driver: ") + "Launch")
        Debug.End()
        return Execution.Crashed

    Debug.Log("[1]: Executing Launch")
    # try:
    execution = function()
    Debug.Log(">>> SUCCESS")
    # except:
        # Debug.Error("Failed to execute the function.")
        # CallPopUps(_("A fatal error occured while executing this device driver's function: ") + "Launch")
        # Debug.End()
        # return Execution.Crashed

    Debug.Log("[2]: Getting error message")
    driverMessage = GetErrorMessageFunction()
    if driverMessage != None:
        driverMessage = " " + _("Driver error message: ") + driverMessage

    Debug.Log("[3]: Handling execution results")

    if(execution == Execution.Passed):
        Debug.Log("Device driver launched successfully.")
        Debug.End()
        return Execution.Passed

    if(execution == Execution.ByPassed):
        Debug.Error("Function bypassed")

        message = _("The device driver is bypassing its launch.") + " " + _("Kontrol cannot launch this device driver safely.")
        if driverMessage != None:
            message = message + driverMessage

        CallPopUps(message)
        Debug.End()
        return Execution.Failed

    if(execution == Execution.Incompatibility):
        Debug.Error("Function Incompatibility")

        message = _("The device driver encountered an incompatibility issue while launching.") + " " + _("Kontrol failed to execute this function.")
        if driverMessage != None:
            message = message + driverMessage

        CallPopUps(message)
        Debug.End()
        return Execution.Failed

    if(execution == Execution.Failed):
        Debug.Error("Function failed")

        message = _("The device driver failed to launch.")
        if driverMessage != None:
            message = message + driverMessage

        CallPopUps(message)
        Debug.End()
        return Execution.Failed

    if(execution == Execution.NoConnection):
        Debug.Error("Function failed due to no connection.")

        message = _("The device driver cannot work without a connection.") + " " + _("Kontrol failed to execute this function.")
        if driverMessage != None:
            message = message + driverMessage

        CallPopUps(message)
        Debug.End()
        return Execution.Failed

    if(execution == Execution.Crashed):
        Debug.Error("Function crashed")

        message = _("The device driver crashed while attempting to launch.") + " " + _("Kontrol failed to execute this function.")
        if driverMessage != None:
            message = message + driverMessage

        CallPopUps(message)
        Debug.End()
        return Execution.Failed

    if(execution == Execution.Unecessary):
        Debug.Error("Function unecessary")

        message = _("The device driver thinks it's unecessesary perform a launch? The driver cannot launch until a proper execution result is given.")
        if driverMessage != None:
            message = message + driverMessage

        CallPopUps(message)
        Debug.End()
        return Execution.Failed

    Debug.Error("The device driver returned an unknown value.")
    message = _("The launch executed by the device driver returned an unkown result that Kontrol cannot comprehend.")
    message = message + " " + ("Returned value is: ") + str(execution)
    CallPopUps(message)
    Debug.End()
#====================================================================#
# Screen class
#====================================================================#
LoadingLog.Class("DriverMenu_Screens")
class DriverMenu_Screens:
    """
        DriverMenu_Screens:
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
        DriverMenu_Screens._exitClass = screenClass
        DriverMenu_Screens._exitName  = screenName

        DriverMenu_Screens._exitTransition = transition
        DriverMenu_Screens._exitDuration = duration
        DriverMenu_Screens._exitDirection = direction
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
        DriverMenu_Screens._callerClass = screenClass
        DriverMenu_Screens._callerName  = screenName

        DriverMenu_Screens._callerTransition = transition
        DriverMenu_Screens._callerDuration = duration
        DriverMenu_Screens._callerDirection = direction
        return False

    def _Exit() -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("DriverMenu_Screens -> _Exit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(DriverMenu_Screens._exitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(DriverMenu_Screens._exitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                DriverMenu_Screens._exitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(DriverMenu_Screens._exitClass(name=DriverMenu_Screens._exitName))
        except:
            Debug.Error("AppLoading -> Exception occured.")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = DriverMenu_Screens._exitTransition()
        AppManager.manager.transition.duration = DriverMenu_Screens._exitDuration
        AppManager.manager.transition.direction = DriverMenu_Screens._exitDirection

        # try:
        AppManager.manager.current = DriverMenu_Screens._exitName
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
        Debug.Start("DriverMenu_Screens -> Call()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if caller class was specified
            # Debug.Log("Checking caller class")
            # if(DriverMenu_Screens._callerClass == None):
                # Debug.Error("No caller class specified.")
                # Debug.End()
                # return True

            # Debug.Log("Checking caller name")
            # if(DriverMenu_Screens._callerName == None):
                # Debug.Error("No caller name specified.")
                # Debug.End()
                # return True

            Debug.Log("Attempting to add widget")
            AppManager.manager.add_widget(DriverMenu(name="DriverMenu"))
        except:
            Debug.Error("Exception occured while handling Call()")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = DriverMenu_Screens._callerTransition()
        AppManager.manager.transition.duration = DriverMenu_Screens._callerDuration
        AppManager.manager.transition.direction = DriverMenu_Screens._callerDirection

        # try:
        AppManager.manager.current = "DriverMenu"
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
LoadingLog.Class("DriverMenu")
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
        self.Layout = MDFloatLayout()
        # Create a horizontal box layout offset by half the screen to center the first profile in view.
        self.driversBox = MDBoxLayout(size_hint=(1,1), pos_hint = {'top': 1, 'left': 0}, orientation='horizontal', spacing="100sp", padding = (50,50,50,50), size_hint_x=None)
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

        for driver in drivers:
            card = DeviceDriverCard(driverName=driver)
            card.PressedEnd = self.DriverPressed
            self.driversBox.add_widget(card)
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
    def DriverPressed(*args):
        """
            DriverPressed:
            ==============
            Summary:
            --------
            This function is used as a callback when device driver card is
            pressed. It will attempt to call the Launch function of that
            device driver.
        """
        Debug.Start("DriverPressed")
        from Programs.Local.FileHandler.deviceDriver import GetFunction
        card = args[1]
        driverName = card.Name.text

        GetError = GetFunction("GetErrorMessage", driverName)

        execution = HandleDriverIntegrity(driverName, GetError)
        if(execution == Execution.Passed):
            HandleDriverLaunch(driverName, GetError)
        Debug.End()
# ------------------------------------------------------------------------

LoadingLog.End("DriverMenu.py")