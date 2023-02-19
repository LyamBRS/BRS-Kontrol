#====================================================================#
# File Information
#====================================================================#

#====================================================================#
print("ProfileCreation.py")
#====================================================================#
# Imports
#====================================================================#
import os
from kivy.animation import Animation
# -------------------------------------------------------------------
from kivymd.uix.button import MDRaisedButton,MDRectangleFlatButton,MDFillRoundFlatButton,MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, CardTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.icon_definitions import md_icons
# -------------------------------------------------------------------
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Rounding,Shadow
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import AppLanguage, _
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Programs.Local.FileHandler.Profiles import LoadedProfile,Temporary
# from Programs.Pages.ProfileMenu import ProfileMenu
# -------------------------------------------------------------------
from ..Local.FileHandler import Profiles
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineIconListItem,IconLeftWidget
#====================================================================#
# Functions
#====================================================================#
class IconListItem(OneLineIconListItem):
    icon = StringProperty()
    def __init__(self, **kwargs):
        super(IconListItem, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        Bruh = IconLeftWidget()
        # Bruh.icon = md_icons["cancel"]
        Bruh.theme_icon_color = "Hint"
        self.add_widget(Bruh)
    print("This is not doing anything")
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

        # Language selection layouts
        self.MainLayout = MDBoxLayout(spacing=10, padding=("20sp","20sp","20sp","20sp"), orientation="vertical")
        self.MiddleLayout = MDBoxLayout(spacing=10, padding=("20sp","20sp","20sp","20sp"), orientation="vertical")
        self.TopLayout = MDBoxLayout(padding=("20sp","20sp","20sp","20sp"), size_hint_y = 0.25)

        self.Card = MDCard(
                            elevation = Shadow.Elevation.default,
                            shadow_softness = Shadow.Smoothness.default,
                            radius=Rounding.default,
                            padding = 25,
                            orientation = "vertical"
                            )
        self.CardTop = MDBoxLayout(spacing=10, padding=("10sp","10sp","10sp","10sp"), orientation="vertical")
        self.CardBottom = MDBoxLayout(spacing=10, padding=("10sp","10sp","10sp","10sp"), orientation="horizontal")
        #region ---- Top Of Card
        self.HelloWorld = MDLabel(text=_("Hello World"), 
                                 font_style = "H2", 
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
        #region ---- Previous/Next
        self.Next = MDIconButton(text="chevron-right", icon="chevron-right")
        self.Next.icon_size = "75sp"
        self.Next.pos_hint={"center_x": 0.75, "center_y": 0.5}

        self.Previous = MDIconButton(text="close", icon="close")
        self.Previous.icon_size = "75sp"
        self.Previous.pos_hint={"center_x": 0.25, "center_y": 0.5}
        self.Previous.on_release = self.GoBack
        #endregion
        # Page title
        self.PageTitle = MDLabel(text=_("Select a language"), 
                                 font_style = "H2", 
                                 halign = "center")

        # Bottom layout widgets
        self.TopLayout.add_widget(self.Previous)
        self.TopLayout.add_widget(self.PageTitle)
        self.TopLayout.add_widget(self.Next)

        # Button on_release binding

        # Add widgets
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
        """
            Animate all the widgets into view once the screen is fully present.
        """
        print("ProfileCreation_Step1: on_enter")

        # Start Animation
        # self.animation.stop_all(self)
        # self.animation = Animation(progress = 1, duration = 0.5)
        # self.animation.bind(on_progress = self._Animating)
        # self.animation.start(self)
        pass
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully left.
        """
        print("ProfileCreation_Step1: on_leave")
        self.clear_widgets()
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            Function called before the screen is fully left. This gives
            us time to animate the screen leaving before destroying the
            objects and instances it created.
        """
        print("ProfileCreation_Step1: on_pre_leave")
# ------------------------------------------------------------------------
    def _Animating(self, *args):
        """
            Call back function called each time an animation tick happens.
            We use it to add/remove the shadow of cards when entering or
            leaving the application.
        """
        pass
# ------------------------------------------------------------------------
    def GoBack(self, *args):
        """
            Function to go back to `ProfileMenu.py`
        """
        AppManager.manager.transition.direction = "down"
        AppManager.manager.current = "ProfileMenu"
# ------------------------------------------------------------------------
    def SetNewLanguage(self, language:str):
        """
            Callback function of the dropdown allowing it to
            set a new language.
        """
        AppLanguage.LoadLanguage(language)

        # - Update the application's displayed text
        self.PageTitle.text = _(self.PageTitle.text)
        self.menu.dismiss()