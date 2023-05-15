#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from profile import Profile
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import FileIntegrity
from Programs.Local.Hardware.RGB import KontrolRGB
LoadingLog.Start("ProfileCreation.py")
#====================================================================#
# Imports
#====================================================================#
import os
from kivy.animation import Animation
from kivy.properties import StringProperty
# -------------------------------------------------------------------
from kivymd.uix.button import MDFillRoundFlatButton,MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard,MDSeparator
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField
from kivymd.icon_definitions import md_icons
from kivymd.color_definitions import palette,colors
from kivymd.app import MDApp
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, SlideTransition
# -------------------------------------------------------------------
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Rounding,Shadow
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import AppLanguage, _
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Programs.Local.FileHandler.Profiles import ProfileHandler, ProfileGenericEnum, ProfileThemeEnum, SetTemporary, structureEnum, CheckUsername, CheckPassword, CheckBiography, GetTemporary
from kivy.utils import get_color_from_hex
# -------------------------------------------------------------------
from ..Local.FileHandler import Profiles
from ..Pages.PopUps import PopUps_Screens,PopUpsHandler,PopUpTypeEnum
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineIconListItem,IconLeftWidget
#====================================================================#
# Variables
#====================================================================#
DefaultIconBannedWords = {
    "abjad",
    "access",
    "align",
    "alert",
    "alphabet",
    "archive",
    "arrow",
    "arrange",
    "axis",
    "border",
    "battery",
    "lock",
    "progress",
    "chat",
    "form",
    "crop",
    "cursor",
    "drag",
    "outline",
    "chevron",
    "chart",
    "cancel",
    "calendar",
    "circle",
    "cog",
    "edit",
    "off",
    "remove",
    "settings",
    "plus",
    "minus",
    "check",
    "clock",
    "box",
    "search",
    "comment",
    "refresh",
    "decimal",
    "delete",
    "sync",
    "marker",
    "distribute",
    "dock",
    "download",
    "flip",
    "folder",
    "format",
    "gesture",
    "menu",
    "message",
    "strength",
    "order",
    "page",
    "pan",
    "relation",
    "rewind",
    "rotate",
    "selection",
    "signal",
    "sort",
    "select",
    "step",
    "surround",
    "view",
    "source",
    "text",
    "call",
    "unfold",
    "vector",
    "share",
    "filter",
    "block",
}

ProfileIcons = []

# Creating the allowed icons list:
LoadingLog.Log("Creating profile icon list")
for key in md_icons.keys():
    keyWordList = key.split("-")
    isBanned = False
    for banned in DefaultIconBannedWords:
        if banned in keyWordList:
            isBanned = True
    
    if(not isBanned):
        ProfileIcons.append(key)
