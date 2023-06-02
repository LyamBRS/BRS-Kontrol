#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Programs.Local.FileHandler.Profiles import GetTemporary, ProfileHandler
LoadingLog.Start("Account.py")
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
from Libraries.BRS_Python_Libraries.BRS.Utilities.addons import Addons
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
from kivy.uix.screenmanager import Screen, SlideTransition
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import("KivyMD")
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.floatlayout import MDFloatLayout
#endregion
#region ------------------------------------------------------ Kontrol
LoadingLog.Import("Local")
from ..Local.GUI.Navigation import AppNavigationBar
from ..Local.GUI.Cards import WidgetCard
from ..Local.Hardware.RGB import KontrolRGB
#endregion
#====================================================================#
# Functions
#====================================================================#
def DeleteAccount(*args):
    """
        DeleteAccount:
        ==============
        Summary:
        --------
        Calling this deletes the currently loaded profile and deletes
        their JSON from any BrSpand drivers or Device Drivers.
    """
    Debug.Start("DeleteAccount")
    #region --------------------- Deleting profile
    Addons.UnloadProfile(ProfileHandler.currentName)
    Addons.ClearProfile(ProfileHandler.currentName)
    ProfileHandler.Delete()
    #endregion
    #region ------------------- Imports
    Debug.Log("Importing dependencies for ProfileMenu handling")
    from .ProfileMenu import ProfileMenu_Screens
    #endregion
    #region ------------------- Load to Profile_Menu
    Debug.Log("Returning to ProfileMenu_Screens")
    ProfileMenu_Screens.Call()
    #endregion
    Debug.End()
# -------------------------------------------------------------------
def DeletePressed(*args):
    """
        DeletePressed:
        ==============
        Summary:
        --------
        This function is a callback function called when the Delete
        card is pressed. This function handles the deletion of the
        Loaded profile and then calls the function that LogsOut the
        user.

        Firstly, the user is asked if he really wants to delete the
        profile prior to deleting it. This is done through the PopUps
        handler.
    """
    Debug.Start("DeletePressed")

    #region ------------------- Imports
    Debug.Log("Importing dependencies for Pop Ups handling")
    from .PopUps import PopUpsHandler,PopUps_Screens, PopUpTypeEnum
    from .DriverMenu import DriverMenu_Screens
    from .ProfileMenu import ProfileMenu_Screens
    #endregion
    #region ------------------- PopUps Creation
    PopUpsHandler.Clear()
    PopUpsHandler.Add(Icon              = "delete",
                      Message           = _("Are you sure you want to delete this account? You will not be able to recover this account. Cache associated with this account inside of drivers and cards will also be deleted permanently."),
                      Type              = PopUpTypeEnum.Custom,
                      ButtonAText       = _("Delete account"),
                      ButtonBText       = _("Cancel"),
                      ButtonAHandler    = None,
                      ButtonBHandler    = AccountMenu_Screens.Call)
    PopUpsHandler.Add(Icon              = "delete",
                      Message           = _("Are you really sure you want to permanently delete this account?"),
                      Type              = PopUpTypeEnum.Custom,
                      ButtonAText       = _("Cancel"),
                      ButtonBText       = _("Delete account"),
                      ButtonAHandler    = AccountMenu_Screens.Call,
                      ButtonBHandler    = DeleteAccount)
    #endregion
    #region ------------------- PopUps calling
    Debug.Log("Handling PopUps_Screens")
    PopUps_Screens.SetCaller(AccountMenu_Screens, "AccountMenu")
    PopUps_Screens.SetExiter(None, None)

    Debug.Log("Calling PopUps")
    PopUps_Screens.Call()
    #endregion
    Debug.End()
# -------------------------------------------------------------------
def LogOutPressed(*args):
    """
        LogOutPressed:
        ==============
        Summary:
        --------
        This function is a callback function called when the LogOut
        card is pressed. This function can also just be called to 
        log out.

        It is preferable that you copy this function for your logout
        purposes. Please note that a pop up is generated prompting
        the user to answer yes or no to leaving the application.
    """
    Debug.Start("LogOutPressed")

    #region ------------------- Imports
    Debug.Log("Importing dependencies for Pop Ups handling")
    from .PopUps import PopUpsHandler,PopUps_Screens, PopUpTypeEnum
    from .DriverMenu import DriverMenu_Screens
    from .ProfileMenu import ProfileMenu_Screens
    #endregion

    #region ------------------- PopUps Creation
    Debug.Log("Creating necessary pop ups")
    PopUpsHandler.Clear()
    PopUpsHandler.Add(Icon              = "logout",
                      Message           = _("Are you sure you want to log out of your account? You need to be logged in to close Kontrol."),
                      Type              = PopUpTypeEnum.Custom,
                      ButtonAText       = _("Log out"),
                      ButtonBText       = _("Cancel"),
                      ButtonAHandler    = ProfileMenu_Screens.Call,
                      ButtonBHandler    = AccountMenu_Screens.Call)
    #endregion

    #region ------------------- PopUps calling
    Debug.Log("Handling PopUps_Screens")
    PopUps_Screens.SetCaller(AccountMenu_Screens, "AccountMenu")
    PopUps_Screens.SetExiter(None, None)

    Debug.Log("Calling PopUps")
    PopUps_Screens.Call()
    #endregion
    Debug.End()
