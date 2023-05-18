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
# from Programs.Pages.AppLoading import AppLoading, AppLoading_Screens
LoadingLog.Start("PopUps.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import os
from enum import Enum
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Rounding, Shadow
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
LoadingLog.Import("KontrolRGB")
from ..Local.Hardware.RGB import KontrolRGB
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
from kivy.uix.screenmanager import Screen,SlideTransition
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import("KivyMD")
from kivymd.color_definitions import colors
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton,MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
#endregion
#====================================================================#
# Enums
#====================================================================#
LoadingLog.Class("PopUpTypeEnum")
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
    Custom:int = 4
LoadingLog.Class("Keys")
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
    ButtonAText:int = 4
    ButtonBText:int = 5
    ButtonAHandler:int = 6
    ButtonBHandler:int = 7
#====================================================================#
# Pop up structure
#====================================================================#
LoadingLog.GlobalVariable("PopUpStructure")
PopUpStructure = {
    Keys.Icon : "exclamation",
    Keys.Message : "Message",
    Keys.Type : PopUpTypeEnum.Remark,
    Keys.CanContinue : True,
    Keys.ButtonAText : "Ok",
    Keys.ButtonBText : "None",
    Keys.ButtonAHandler : None,
    Keys.ButtonBHandler : None
}
"""
    the template structure used to build pop ups
"""
#====================================================================#
# Functions
#====================================================================#
LoadingLog.Class("PopUpsHandler")
class PopUpsHandler:
    """
        PopUpsHandler:
        ==============
        Summary:
        --------
        This class handles the creation and clearing of the PopUps
        buffer. Use this class to create a series of popups that will
        be hosted on a screen.

        How to use:
        -----------
        To use this class, you need to use the 2 main methods provided
        in it. These methods are the following:
            - :ref:`Add`
            - :ref:`Clear`
        For more information, see their individual DocStrings.

        How to call:
        -----------
        After you've created your PopUps, using this class, you will
        need to set the `PopUps_Screens` transitional screen manager class
        If no exit classes are refered in your pop ups, the Exiter will be called.
    """
    #region   --------------------------- MEMBERS
    PopUps:list = []
    _PopUpsWidgets:list = []
    _PopUpTypes:list = []
    """
        Used to keep track of the PopUp type
        being currently displayed.
    """
    #endregion
    #region   --------------------------- METHODS
    LoadingLog.Method("Clear")
    def Clear():
        """
            Clear:
            ------
            Clears all pop ups in the pop up list.
            Before adding new pop ups, call this to ensure
            that no other screens forgot to call theirs.
        """
        Debug.Start("PopUps -> Clear")
        PopUpsHandler.PopUps.clear()
        PopUpsHandler._PopUpsWidgets.clear()
        Debug.End()
    # -------------------------------------------
    LoadingLog.Method("Add")
    def Add(Type:Keys, Icon:str = "blank", Message:str=_("Empty pop up"), CanContinue:bool=True, ButtonAText:str="Ok", ButtonBText:str="Cancel", ButtonAHandler=None, ButtonBHandler=None):
        """
            Add:
            ====
            Summary:
            --------
            Adds a pop up to the list of daisy chain pop ups that will
            be displayed to the user.

            Parameters:
            -----------
                - :ref:`Type` : Refer to :ref:`PopUpTypeEnum` to see all the types of PopUps
                - :ref:`Icon` : The name of a KivyMD icon.
                - :ref:`Message` : the message to display to the user.
                - :ref:`CanContinue` : If set to false, the application will close after the button is pressed
                - :ref:`ButtonAText` : The text displayed on the only button or the right button
                - :ref:`ButtonBText` : The text displayed on the second button. Keep empty for only one button

                - :ref:`ButtonAHandler`: Put a function here if you want the pop up to do something when a button is pressed.
                - :ref:`ButtonBHandler`: Put a function here if you want the pop up to do something when a button is pressed.

            Note:
            -----
            Leaving the `ButtonXHandler` parameters empty will cause the PopUps to transition to the next one.
            Otherwise,
            the PopUps list will be cleared, then the PopUps will navigate to the transitional screen specified when the corresponding
            button is pressed.
            If no popups button handler are specified, the PopUps_Screen caller and exiter will define where the application goes
            once all the popups are exhausted.
        """
        Debug.Start("Add")
        PopUpsHandler.PopUps.append({
            Keys.Icon : Icon,
            Keys.Message : Message,
            Keys.Type : Type,
            Keys.CanContinue : CanContinue,
            Keys.ButtonAText : ButtonAText,
            Keys.ButtonBText : ButtonBText,
            Keys.ButtonAHandler : ButtonAHandler,
            Keys.ButtonBHandler : ButtonBHandler,
        })
        Debug.End()
    # -------------------------------------------
    LoadingLog.Method("_AddWidget")
    def _AddWidget(widget):
        """
            Adds the widget reference to the list of widgets displayed
            in the scrollview.
        """
        PopUpsHandler._PopUpsWidgets.append(widget)
    #endregion
#====================================================================#
# Screen class
#====================================================================#
LoadingLog.Class("PopUps_Screens")
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

    def _Exit(*args) -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("PopUps -> _Exit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(PopUps_Screens._exitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(PopUps_Screens._exitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                PopUps_Screens._exitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Error("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(PopUps_Screens._exitClass(name=PopUps_Screens._exitName))
        except:
            Debug.Error("PopUps: _Exit() -> Failed in add_widget")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = PopUps_Screens._exitTransition()
        AppManager.manager.transition.duration = PopUps_Screens._exitDuration
        AppManager.manager.transition.direction = PopUps_Screens._exitDirection

        # try:
        AppManager.manager.current = PopUps_Screens._exitName
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
        Debug.Start("PopUps -> Call")
        # Attempt to add the screen class as a widget of the AppManager
        if(len(PopUpsHandler.PopUps) > 0):
            Debug.Log("Some pop ups can be displayed.")
            # try:
                # Check if exit class was specified
            Debug.Log("Checking caller class")
            if(PopUps_Screens._callerClass == None):
                Debug.Error("No caller class specified.")
                Debug.End()
                return True

            Debug.Log("Checking caller name")
            if(PopUps_Screens._callerName == None):
                Debug.Error("No caller name specified.")
                Debug.End()
                return True

            Debug.Log("Adding widget")
            AppManager.manager.add_widget(PopUps(name="PopUps"))
            # except:
                # Debug.Error("Exception occured while handling Call()")
                # Debug.End()
                # return True

            # Attempt to call the added screen
            AppManager.manager.transition = PopUps_Screens._callerTransition()
            AppManager.manager.transition.duration = PopUps_Screens._callerDuration
            AppManager.manager.transition.direction = PopUps_Screens._callerDirection
    
            try:
                AppManager.manager.current = "PopUps"
            except:
                Debug.Error("Failed to add PopUps as current screen.")
                Debug.End()
                return True

            Debug.End()
            return False
        else:
            Debug.Warn("No pop ups were queued, calling exit immediately.")
            PopUps_Screens._Exit()
            Debug.End()
            return True
    #endregion
#====================================================================#
# Main Function
#====================================================================#
LoadingLog.Class("PopUps")
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
    LoadingLog.Method("__init__")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("PopUps")
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
        Debug.Start("PopUps -> on_pre_enter")
        self.padding = 25
        self.spacing = 25

        #region ---- Background
        from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
        from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
        path = os.getcwd()

        background = GetBackgroundImage(AppendPath(path, "/Libraries/Backgrounds/PopUps/Dark.png"),
                                        AppendPath(path, "/Libraries/Backgrounds/PopUps/Light.png"))
        #endregion

        #region ---- Main Layout
        self.Layout = MDBoxLayout()
        #endregion

        #region ---- ScrollView N widget
        self.CardLayout = MDBoxLayout(orientation='horizontal', spacing="100sp", padding = ("50sp","50sp","50sp","50sp"), size_hint_x=None)
        self.CardLayout.bind(minimum_width = self.CardLayout.setter('width'))

        # Create the scroll view
        self.Layout.ScrollView = MDScrollView(scroll_type=['bars'])
        self.Layout.ScrollView.scroll_timeout = 0 #So the scrollview cannot be scrolled.
        self.Layout.ScrollView.smooth_scroll_end = 10
        #endregion

        #region ---- Widgets
        firstPopUp:bool = False
        for popup in PopUpsHandler.PopUps:
            Debug.Log("Adding new pop up.")
            if(not firstPopUp):
                firstPopUp = True
                KontrolRGB.DisplayPopUpAnimation(popup[Keys.Type])
            Card = GetPopUpCard(popup)
            self.CardLayout.add_widget(Card)

            # For RGB displays when pop up changes.
            PopUpsHandler._PopUpTypes.append(popup[Keys.Type])
            PopUpsHandler._AddWidget(Card)
        #endregion

        #region ---- add_widgets
        self.add_widget(background)
        self.Layout.ScrollView.add_widget(self.CardLayout)
        self.Layout.add_widget(self.Layout.ScrollView)
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
        Debug.Log("Attempting to remove self from AppManager's widgets")
        self.clear_widgets()
        AppManager.manager.remove_widget(self)
        PopUpsHandler.Clear()
        Debug.End()
# ------------------------------------------------------------------------

#====================================================================#
LoadingLog.Function("GetPopUpCard")
def GetPopUpCard(profileStructure:dict) -> Widget:
    """
        GetPopUpCard:
        -------------
        This function returns you a card built based off the 
        :ref:`PopUpStructure`.

        You need to pass a profileStructure for this to build out of.
    """
    Debug.Start("GetPopUpCard")

    #region --------------------------- Set Card
    Card = MDCard()
    Card.orientation = "vertical"
    Card.radius = Rounding.default
    Card.elevation = Shadow.Elevation.default
    Card.shadow_softness = Shadow.Smoothness.default
    Card.size_hint_min = (Window.width - 100, Window.height - 100)
    Card.padding = "10sp"
    Layout = MDBoxLayout(orientation="vertical")
    #endregion

    #region --------------------------- Card widgets
    Icon = MDIconButton(icon = profileStructure[Keys.Icon], valign="center", halign="center", pos_hint={"center_x": 0.5, "center_y": 0.5})
    Icon.icon_size = "75sp"
    # Icon.theme_icon_color = "Secondary"
    Message = MDLabel(text = profileStructure[Keys.Message], valign="bottom", halign="center")
    Message.font_style = "H6"
    Message.theme_text_color = "Secondary"
    ButtonLayout = MDBoxLayout(orientation = "horizontal", spacing = "25sp", size_hint=(1,0.25), padding="10sp")
    ButtonA = MDFillRoundFlatButton(size_hint = (1,None), text=profileStructure[Keys.ButtonAText], font_style = "H5")
    ButtonB = MDFillRoundFlatButton(size_hint = (1,None), text=profileStructure[Keys.ButtonBText], font_style = "H5")
    #region ---- button function binding
    Debug.Log("Binding user functions to button's releases")
    if(profileStructure[Keys.ButtonAHandler] != None):
        ButtonA.bind(on_press = profileStructure[Keys.ButtonAHandler])

    if(profileStructure[Keys.ButtonBHandler] != None):
        ButtonB.bind(on_press = profileStructure[Keys.ButtonBHandler])

    Debug.Log("Binding self delete functions to button's releases")
    ButtonA.bind(on_release = AutoDestruction)
    ButtonB.bind(on_release = AutoDestruction)
    #endregion

    if(profileStructure[Keys.Type] == PopUpTypeEnum.Remark):
        Debug.Log("Building remark pop up")
        ButtonB = None

    if(profileStructure[Keys.Type] == PopUpTypeEnum.Question):
        Debug.Log("Building Question pop up")
        if(profileStructure[Keys.Icon] == "blank"):
            Icon.icon = "help"

    if(profileStructure[Keys.Type] == PopUpTypeEnum.Warning):
        Debug.Log("Building warning pop up")
        Icon.theme_icon_color = "Custom"
        Message.theme_text_color = "Custom"
        Icon.icon_color = get_color_from_hex(colors["Orange"]["500"])
        Message.text_color = get_color_from_hex(colors["Orange"]["500"])
        if(profileStructure[Keys.Icon] == "blank"):
            Icon.icon = "alert"
        ButtonB = None

    if(profileStructure[Keys.Type] == PopUpTypeEnum.FatalError):
        Debug.Log("Building fatal error pop up")
        Icon.icon = "alert-octagon"
        Icon.theme_icon_color = "Error"
        Icon.theme_text_color = "Error"
        Message.theme_text_color = "Error"
        ButtonB = None

    if(profileStructure[Keys.Type] == PopUpTypeEnum.Custom):
        Debug.Log("Building custom pop up.")
        if(ButtonB.text == "None"):
            ButtonB = None


    #endregion
    #region --------------------------- Add widgets
    Layout.add_widget(Icon)
    Layout.add_widget(Message)
    Card.add_widget(Layout)
    ButtonLayout.add_widget(ButtonA)

    if(ButtonB != None):
        ButtonLayout.add_widget(ButtonB)

    Card.add_widget(ButtonLayout)
    Debug.End()
    return Card
    #endregion
# -------------------------------------------------------------------
LoadingLog.Function("AutoDestruction")
def AutoDestruction(self, *args):
    """
        AutoDestruction:
        ----------------
        This function is a function that can be bind to a widget's
        callbacks. This function's purpose is to delete the widget
        which called this function to free up space in the
        ScrollView.
    """
    Debug.Start("AutoDestruction")
    Card = self.parent.parent
    ScrollView = Card.parent.parent

    # self.parent.parent.parent.remove_widget(self.parent.parent)
    Debug.Log("Removing self from list of pop up widgets.")
    try:
        PopUpsHandler._PopUpsWidgets.remove(Card)
        PopUpsHandler._PopUpTypes.pop(0)

        newType = PopUpsHandler._PopUpTypes[0]
        KontrolRGB.DisplayPopUpAnimation(newType)
    except:
        Debug.Error(">>> NO CARD TO REMOVE")

    Debug.Log("Getting first card from the list.")
    try:
        widget = PopUpsHandler._PopUpsWidgets[0]
    except:
        Debug.Warn("Out of pop ups")
        Debug.Warn("Exit to main menu")
        PopUps_Screens._Exit()
        Debug.End()
        return

    Debug.Log("Scrolling to next card...")
    Debug.Log(ScrollView.scroll_to(widget, padding=50))
    Debug.Log("SUCCESS")
    Debug.End()
#====================================================================#
LoadingLog.End("PopUps.py")