#====================================================================#
# Functions
#====================================================================#
class ProfileCreation_Screens:
    """
        ProfileCreation:
        ================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`ProfileCreation`.

        Description:
        ------------
        This class holds the different types of callers of the ProfileCreation
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
    Mode:str = "Creation"
    """
        Mode
        ====
        Summary:
        --------
        The mode member of :ref:`ProfileCreation_Screens` is used to
        indicate in which mode the profile creation screen bundle should
        operate. You need to manually load :ref:`ProfileHandler` into :ref:`Temporary`

        How to use:
        -----------
        The mode member only have 2 possible values.
            - `"Creation"`: This mode will create a new profile uppon completion
            - `"Editing"` : This mode will edit the profile that is loaded in :ref:`ProfileHandler`

        It is important that you set the mode before calling :ref:`Call` because who knows
        what the mode is left as before you call this.
    """

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
        ProfileCreation_Screens._goodExitClass = screenClass
        ProfileCreation_Screens._goodExitName  = screenName

        ProfileCreation_Screens._goodExitTransition = transition
        ProfileCreation_Screens._goodExitDuration = duration
        ProfileCreation_Screens._goodExitDirection = direction
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
        ProfileCreation_Screens._badExitClass = screenClass
        ProfileCreation_Screens._badExitName  = screenName

        ProfileCreation_Screens._badExitTransition = transition
        ProfileCreation_Screens._badExitDuration = duration
        ProfileCreation_Screens._badExitDirection = direction
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
        ProfileCreation_Screens._callerClass = screenClass
        ProfileCreation_Screens._callerName  = screenName

        ProfileCreation_Screens._callerTransition = transition
        ProfileCreation_Screens._callerDuration = duration
        ProfileCreation_Screens._callerDirection = direction
        return False

    def _BadExit() -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetBadExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("ProfileCreation -> _BadExit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(ProfileCreation_Screens._badExitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(ProfileCreation_Screens._badExitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                ProfileCreation_Screens._badExitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Error("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(ProfileCreation_Screens._badExitClass(name=ProfileCreation_Screens._badExitName))
        except:
            Debug.Error("ProfileCreation: _Exit() -> Failed in add_widget")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = ProfileCreation_Screens._badExitTransition()
        AppManager.manager.transition.duration = ProfileCreation_Screens._badExitDuration
        AppManager.manager.transition.direction = ProfileCreation_Screens._badExitDirection

        # try:
        AppManager.manager.current = ProfileCreation_Screens._badExitName
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
        Debug.Start("ProfileCreation -> _GoodExit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(ProfileCreation_Screens._goodExitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(ProfileCreation_Screens._goodExitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                ProfileCreation_Screens._goodExitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(ProfileCreation_Screens._goodExitClass(name=ProfileCreation_Screens._goodExitName))
        except:
            Debug.Error("ProfileCreation: _Exit() -> Failed in add_widget")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = ProfileCreation_Screens._goodExitTransition()
        AppManager.manager.transition.duration = ProfileCreation_Screens._goodExitDuration
        AppManager.manager.transition.direction = ProfileCreation_Screens._goodExitDirection

        # try:
        AppManager.manager.current = ProfileCreation_Screens._goodExitName
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
        Debug.Start("ProfileCreation -> Call")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking caller class")
            if(ProfileCreation_Screens._callerClass == None):
                Debug.Error("No caller class specified.")
                Debug.End()
                return True

            Debug.Log("Checking caller name")
            if(ProfileCreation_Screens._callerName == None):
                Debug.Error("No caller name specified.")
                Debug.End()
                return True

            Debug.Log("Adding widget")
            AppManager.manager.add_widget(ProfileCreation_Step1(name="ProfileCreation_Step1"))
        except:
            Debug.Error("Exception occured while handling Call()")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = ProfileCreation_Screens._callerTransition()
        AppManager.manager.transition.duration = ProfileCreation_Screens._callerDuration
        AppManager.manager.transition.direction = ProfileCreation_Screens._callerDirection

        # try:
        AppManager.manager.current = "ProfileCreation_Step1"
        # except:
            # Debug.Error("Failed to add ProfileLogin as current screen.")
            # Debug.End()
            # return True

        Debug.End()
        return False
    #endregion

#====================================================================#
# Functions
#====================================================================#
class CustomOneLineIconListItem(OneLineIconListItem):
    icon = StringProperty()

class IconListItem(CustomOneLineIconListItem):
    def __init__(self, **kwargs):
        Debug.Start("IconListItem")
        Debug.Log(kwargs)
        Debug.Log(f"self.icon -> {self.icon}")
        super(IconListItem, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        Bruh = IconLeftWidget()
        Bruh.icon = self.icon
        Bruh.theme_icon_color = "Hint"
        self.add_widget(Bruh)
        Debug.End()

def CreateScreenBase(self, title:str, stepType:str) -> None:
    """
        Creates the entire base of the profile creation screen.
        stepType:str -> "First", "Middle", "last"
    """
    Debug.Start("CreateScreenBase")
    
    Debug.Log("Creating Layouts")
    self.MainLayout = MDBoxLayout(spacing=10, padding=("20sp","20sp","20sp","20sp"), orientation="vertical")
    self.MiddleLayout = MDBoxLayout(spacing=10, padding=("20sp","20sp","20sp","20sp"), orientation="vertical")
    self.TopLayout = MDBoxLayout(padding=("20sp","20sp","20sp","20sp"), size_hint_y = 0.25)

    # region ---- Card
    Debug.Log("Creating Card and Card layouts")
    self.Card = MDCard(
                        elevation = Shadow.Elevation.default,
                        shadow_softness = Shadow.Smoothness.default,
                        radius=Rounding.default,
                        padding = 25,
                        orientation = "vertical"
                        )
    self.CardTop = MDBoxLayout(spacing=10, padding=("10sp","10sp","10sp","10sp"), orientation="vertical")
    self.CardBottom = MDBoxLayout(spacing=10, padding=("10sp","10sp","10sp","10sp"), orientation="horizontal")
    # endregion
    # region ---- Previous/Next
    Debug.Log("Creating Previous/Next buttons")
    self.Next = MDIconButton(text="chevron-right", icon="chevron-right")
    self.Next.icon_size = "75sp"
    self.Next.pos_hint={"center_x": 0.75, "center_y": 0.5}
    # self.Next.on_release = self.GoToNext

    if(stepType == "Middle"):
        self.Previous = MDIconButton(text="chevron-left", icon="chevron-left")
        self.Previous.icon_size = "75sp"
        self.Previous.pos_hint={"center_x": 0.25, "center_y": 0.5}
        self.Previous.on_release = self.GoToPrevious
        self.Next.on_release = self.GoToNext

    if(stepType == "First"):
        self.Previous = MDIconButton(text="close", icon="close")
        self.Previous.icon_size = "75sp"
        self.Previous.pos_hint={"center_x": 0.25, "center_y": 0.5}
        self.Previous.on_release = self.GoBack
        self.Next.on_release = self.GoToNext

    if(stepType == "Last"):
        self.Previous = MDIconButton(text="chevron-left", icon="chevron-left")
        self.Previous.icon_size = "75sp"
        self.Previous.pos_hint={"center_x": 0.25, "center_y": 0.5}
        self.Previous.on_release = self.GoToPrevious

        self.Next = MDIconButton(text="confirm", icon="account-check")
        self.Next.icon_size = "75sp"
        self.Next.pos_hint={"center_x": 0.25, "center_y": 0.5}
        self.Next.on_release = self.ConfirmProfile
    # endregion

    # Page title
    Debug.Log(f"Creating page title: {title}")
    self.PageTitle = MDLabel(text=title,
                                font_style = "H2",
                                halign = "center")

    # Top layout widgets
    self.TopLayout.add_widget(self.Previous)
    self.TopLayout.add_widget(self.PageTitle)
    self.TopLayout.add_widget(self.Next)

    Debug.End()
#====================================================================#
# Screens
#====================================================================#
class ProfileCreation_Step1(Screen):
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
        Debug.Start("ProfileCreation_Step1")
        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
            Builds the ProfileCreation_Step1 entirely
            The Language selection screen consists of a single card
            with a dropdown inside of it which contains all the application's
            available languages
        """
        Debug.Start("ProfileCreation_Step1: on_pre_enter")
        self.padding = 25
        self.spacing = 25

        Temporary = GetTemporary()

        Debug.Log("Setting Temporary profile's language to AppLanguage.Current")
        Temporary[structureEnum.Generic.value][ProfileGenericEnum.Language.value] = AppLanguage.Current

        CreateScreenBase(self, _("Select a language"), "First")

        #region ---- Background
        import os
        from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
        from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
        path = os.getcwd()

        background = GetBackgroundImage(AppendPath(path, "/Libraries/Backgrounds/ProfileCreation/Dark.png"),
                                        AppendPath(path, "/Libraries/Backgrounds/ProfileCreation/Light.png"))
        #endregion

        #region ---- Top Of Card
        self.HelloWorld = MDLabel(text=_("Hello, world!"),
                                 font_style = "H2",
                                 halign = "center")
        self.Separator = MDSeparator()
        self.SelectedLanguage = MDLabel(text=AppLanguage.Current,
                                        font_style = "H6",
                                        halign = "center")
        #endregion
        #region ---- DropDown
        self.SelectButton = MDFillRoundFlatButton()
        self.SelectButton.size_hint = (1,0.5)
        self.SelectButton.font_size = "32sp"
        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "earth",
                "text": language,
                "height": 56,
                "on_release": lambda x=language: self.SetNewLanguage(x),
                "opposite_colors" : True
            } for language in AppLanguage.AvailableLanguages
        ]
        self.menu = MDDropdownMenu(
            caller=self.SelectButton,
            items=menu_items,
            position="top",
            width_mult=4,
        )

        self.menu.opening_time = 0.5
        self.menu.size_hint = (1,1)

        self.SelectButton.text = _("Select")
        self.SelectButton.on_release = self.menu.open
        #endregion

        # Add widgets
        self.add_widget(background)
        self.CardTop.add_widget(self.HelloWorld)
        self.CardTop.add_widget(self.SelectedLanguage)
        self.CardTop.add_widget(self.Separator)
        self.CardBottom.add_widget(self.SelectButton)
        self.Card.add_widget(self.CardTop)
        self.Card.add_widget(self.CardBottom)
        self.MiddleLayout.add_widget(self.Card)

        self.MainLayout.add_widget(self.TopLayout)
        self.MainLayout.add_widget(self.MiddleLayout)
        self.add_widget(self.MainLayout)
        Debug.End()
        pass
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        KontrolRGB.DisplayDefaultColor()
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully left.
        """
        Debug.Start("on_leave")
        Debug.Log("Attempting to remove self from AppManager's widgets")
        self.clear_widgets()
        AppManager.manager.remove_widget(self)
        Debug.End()
        self.clear_widgets()
# ------------------------------------------------------------------------
    def GoBack(self, *args):
        """
            Function to go back to `ProfileMenu.py`
        """
        
        if(ProfileCreation_Screens.Mode == "Editing"):
            Debug.Warn("Reloading the profile")
            ProfileHandler.LoadProfile(ProfileHandler.rawJson)
            Debug.Log(">>> SUCCESS")
        
        if (ProfileCreation_Screens._BadExit()):
            PopUpsHandler.Clear()
            PopUpsHandler.Add(PopUpTypeEnum.FatalError, Icon="bug", Message=("An error occured while attempting to go back to the previously loaded screen. The application needs to be restarted."))
            PopUps_Screens.SetCaller(PopUps_Screens._callerClass, PopUps_Screens._callerName)
            PopUps_Screens.Call()
# ------------------------------------------------------------------------
    def GoToNext(self, *args):
        """
            Function to goes to step 2 of the profile creation setup
        """
        AppManager.manager.add_widget(ProfileCreation_Step2(name="ProfileCreation_Step2"))
        AppManager.manager.transition.direction = "left"
        AppManager.manager.current = "ProfileCreation_Step2"
# ------------------------------------------------------------------------
    def SetNewLanguage(self, language:str):
        """
            Callback function of the dropdown allowing it to
            set a new language.
        """
        Debug.Start("SetNewLanguage")
        Debug.Log(f"Loading new selected language: {language}")
        AppLanguage.LoadLanguage(language)

        # - Update the application's displayed text
        Debug.Log("Retranslating page's elements")
        self.PageTitle.text = _("Select a language")
        self.HelloWorld.text = _("Hello, world!")
        self.SelectButton.text = _("Select")
        self.SelectedLanguage.text = AppLanguage.Current

        Debug.Log("Setting new language in temporary profile class")
        Temporary = GetTemporary()
        Temporary[structureEnum.Generic.value][ProfileGenericEnum.Language.value] = AppLanguage.Current
        SetTemporary(Temporary)
        Debug.Warn(f"Temporary profile now uses: {Temporary[structureEnum.Generic.value][ProfileGenericEnum.Language.value]}")

        # Closing drop down menu
        self.menu.dismiss()
        Debug.End()
#====================================================================#
class ProfileCreation_Step2(Screen):
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
        Debug.Start("ProfileCreation_Step2")
        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
            Builds the ProfileCreation_Step1 entirely
            The Language selection screen consists of a single card
            with a dropdown inside of it which contains all the application's
            available languages
        """
        Debug.Start("ProfileCreation_Step2: on_pre_enter")
        self.padding = 25
        self.spacing = 25
        Temporary = GetTemporary()
        colorIconSize = Window.height / 35
        colorIconFontSize = Window.height / 4
        colorIconSpacing = (Window.width / 80) - 20

        #region ---- Background
        import os
        from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
        from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
        path = os.getcwd()

        self.background = GetBackgroundImage(AppendPath(path, "/Libraries/Backgrounds/ProfileCreation/DarkFlip.png"),
                                        AppendPath(path, "/Libraries/Backgrounds/ProfileCreation/LightFlip.png"))
        #endregion

        style = MDApp.get_running_app().theme_cls.theme_style
        primary = MDApp.get_running_app().theme_cls.primary_palette
        accent = MDApp.get_running_app().theme_cls.accent_palette

        Debug.Log("Setting Temporary profile's themes to MDApp's current")
        Temporary[structureEnum.Generic.value][ProfileGenericEnum.Language.value] = AppLanguage.Current

        CreateScreenBase(self, _("Select a theme"), "Middle")

        #region ---- Top Of Card
        self.ThemeStyleLayout = MDBoxLayout(spacing=colorIconSpacing,  padding=(0,0,0,0), orientation="horizontal")
        self.PrimaryLayout = MDBoxLayout(spacing=colorIconSpacing,     padding=(0,0,0,0), orientation="horizontal")
        self.AccentLayout = MDBoxLayout(spacing=colorIconSpacing,      padding=(0,0,0,0), orientation="horizontal")

        self.ThemeStyleLabel = MDLabel(text=_("Theme"),
                                        font_style = "H5",
                                        halign = "left")

        self.PrimaryLabel = MDLabel(text=_("Primary color"),
                                        font_style = "H5",
                                        halign = "left")

        self.AccentLabel = MDLabel(text=_("Accent color"),
                                        font_style = "H5",
                                        halign = "left")
        #endregion

        # region ---- Theme Buttons
        self.PrimaryColorsList:list = []
        for color in palette:
            Primary = MDIconButton()
            Primary.text = color
            Primary.theme_icon_color = "Custom"
            Primary.icon_color = get_color_from_hex(colors[color]["500"])
            Primary.line_width = 1.5
            Primary.icon_size = colorIconSize
            Primary.font_size = colorIconFontSize


            if color == primary:
                Primary.line_color = Primary.icon_color
                Primary.icon = "checkbox-marked-circle"

            Primary.on_press = self.PrimaryPressed
            self.PrimaryColorsList.append(Primary)
            self.PrimaryLayout.add_widget(Primary)

        self.AccentColorsList:list = []
        for color in palette:
            Accent = MDIconButton()
            Accent.text = color
            Accent.theme_icon_color = "Custom"
            Accent.icon_color = get_color_from_hex(colors[color]["500"])
            Accent.line_width = 1.5
            Accent.icon_size = colorIconSize

            if color == accent:
                Accent.line_color = Accent.icon_color
                Accent.icon = "checkbox-marked-circle"

            Accent.on_press = self.AccentPressed
            self.AccentColorsList.append(Accent)
            self.AccentLayout.add_widget(Accent)

        # Theme buttons
        self.ThemeColorsList:list = []
        Light = MDIconButton(text = "Light", line_width = 1.5)
        Dark = MDIconButton(text = "Dark", line_width = 1.5)
        Light.line_width = 1.5
        Dark.line_width = 1.5
        Light.icon_size = colorIconSize
        Dark.icon_size = colorIconSize
        Light.theme_icon_color = "Custom"
        Dark.theme_icon_color = "Custom"
        Light.icon_color = (0.8,0.8,0.8,1)
        Dark.icon_color = (0,0,0,1)

        if style == "Light":
            Light.line_color = Light.icon_color
            Light.icon = "checkbox-marked-circle"

        if style == "Dark":
            Dark.line_color = Dark.icon_color
            Dark.icon = "checkbox-marked-circle"

        Light.on_press = self.ThemePressed
        Dark.on_press = self.ThemePressed
        self.ThemeColorsList.append(Light)
        self.ThemeColorsList.append(Dark)
        self.ThemeStyleLayout.add_widget(Light)
        self.ThemeStyleLayout.add_widget(Dark)
        #endregion

        # Save current theme_cls in Temporary
        Temporary[structureEnum.Theme.value][ProfileThemeEnum.Style.value] = style
        Temporary[structureEnum.Theme.value][ProfileThemeEnum.Primary.value] = primary
        Temporary[structureEnum.Theme.value][ProfileThemeEnum.Accent.value] = accent

        # Add widgets
        self.add_widget(self.background)
        self.Card.add_widget(self.ThemeStyleLabel)
        self.Card.add_widget(self.ThemeStyleLayout)
        self.Card.add_widget(self.PrimaryLabel)
        self.Card.add_widget(self.PrimaryLayout)
        self.Card.add_widget(self.AccentLabel)
        self.Card.add_widget(self.AccentLayout)
        self.MiddleLayout.add_widget(self.Card)

        self.MainLayout.add_widget(self.TopLayout)
        self.MainLayout.add_widget(self.MiddleLayout)
        self.add_widget(self.MainLayout)

        SetTemporary(Temporary)
        Debug.End()
        pass
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully left.
        """
        Debug.Start("on_leave")
        Debug.Log("Attempting to remove self from AppManager's widgets")
        self.clear_widgets()
        AppManager.manager.remove_widget(self)
        Debug.End()
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        KontrolRGB.DisplayDefaultColor()

    def GoToPrevious(self, *args):
        """
            Function to go back to `ProfileCreation_Step1.py`
        """
        AppManager.manager.add_widget(ProfileCreation_Step1(name="ProfileCreation_Step1"))
        AppManager.manager.transition.direction = "right"
        AppManager.manager.current = "ProfileCreation_Step1"
# ------------------------------------------------------------------------
    def GoToNext(self, *args):
        """
            Function to go back to `ProfileCreation_Step3.py`
        """
        AppManager.manager.add_widget(ProfileCreation_Step3(name="ProfileCreation_Step3"))
        AppManager.manager.transition.direction = "left"
        AppManager.manager.current = "ProfileCreation_Step3"
# ------------------------------------------------------------------------
    def PrimaryPressed(self, *args):
        """
            Function called whenever one of the primary colors is pressed.
            Updates the selected theme.
            Sets the Temporary theme to the pressed one.
            Highlights the selected button.
        """
        Debug.Start("PrimaryPressed")
        Temporary = GetTemporary()
        for button in self.PrimaryColorsList:
            if(button.state == "normal"):
                button.line_color = (0,0,0,0)
                button.icon = "circle"
            else:
                button.line_color = button.icon_color
                button.icon = "checkbox-marked-circle"
                MDApp.get_running_app().theme_cls.primary_palette = button.text

                Temporary[structureEnum.Theme.value][ProfileThemeEnum.Primary.value] = button.text
                Debug.Log(f"Primary color is now: {button.text}")
        SetTemporary(Temporary)
        Debug.End()
# ------------------------------------------------------------------------
    def AccentPressed(self, *args):
        """
            Function called whenever one of the accent colors is pressed.
            Updates the selected theme.
            Sets the Temporary theme to the pressed one.
            Highlights the selected button.
        """
        Debug.Start("AccentPressed")
        Temporary = GetTemporary()
        for button in self.AccentColorsList:
            if(button.state == "normal"):
                button.line_color = (0,0,0,0)
                button.icon = "circle"
            else:
                button.line_color = button.icon_color
                button.icon = "checkbox-marked-circle"
                MDApp.get_running_app().theme_cls.accent_palette = button.text

                Temporary[structureEnum.Theme.value][ProfileThemeEnum.Accent.value] = button.text
                Debug.Log(f"Accent color is now: {button.text}")

        Debug.Log("Updating RGB LEDs")
        KontrolRGB.DisplayDefaultColor()
        SetTemporary(Temporary)
        Debug.End()
# ------------------------------------------------------------------------
    def ThemePressed(self, *args):
        """
            Function called whenever one of the theme colors is pressed.
            Updates the selected theme.
            Sets the Temporary theme to the pressed one.
            Highlights the selected button.
        """
        Debug.Start("ThemePressed")
        Temporary = GetTemporary()
        for button in self.ThemeColorsList:
            if(button.state == "normal"):
                button.line_color = (0,0,0,0)
                button.icon = "circle"
            else:
                button.line_color = button.icon_color
                button.icon = "checkbox-marked-circle"

                Temporary[structureEnum.Theme.value][ProfileThemeEnum.Style.value] = button.text
                MDApp.get_running_app().theme_cls.theme_style = button.text
                Debug.Log(f"Theme style color is now: {button.text}")

                if(button.text == "Dark"):
                    CardBackground = (0.12,0.12,0.12,1)
                    TextColor = (1,1,1,1)
                    from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
                    path = os.getcwd()
                    self.background.source = AppendPath(path, "/Libraries/Backgrounds/ProfileCreation/DarkFlip.png")
                else:
                    CardBackground = (1,1,1,1)
                    TextColor = (0.12,0.12,0.12,1)
                    from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
                    path = os.getcwd()
                    self.background.source = AppendPath(path, "/Libraries/Backgrounds/ProfileCreation/LightFlip.png")

                self.PageTitle.theme_text_color = "Custom"
                self.ThemeStyleLabel.theme_text_color = "Custom"
                self.AccentLabel.theme_text_color = "Custom"
                self.PrimaryLabel.theme_text_color = "Custom"
                self.Next.theme_text_color = "Custom"
                self.Next.theme_icon_color = "Custom"
                self.Previous.theme_icon_color = "Custom"
                self.Previous.theme_text_color = "Custom"
                self.PageTitle.text_color = TextColor
                self.Card.md_bg_color = CardBackground
                self.Card.bg_color = CardBackground
                self.Card.color = CardBackground
                self.ThemeStyleLabel.text_color = TextColor
                self.AccentLabel.text_color = TextColor
                self.PrimaryLabel.text_color = TextColor
                self.Next.icon_color = TextColor
                self.Previous.icon_color = TextColor
        
        SetTemporary(Temporary)
        Debug.End()
#====================================================================#
class ProfileCreation_Step3(Screen):
    #region   --------------------------- MEMBERS
    progress = 0
    """The animation's progress from 0 to 1"""
    animation = Animation()
    """Animation object"""
    elevation = 0
    softness = 0
    selectedProfilePic = ""

    usernameError:bool = False
    passwordError:bool = False
    biographyError:bool = False
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("ProfileCreation_Step3")
        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
            Builds the ProfileCreation_Step3 entirely
            The username and password screen consists of 2 textfields
            as well as 2 labels and a confirm button.
        """
        Debug.Start("ProfileCreation_Step3: on_pre_enter")
        self.padding = 25
        self.spacing = 25

        KontrolRGB.ApploadingAnimation()

        #region ---- Background
        import os
        from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
        from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
        path = os.getcwd()

        background = GetBackgroundImage(AppendPath(path, "/Libraries/Backgrounds/ProfileCreation/Dark.png"),
                                        AppendPath(path, "/Libraries/Backgrounds/ProfileCreation/Light.png"))
        #endregion

        Temporary = GetTemporary()

        Debug.Log("Setting Temporary profile's themes to MDApp's current")

        Debug.Log("Creating Layouts")
        self.MainLayout = MDBoxLayout(spacing=10, padding=("20sp","20sp","20sp","20sp"), orientation="vertical")
        self.MiddleLayout = MDBoxLayout(spacing=10, padding=("20sp","20sp","20sp","20sp"), orientation="horizontal")
        self.TopLayout = MDBoxLayout(padding=("20sp","20sp","20sp","20sp"), size_hint_y = 0.25)

        # region ---- Card
        Debug.Log("Creating Card and Card layouts")
        self.LeftCard = MDCard(
                        elevation = Shadow.Elevation.default,
                        shadow_softness = Shadow.Smoothness.default,
                        radius=Rounding.default,
                        padding = 25,
                        orientation = "vertical"
                        )
        self.RightCard = MDCard(
                        elevation = Shadow.Elevation.default,
                        shadow_softness = Shadow.Smoothness.default,
                        radius=Rounding.default,
                        padding = 25,
                        orientation = "vertical"
                        )

        self.LeftCardTop = MDBoxLayout(spacing=5, padding=("10sp","10sp","10sp","10sp"), orientation="vertical")
        self.LeftCardBottom = MDBoxLayout(spacing=5, padding=("10sp","10sp","10sp","10sp"), orientation="horizontal")

        self.RightCardTop = MDBoxLayout(spacing=5, padding=("0sp","10sp","0sp","10sp"), orientation="vertical")
        self.RightCardTop.size_hint = (1, 0.25)
        self.RightCardBottom = MDBoxLayout(spacing=5, padding=("10sp","10sp","10sp","10sp"), orientation="horizontal")

        Debug.Log("Creating standard profile information widgets")
        self.UsernameTitle = MDLabel(text=_("Username") + ":")
        self.PasswordTitle = MDLabel(text=_("Password") + ":")
        self.BiographyTitle = MDLabel(text=_("Biography") + ":")
        self.Username  = MDTextField(text=Temporary[structureEnum.Generic.value][ProfileGenericEnum.Username.value])
        self.Password  = MDTextField(text=Temporary[structureEnum.Generic.value][ProfileGenericEnum.Password.value])
        self.Biography = MDTextField(text=Temporary[structureEnum.Generic.value][ProfileGenericEnum.Biography.value])
        self.Username.bind(text = self.UsernameTextChanged)
        self.Password.bind(text = self.PasswordTextChanged)
        self.Biography.bind(text = self.BiographyTextChanged)
        self.Username.hint_text = _("Username")
        self.Password.hint_text = _("Password")
        self.Biography.hint_text = _("Biography")

        # self.Biography.max_height = 3
        self.PasswordTitle.font_style = "H5"
        self.UsernameTitle.font_style = "H5"
        self.BiographyTitle.font_style = "H5"

        # endregion
        # region ---- Previous/Next
        Debug.Log("Creating Previous/Next buttons")
        self.Next = MDIconButton(text="chevron-right", icon="chevron-right")
        self.Next.icon_size = "75sp"
        self.Next.pos_hint={"center_x": 0.75, "center_y": 0.5}
        self.Next.on_release = self.GoToNext

        self.Previous = MDIconButton(text="chevron-left", icon="chevron-left")
        self.Previous.icon_size = "75sp"
        self.Previous.pos_hint={"center_x": 0.25, "center_y": 0.5}
        self.Previous.on_release = self.GoToPrevious

        # endregion

        # Page title
        self.PageTitle = MDLabel(text=_("Select profile information"),
                                 font_style = "H2",
                                 halign = "center")

        # Top layout widgets
        self.TopLayout.add_widget(self.Previous)
        self.TopLayout.add_widget(self.PageTitle)
        self.TopLayout.add_widget(self.Next)

        #region ---- SearchBar
        # self.MagnifyGlass = MDIconButton(icon = "magnify")
        self.SearchBar = MDTextField()
        self.SearchBar.hint_text = _("Search")
        self.SearchBar.bind(text=self.SearchIcons)
        self.SearchLayout = MDBoxLayout(spacing=10, padding=("0sp","0sp","10sp","0sp"), orientation="horizontal")
        # self.SearchLayout.add_widget(self.MagnifyGlass)
        self.SearchLayout.add_widget(self.SearchBar)
        self.RightCardTop.add_widget(self.SearchLayout)
        #endregion

        #region ---- Recycle view
        # Clock.schedule_once(self.create_layouts, 1)
        self.create_layouts()
        #endregion

        #region ---- Top Of Card
        self.LeftCard.add_widget(self.UsernameTitle)
        self.LeftCard.add_widget(self.Username)
        self.LeftCard.add_widget(self.PasswordTitle)
        self.LeftCard.add_widget(self.Password)
        self.LeftCard.add_widget(self.BiographyTitle)
        self.LeftCard.add_widget(self.Biography)
        #endregion

        #Checking currently saved username
        self.UsernameTextChanged()

        if(ProfileCreation_Screens.Mode == "Editing"):
            Debug.Log("EDITING SET TO TRUE, TEXT FIELDS SHOULD BE FILLED.")
            self.Username.text = Temporary[structureEnum.Generic.value][ProfileGenericEnum.Username.value]
            self.Password.text = Temporary[structureEnum.Generic.value][ProfileGenericEnum.Password.value]
            self.Biography.text = Temporary[structureEnum.Generic.value][ProfileGenericEnum.Biography.value]

            Debug.Log(f">>> Username -> {self.Username.text}")
            Debug.Log(f">>> Password -> {self.Password.text}")
            Debug.Log(f">>> Biography -> {self.Biography.text}")

            Debug.Log(f"Temporary -> {Temporary}")

        # Add widgets
        self.add_widget(background)
        self.RightCard.add_widget(self.RightCardTop)
        self.RightCard.add_widget(self.RightCardBottom)
        self.MiddleLayout.add_widget(self.LeftCard)
        self.MiddleLayout.add_widget(self.RightCard)

        self.MainLayout.add_widget(self.TopLayout)
        self.MainLayout.add_widget(self.MiddleLayout)
        self.add_widget(self.MainLayout)
        Debug.End()
        pass
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        KontrolRGB.DisplayDefaultColor()
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully left.
        """
        Debug.Start("on_leave")
        Debug.Log("Attempting to remove self from AppManager's widgets")
        self.clear_widgets()
        AppManager.manager.remove_widget(self)
        Debug.End()