# -------------------------------------------------------------------
def EditProfilePressed(*args):
    """
        EditProfilePressed:
        ==============
        Summary:
        --------
        This function is a callback function called when the Edit Profile
        card is pressed. This function calls directly the ProfileCreation_Screen
        in "Editing" mode.
    """
    Debug.Start("EditProfilePressed")

    #region ------------------- Imports
    Debug.Log("Importing dependencies for ProfileCreation handling")
    from .ProfileCreation import ProfileCreation_Screens
    from ..Local.FileHandler.Profiles import SetTemporary
    #endregion

    #region ------------------- ProfileCreation_Screens handling
    Debug.Log("Setting up ProfileCreation_Screens")
    ProfileCreation_Screens.SetCaller(AccountMenu_Screens, "AccountMenu")
    ProfileCreation_Screens.SetBadExiter(AccountMenu_Screens, "AccountMenu")
    ProfileCreation_Screens.SetGoodExiter(AccountMenu_Screens, "AccountMenu")
    ProfileCreation_Screens.Mode = "Editing"
    #endregion

    #region ------------------- Profile loading into Temporary
    Debug.Log("Setting temporary as the current profile")
    SetTemporary(ProfileHandler.rawJson.jsonData.copy())
    #endregion

    #region ------------------- Profile loading into Temporary
    Debug.Log("Calling ProfileCreation")
    ProfileCreation_Screens.Call()
    #endregion
    Debug.End()
#====================================================================#
# Screen class
#====================================================================#
LoadingLog.Class("AccountMenu_Screens")
class AccountMenu_Screens:
    """
        AccountMenu_Screens:
        ================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`AccountMenu`.

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
        AccountMenu_Screens._exitClass = screenClass
        AccountMenu_Screens._exitName  = screenName

        AccountMenu_Screens._exitTransition = transition
        AccountMenu_Screens._exitDuration = duration
        AccountMenu_Screens._exitDirection = direction
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
        AccountMenu_Screens._callerClass = screenClass
        AccountMenu_Screens._callerName  = screenName

        AccountMenu_Screens._callerTransition = transition
        AccountMenu_Screens._callerDuration = duration
        AccountMenu_Screens._callerDirection = direction
        return False

    def _Exit() -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("AccountMenu_Screens -> _Exit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(AccountMenu_Screens._exitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(AccountMenu_Screens._exitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                AccountMenu_Screens._exitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(AccountMenu_Screens._exitClass(name=AccountMenu_Screens._exitName))
        except:
            Debug.Error("AppLoading -> Exception occured.")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = AccountMenu_Screens._exitTransition()
        AppManager.manager.transition.duration = AccountMenu_Screens._exitDuration
        AppManager.manager.transition.direction = AccountMenu_Screens._exitDirection

        # try:
        AppManager.manager.current = AccountMenu_Screens._exitName
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
        Debug.Start("DriverMenu_Screens -> Call()")
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
            AppManager.manager.add_widget(AccountMenu(name="AccountMenu"))
        except:
            Debug.Error("Exception occured while handling Call()")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = AccountMenu_Screens._callerTransition()
        AppManager.manager.transition.duration = AccountMenu_Screens._callerDuration
        AppManager.manager.transition.direction = AccountMenu_Screens._callerDirection

        # try:
        AppManager.manager.current = "AccountMenu"
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
LoadingLog.Class("AccountMenu")
class AccountMenu(Screen):
    """
        AccountMenu:
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
        Debug.Start("AccountMenu -> __init__")
        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
        """
        Debug.Start("AccountMenu -> on_pre_enter")
        KontrolRGB.FastLoadingAnimation()
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
        Layout = MDFloatLayout()
        # Create a horizontal box layout offset by half the screen to center the first profile in view.
        cardBox = MDBoxLayout(size_hint=(1,1), pos_hint = {'top': 1, 'left': 0}, orientation='horizontal', spacing="100sp", padding = (50,50,50,50), size_hint_x=None)
        cardBox.bind(minimum_width = cardBox.setter('width'))

        # Create the scroll view and add the box layout to it
        scroll = MDScrollView(pos_hint = {'top': 1, 'left': 0}, scroll_type=['bars','content'], size_hint = (1,1))
        scroll.smooth_scroll_end = 10

        # Add widgets
        scroll.add_widget(cardBox)
        #endregion
        #region ---------------------------- ToolBar
        ToolBar = AppNavigationBar(pageTitle=_("Account Parameters"))
        #endregion

        # Card widgets
        EditCard = WidgetCard(_("Edit"), "account-edit")
        LogOutCard = WidgetCard(_("Log out"), "logout")
        DeleteCard = WidgetCard(_("Delete"), "delete-forever", True)

        DeleteCard.PressedEnd = DeletePressed
        LogOutCard.PressedEnd = LogOutPressed
        EditCard.PressedEnd = EditProfilePressed

        Layout.add_widget(scroll)
        Layout.add_widget(ToolBar.ToolBar)
        Layout.add_widget(ToolBar.NavDrawer)

        cardBox.add_widget(EditCard)
        cardBox.add_widget(LogOutCard)
        cardBox.add_widget(DeleteCard)

        self.add_widget(background)
        self.add_widget(Layout)
        Debug.End()
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            Function called when the screen is fully entered in view.
            In this case, once the view is fully loaded, the cards
            will slowly elevate to the wanted value.
        """
        Debug.Start("DriverMenu -> on_enter")
        KontrolRGB.DisplayDefaultColor()
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

LoadingLog.End("DriverMenu.py")