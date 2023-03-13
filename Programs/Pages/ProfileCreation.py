#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from re import X
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("ProfileCreation.py")
#====================================================================#
# Imports
#====================================================================#
import os
import time
from kivy.animation import Animation
from kivy.properties import StringProperty
# -------------------------------------------------------------------
from kivymd.uix.button import MDRaisedButton,MDRectangleFlatButton,MDFillRoundFlatButton,MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard,MDSeparator
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, CardTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField,MDTextFieldRect
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.icon_definitions import md_icons
from kivymd.color_definitions import palette,colors
from kivymd.app import MDApp
from kivymd.uix.recycleview import MDRecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock
# -------------------------------------------------------------------
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Rounding,Shadow
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import AppLanguage, _
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Programs.Local.FileHandler.Profiles import LoadedProfile,Temporary
from kivymd.uix.scrollview import MDScrollView
from kivy.utils import get_color_from_hex
# -------------------------------------------------------------------
from ..Local.FileHandler import Profiles
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
class CustomOneLineIconListItem(OneLineIconListItem):
    print("CustomOneLineIconListItem")
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
    self.Next.on_release = self.GoToNext
    
    if(stepType == "Middle"):
        self.Previous = MDIconButton(text="chevron-left", icon="chevron-left")
        self.Previous.icon_size = "75sp"
        self.Previous.pos_hint={"center_x": 0.25, "center_y": 0.5}
        self.Previous.on_release = self.GoToPrevious

    if(stepType == "First"):
        self.Previous = MDIconButton(text="close", icon="close")
        self.Previous.icon_size = "75sp"
        self.Previous.pos_hint={"center_x": 0.25, "center_y": 0.5}
        self.Previous.on_release = self.GoBack
    # endregion

    # Page title
    Debug.Log(f"Creating page title: {title}")
    self.PageTitle = MDLabel(text=_(title),
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

        Debug.Log("Setting Temporary profile's language to AppLanguage.Current")
        Temporary["Generic"]["Language"] = AppLanguage.Current

        CreateScreenBase(self, "Select a language", "First")

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
    def on_leave(self, *args):
        """
            Function called when the screen is fully left.
        """
        print("ProfileCreation_Step1: on_leave")
        self.clear_widgets()
# ------------------------------------------------------------------------
    def GoBack(self, *args):
        """
            Function to go back to `ProfileMenu.py`
        """
        AppManager.manager.transition.direction = "down"
        AppManager.manager.current = "ProfileMenu"
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
        Temporary["Generic"]["Language"] = AppLanguage.Current
        language = Temporary["Generic"]["Language"]
        Debug.Warn(f"Temporary profile now uses: {language}")

        Debug.Log("Closing dropdown menu")
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

        Debug.Log("Setting Temporary profile's themes to MDApp's current")
        Temporary["Generic"]["Language"] = AppLanguage.Current

        CreateScreenBase(self, "Select a theme", "Middle")

        #region ---- Top Of Card
        self.ThemeStyleLayout = MDBoxLayout(spacing=0,  padding=("0sp","0sp","0sp","0sp"), orientation="horizontal")
        self.PrimaryLayout = MDBoxLayout(spacing=0,     padding=("0sp","0sp","0sp","0sp"), orientation="horizontal")
        self.AccentLayout = MDBoxLayout(spacing=0,      padding=("0sp","0sp","0sp","0sp"), orientation="horizontal")

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
            Temporary["Theme"]["Primary"] = Primary.text
            Primary.theme_icon_color = "Custom"
            Primary.icon_color = get_color_from_hex(colors[color]["500"])
            Primary.line_width = 1.5

            if color == MDApp.get_running_app().theme_cls.primary_palette:
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

            if color == MDApp.get_running_app().theme_cls.accent_palette:
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
        Light.theme_icon_color = "Custom"
        Dark.theme_icon_color = "Custom"
        Light.icon_color = (0.8,0.8,0.8,1)
        Dark.icon_color = (0,0,0,1)

        if MDApp.get_running_app().theme_cls.theme_style == "Light":
            Light.line_color = Light.icon_color
            Light.icon = "checkbox-marked-circle"

        if MDApp.get_running_app().theme_cls.theme_style == "Dark":
            Dark.line_color = Dark.icon_color
            Dark.icon = "checkbox-marked-circle"

        Light.on_press = self.ThemePressed
        Dark.on_press = self.ThemePressed
        self.ThemeColorsList.append(Light)
        self.ThemeColorsList.append(Dark)
        self.ThemeStyleLayout.add_widget(Light)
        self.ThemeStyleLayout.add_widget(Dark)
        #endregion


        # Add widgets
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
        Debug.End()
        pass
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully left.
        """
        print("ProfileCreation_Step2: on_leave")
        self.clear_widgets()
# ------------------------------------------------------------------------
    def GoToPrevious(self, *args):
        """
            Function to go back to `ProfileCreation_Step1.py`
        """
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
        for button in self.PrimaryColorsList:
            if(button.state == "normal"):
                button.line_color = (0,0,0,0)
                button.icon = "circle"
            else:
                button.line_color = button.icon_color
                button.icon = "checkbox-marked-circle"
                Temporary["Theme"]["Primary"] = button.text
                MDApp.get_running_app().theme_cls.primary_palette = button.text
                Debug.Log(f"Primary color is now: {button.text}")
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
        for button in self.AccentColorsList:
            if(button.state == "normal"):
                button.line_color = (0,0,0,0)
                button.icon = "circle"
            else:
                button.line_color = button.icon_color
                button.icon = "checkbox-marked-circle"
                Temporary["Theme"]["Accent"] = button.text
                MDApp.get_running_app().theme_cls.accent_palette = button.text
                Debug.Log(f"Accent color is now: {button.text}")
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
        for button in self.ThemeColorsList:
            if(button.state == "normal"):
                button.line_color = (0,0,0,0)
                button.icon = "circle"
            else:
                button.line_color = button.icon_color
                button.icon = "checkbox-marked-circle"
                Temporary["Theme"]["Style"] = button.text
                MDApp.get_running_app().theme_cls.theme_style = button.text
                Debug.Log(f"Theme style color is now: {button.text}")

                if(button.text == "Dark"):
                    CardBackground = (0.12,0.12,0.12,1)
                    TextColor = (1,1,1,1)
                else:
                    CardBackground = (1,1,1,1)
                    TextColor = (0.12,0.12,0.12,1)

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

        Debug.Log("Setting Temporary profile's themes to MDApp's current")
        # Temporary["Generic"]["Language"] = AppLanguage.Current

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

        self.RightCardTop = MDBoxLayout(spacing=5, padding=("10sp","10sp","10sp","10sp"), orientation="vertical")
        self.RightCardTop.size_hint = (1, 0.25)
        self.RightCardBottom = MDBoxLayout(spacing=5, padding=("10sp","10sp","10sp","10sp"), orientation="horizontal")

        Debug.Log("Creating standard profile information widgets")
        self.UsernameTitle = MDLabel(text=_("Username") + ":")
        self.PasswordTitle = MDLabel(text=_("Password") + ":")
        self.BiographyTitle = MDLabel(text=_("Short biography") + ":")
        self.Username = MDTextField(text=Temporary["Generic"]["Username"])
        self.Password = MDTextField(text=Temporary["Generic"]["Password"])
        self.Biography = MDTextField(text=Temporary["Generic"]["Biography"])
        self.Biography.max_height = 3
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
        self.MagnifyGlass = MDIconButton(icon = "magnify")
        self.SearchBar = MDTextField()
        self.SearchBar.hint_text = _("Search")
        self.SearchBar.bind(text=self.SearchIcons)
        self.SearchLayout = MDBoxLayout(spacing=10, padding=("20sp","0sp","20sp","0sp"), orientation="horizontal")
        self.SearchLayout.add_widget(self.MagnifyGlass)
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

        # Add widgets
        # self.LeftCard.add_widget(self.LeftCardTop)
        # self.LeftCard.add_widget(self.LeftCardBottom)
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
    def on_leave(self, *args):
        """
            Function called when the screen is fully left.
        """
        print("ProfileCreation_Step3: on_leave")
        self.clear_widgets()
# ------------------------------------------------------------------------
    def GoToPrevious(self, *args):
        """
            Function to go back to `ProfileCreation_Step1.py`
        """
        AppManager.manager.transition.direction = "right"
        AppManager.manager.current = "ProfileCreation_Step2"
# ------------------------------------------------------------------------
    def GoToNext(self, *args):
        """
            Function to go back to `ProfileCreation_Step3.py`
        """
        # AppManager.manager.add_widget(ProfileCreation_Step4(name="ProfileCreation_Step4"))
        # AppManager.manager.transition.direction = "left"
        # AppManager.manager.current = "ProfileCreation_Step4"
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
    def create_recycle_view(self):
        Debug.Log("Creating recycle box layout")
        self.RecyleBoxLayout = RecycleBoxLayout(default_size=(None,56),
                                                default_size_hint=(1, None),
                                                size_hint=(1, None),
                                                orientation='vertical')
        self.RecyleBoxLayout.bind(minimum_height=self.RecyleBoxLayout.setter("height"))

        self.recycleView = RecycleView()
        self.recycleView.add_widget(self.RecyleBoxLayout)
        self.recycleView.viewclass = 'Label'
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
        icon:str = ""

        Debug.Log("Clearing recycle view.")
        if(len(self.SearchBar.text) > 0):
            self.recycleView.data = [{'text': str(icon)} for icon in ProfileIcons if self.SearchBar.text in str(icon)]
        else:
            self.recycleView.data = [{'text': str(icon)} for icon in ProfileIcons]
        Debug.End()
LoadingLog.End("ProfileCreation.py")