# ------------------------------------------------------------------------
    def GoToPrevious(self, *args):
        """
            Function to go back to `ProfileCreation_Step1.py`
        """
        AppManager.manager.add_widget(ProfileCreation_Step2(name="ProfileCreation_Step2"))
        AppManager.manager.transition.direction = "right"
        AppManager.manager.current = "ProfileCreation_Step2"
# ------------------------------------------------------------------------
    def GoToNext(self, *args):
        """
            Function to go back to `ProfileCreation_Step3.py`
        """
        Debug.Start("GoToNext")

        Debug.Log("Checking if anything equals to errors")
        AppManager.manager.add_widget(ProfileCreation_Step4(name="ProfileCreation_Step4"))
        AppManager.manager.transition.direction = "left"
        AppManager.manager.current = "ProfileCreation_Step4"
        Debug.End()
# ------------------------------------------------------------------------
    def UpdateScreenForErrors(self, *args) -> bool:
        """
            UpdateScreenForErrors:
            ----------------------
            This function verifies if anything is giving out errors to
            update the view of the application until the errors are no
            longer there.

            Call this anytime you verify some information for the screen
            to visually update other components unrelated to the component
            giving out errors.
        """
        Debug.Start("UpdateScreenForErrors")

        if(self.Username.error or self.Password.error or self.Biography.error):
            Debug.Warn("Some errors were found. Updating Step3 visually.")
            self.Next.icon = "lock"
            self.Next.theme_icon_color = "Error"
            self.Next.disabled = True
        else:
            self.Next.icon = "chevron-right"
            self.Next.theme_icon_color = "Primary"
            self.Next.disabled = False

        Debug.End()
# ------------------------------------------------------------------------
    def LoadProfileIcons(searchWord:str = None):
        """
            Loads profile icons that respects the banned word and must contain the
            searchWord into the class's MDScrollview so that the user can choose a 
            KivyMD icon for their profile.
        """
# ------------------------------------------------------------------------
    def create_layouts(self,*args):
        Debug.Start("create_layouts")
        self.create_recycle_view()
        Debug.End()
# ------------------------------------------------------------------------
    def IconSelected(self, *args):
        """
            IconSelected:
            -------------
            This function is a callback function executed when a new
            icon is selected to use for the profile creation.
        """
        Debug.Start("IconSelected")
        Temporary = GetTemporary()
        Temporary[structureEnum.Generic.value][ProfileGenericEnum.IconPath.value] = args[0]
        Debug.Log(f"Profile icon is now: {args[0]}")
        self.SearchIcons()
        SetTemporary(Temporary)
        Debug.End()
# ------------------------------------------------------------------------
    def create_recycle_view(self):
        Debug.Log("Creating recycle box layout")
        self.RecyleBoxLayout = RecycleGridLayout(default_size=(None,56),
                                                default_size_hint=(1, None),
                                                size_hint=(1, None),
                                                orientation='lr-tb')
        self.RecyleBoxLayout.cols = 5
        # self.RecyleBoxLayout.orientation
        self.RecyleBoxLayout.bind(minimum_height=self.RecyleBoxLayout.setter("height"))

        self.recycleView = RecycleView()
        self.recycleView.add_widget(self.RecyleBoxLayout)
        self.recycleView.viewclass = MDIconButton
        self.RightCardBottom.add_widget(self.recycleView)
        self.SearchIcons()
# ------------------------------------------------------------------------
    def SearchIcons(self, *args):
        """
            SearchIcons:
            ------------
            This function is a callback function called when the search
            textbox changes or is confirmed. Doing this will rebuild
            the recycleview's displayed icons and only keep the ones
            which contains what is inside of the searchbar.
        """
        Debug.Start("SearchIcons")
        Temporary = GetTemporary()
        icon:str = ""
        style = MDApp.get_running_app().theme_cls.theme_style

        Debug.Log(f"style = {style}")
        if(style == "Light"):
            color = (0,0,0,1)
        else:
            color = (1,1,1,1)

        Debug.Log("Clearing recycle view.")
        if(len(self.SearchBar.text) > 0):
            self.recycleView.data = [{'theme_icon_color' : "Custom",
                                      "icon_color":color,
                                      'icon': str(icon),
                                      'on_release':(lambda x: lambda: self.IconSelected(str(x)))(icon),
                                      'icon_size':50}
                                      for icon in ProfileIcons if self.SearchBar.text in str(icon) and not str(icon) in Temporary[structureEnum.Generic.value][ProfileGenericEnum.IconPath.value]]
        else:
            self.recycleView.data = [{'theme_icon_color' : "Custom",
                                      "icon_color":color,
                                      'icon': str(icon),
                                      'on_release':(lambda x: lambda: self.IconSelected(str(x)))(icon),
                                      'icon_size':50}
                                      for icon in ProfileIcons if not str(icon) in Temporary[structureEnum.Generic.value][ProfileGenericEnum.IconPath.value]]

        # Add the selected icon first in the list:
        self.recycleView.data.insert(0,
                                     {'theme_icon_color' : "Custom",
                                      "icon_color":get_color_from_hex(colors[Temporary[structureEnum.Theme.value][ProfileThemeEnum.Primary.value]]["500"]),
                                      'icon': str(Temporary[structureEnum.Generic.value][ProfileGenericEnum.IconPath.value]), 
                                      'icon_size':50})
        MDIconButton.theme_icon_color
        Debug.End()
# ------------------------------------------------------------------------
    def UsernameTextChanged(self, *args):
        """
            UsernameTextChanged:
            --------------------
            Callback function executed when the username text field
            changes. This compares the new username with the
            :ref: CheckUsername function.
        """
        Debug.Start("UsernameTextChanged")
        Temporary = GetTemporary()

        if(ProfileCreation_Screens.Mode == "Editing"):
            error = CheckUsername(self.Username.text, byPassName=Temporary[structureEnum.Generic.value][ProfileGenericEnum.Username.value])
        else:
            error = CheckUsername(self.Username.text)
        Debug.Log(error)

        if(not error):
            Debug.Log(self.Username.error)
            if(self.usernameError == True):
                Debug.Log("Was previously error, updating...")
                self.usernameError = False
                self.Username.error = False
                self.UpdateScreenForErrors()
                self.Username.hint_text = _("Username")
                KontrolRGB.DisplayDefaultColor()

            Temporary[structureEnum.Generic.value][ProfileGenericEnum.Username.value] = self.Username.text
        else:
            if(self.usernameError == False):
                Debug.Log("Was not previously in error, updating")
                self.Username.error = True
                self.usernameError = True
                self.UpdateScreenForErrors()
                KontrolRGB.DisplayUserError()

            self.Username.hint_text = _(error)
        SetTemporary(Temporary)
        Debug.End()
# ------------------------------------------------------------------------
    def PasswordTextChanged(self, *args):
        """
            PasswordTextChanged:
            --------------------
            Callback function executed when the password MDtextfield
            changes. This compares the new password with the
            :ref: CheckPassword function.
        """
        Temporary = GetTemporary()
        error = CheckPassword(self.Password.text)

        if(error):
            if(self.passwordError == False):
                self.passwordError = True
                self.Password.error = True
                self.UpdateScreenForErrors()
                KontrolRGB.DisplayUserError()
            self.Password.hint_text = _(error)
        else:
            if(self.passwordError == True):
                self.passwordError = False
                self.Password.error = False
                self.UpdateScreenForErrors()
                self.Password.hint_text = _("Password")
                KontrolRGB.DisplayDefaultColor()
            Temporary[structureEnum.Generic.value][ProfileGenericEnum.Password.value] = self.Password.text
        SetTemporary(Temporary)
# ------------------------------------------------------------------------
    def BiographyTextChanged(self, *args):
        """
            BiographyTextChanged:
            --------------------
            Callback function executed when the biography MDtextfield
            changes.This compares the new username with the
            :ref: CheckBiography function.
        """
        Temporary = GetTemporary()
        error = CheckBiography(self.Biography.text)

        if(error):
            if(self.biographyError == False):
                self.biographyError = True
                self.Biography.error = True
                self.UpdateScreenForErrors()
                KontrolRGB.DisplayUserError()
            self.Biography.hint_text = _(error)
        else:
            if(self.biographyError == True):
                self.biographyError = False
                self.Biography.error = False
                self.UpdateScreenForErrors()
                self.Biography.hint_text = _("Biography")
                KontrolRGB.DisplayDefaultColor()

            Temporary[structureEnum.Generic.value][ProfileGenericEnum.Biography.value] = self.Biography.text
        SetTemporary(Temporary)
#====================================================================#
class ProfileCreation_Step4(Screen):
    #region   --------------------------- MEMBERS
    progress = 0
    """The animation's progress from 0 to 1"""
    animation = Animation()
    """Animation object"""
    elevation = 0
    softness = 0
    selectedProfilePic = ""
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("ProfileCreation_Step4", DontDebug=True)
        Debug.End(ContinueDebug=True)
        #endregion
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        KontrolRGB.DisplayDefaultColor()
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
            Builds the ProfileCreation_Step4 entirely
        """
        Debug.Start("ProfileCreation_Step4 -> on_pre_enter")
        self.padding = 25
        self.spacing = 25

        #region ---- Background
        import os
        from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
        from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
        path = os.getcwd()

        background = GetBackgroundImage(AppendPath(path, "/Libraries/Backgrounds/ProfileCreation/DarkFlip.png"),
                                        AppendPath(path, "/Libraries/Backgrounds/ProfileCreation/LightFlip.png"))
        #endregion

        CreateScreenBase(self, _("Confirm your profile"), "Last")

        #region ---- RecycleView
        Debug.Log("Creating recycle box layout")
        self.RecyleBoxLayout = RecycleBoxLayout(default_size=(None,56),
                                                default_size_hint=(1, None),
                                                size_hint=(1, None),
                                                orientation='vertical')
        self.RecyleBoxLayout.bind(minimum_height=self.RecyleBoxLayout.setter("height"))

        self.recycleView = RecycleView()
        self.recycleView.add_widget(self.RecyleBoxLayout)
        self.recycleView.viewclass = MDLabel
        self.Card.add_widget(self.recycleView)
        self._FillRecycleView()
        #endregion
        self.add_widget(background)
        self.MainLayout.add_widget(self.TopLayout)
        self.MainLayout.add_widget(self.Card)
        self.add_widget(self.MainLayout)
        Debug.End()
        pass
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully left.
        """
        Debug.Start("on_leave")
        Debug.Log("Attempting to remove self from AppManager's widgets")
        self.clear_widgets()
        AppManager.manager.remove_widget(self)
        Debug.End()
# ------------------------------------------------------------------------
    def GoToPrevious(self, *args):
        """
            Function to go back to `ProfileCreation_Step3.py`
        """
        AppManager.manager.add_widget(ProfileCreation_Step3(name="ProfileCreation_Step3"))
        AppManager.manager.transition.direction = "right"
        AppManager.manager.current = "ProfileCreation_Step3"
# ------------------------------------------------------------------------
    def ConfirmProfile(self, *args):
        """
            Function that creates the profile and calls Good exit from
            _screen.
        """
        Debug.Start("ConfirmProfile")
        Temporary = GetTemporary()
        Debug.Log("Creating profile")

        if(ProfileCreation_Screens.Mode == "Editing"):
            Debug.Warn("Deleting profile")
            ProfileHandler.Delete()

        ProfileHandler.CreateProfile(Temporary)

        if(ProfileCreation_Screens.Mode == "Editing"):
            Debug.Warn("Loading new profile")
            if(ProfileHandler.LoadProfile(ProfileHandler.rawJson) == FileIntegrity.Good):
                Debug.Log(">>> LOADING SUCCESS")
            else:
                Debug.Error("FAILED TO LOAD PROFILE.")
                Debug.Error(f"Tried to load: {ProfileHandler.rawJson}")

        ProfileCreation_Screens._GoodExit()
        Debug.End()
# ------------------------------------------------------------------------
    def _FillRecycleView(self, *args):
        """
            _FillRecycleView:
            ------------
            This function's purpose is to fill the screen's recycleViews
            with their respective data lists. This one fills the screen's
            recycle view with Labels consisting of the profile's data.
        """
        Debug.Start("_FillRecycleView")
        Temporary = GetTemporary()

        Debug.Log("Filling recycle view.")
        # self.recycleView.data = [{'font_style' : "Body1",
                                    # 'text' : (generic.value + ":    " + str(Temporary[structureEnum.Generic.value][generic]))}
                                    # for generic in Temporary[structureEnum.Generic.value]]

        Debug.Log("Creating profile datas")
        Generics = [{'font_style' : "Body1",
                        'text' : (_(generic) + ":    " + str(Temporary[structureEnum.Generic.value][generic]))}
                        for generic in Temporary[structureEnum.Generic.value]]

        Configs = [{'font_style' : "Body1",
                    'text' : (_(config) + ":    " + str(Temporary[structureEnum.ProfileConfig.value][config]))}
                        for config in Temporary[structureEnum.ProfileConfig.value]]

        Themes = [{'font_style' : "Body1",
                    'text' : (_(theme) + ":    " + str(Temporary[structureEnum.Theme.value][theme]))}
                        for theme in Temporary[structureEnum.Theme.value]]

        Debug.Log("Creating section titles")
        GenericTitle = [{'font_style' : "H4",
                        'text' : _("Generic")+":"}]

        ThemeTitle = [{'font_style' : "H4",
                        'text' : _("Theme")+":"}]

        ConfigsTitle = [{'font_style' : "H4",
                        'text' : _("Configuration")+":"}]

        Debug.Log("Building recycleView data")
        self.recycleView.data = GenericTitle
        self.recycleView.data.extend(Generics)
        self.recycleView.data.extend(ThemeTitle)
        self.recycleView.data.extend(Themes)
        self.recycleView.data.extend(ConfigsTitle)
        self.recycleView.data.extend(Configs)
        Debug.End()
# ------------------------------------------------------------------------

LoadingLog.End("ProfileCreation.py")