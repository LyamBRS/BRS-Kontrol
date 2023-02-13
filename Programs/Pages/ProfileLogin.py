#====================================================================#
# File Information
#====================================================================#

#====================================================================#
print("ProfileLogin.py")
#====================================================================#
# Imports
#====================================================================#
from cgitb import text
import os
from random import randint, random
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import FilesFinder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.animation import Animation
# -------------------------------------------------------------------
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton,MDRectangleFlatButton,MDFillRoundFlatButton,MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, CardTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
# -------------------------------------------------------------------
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Shadow
from Libraries.BRS_Python_Libraries.BRS.GUI.Inputs.buttons import Get_RaisedButton,TextButton
from Libraries.BRS_Python_Libraries.BRS.GUI.Status.ValueDisplay import OutlineDial, LineGraph
from Libraries.BRS_Python_Libraries.BRS.GUI.Status.Indicators import SVGDisplay
from Libraries.BRS_Python_Libraries.BRS.GUI.Containers.cards import WidgetCard,ProfileCard
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Rounding,Shadow
from Libraries.BRS_Python_Libraries.BRS.Utilities.states import StatesColors,States
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Programs.Local.FileHandler.Profiles import LoadedProfile
# from Programs.Pages.ProfileMenu import ProfileMenu
# -------------------------------------------------------------------
from ..Local.FileHandler import Profiles
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class ProfileLogin(Screen):
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
        Debug.Start("ProfileLogin")
        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
            Sets all widgets to be animated.
        """
        self.padding = 25
        self.spacing = 25

        # Login card
        self.MainLayout = MDBoxLayout(spacing=10, padding=("300sp","20sp","300sp","20sp"), orientation="vertical")
        self.Card = MDCard(
                            elevation = Shadow.Elevation.default,
                            shadow_softness = Shadow.Smoothness.default,
                            radius=Rounding.default, padding = 25,
                            orientation = "vertical"
                            )
        self.UsernameTitle = MDLabel(text="Username:")
        self.PasswordTitle = MDLabel(text="Password:")
        self.Username = MDTextField(text=LoadedProfile.rawJson.jsonData["Generic"]["Username"])
        self.Password = MDTextField()
        self.PasswordTitle.font_style = "H5"
        self.UsernameTitle.font_style = "H5"

        # Page title
        self.LoginTitle = MDLabel(text="Login", font_style = "H1", halign = "center", size_hint_y = 0.25)

        # Button Layout
        self.ButtonLayout = MDBoxLayout(spacing=20)
        self.CancelLayout = MDFloatLayout()
        self.LoginLayout = MDFloatLayout()

        self.Login = MDIconButton(text="check", icon="check")
        self.Cancel = MDIconButton(text="close-circle", icon="close-circle")
        self.Login.icon_size = "100sp"
        self.Cancel.icon_size = "100sp"
        self.Login.pos_hint={"center_x": 0.5, "center_y": 0.5}
        self.Cancel.pos_hint={"center_x": 0.5, "center_y": 0.5}

        # Set back function
        self.Cancel.on_release = self.GoBack
        self.Login.on_release = self.LoginAttempt

        # Add widgets
        self.CancelLayout.add_widget(self.Cancel)
        self.LoginLayout.add_widget(self.Login)
        self.ButtonLayout.add_widget(self.LoginLayout)
        self.ButtonLayout.add_widget(self.CancelLayout)
        self.Card.add_widget(self.UsernameTitle)
        self.Card.add_widget(self.Username)
        self.Card.add_widget(self.PasswordTitle)
        self.Card.add_widget(self.Password)
        self.Card.add_widget(self.ButtonLayout)

        self.MainLayout.add_widget(self.LoginTitle)
        self.MainLayout.add_widget(self.Card)
        self.add_widget(self.MainLayout)
        print("Login: on_pre_enter")
        pass
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            Animate all the widgets into view once the screen is fully present.
        """
        print("Login: on_enter")


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
        print("Login: on_leave")
        self.clear_widgets()
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            Function called before the screen is fully left. This gives
            us time to animate the screen leaving before destroying the
            objects and instances it created.
        """
        print("Login: on_pre_leave")
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
    def LoginAttempt(self, *args):
        """
            Function called when attempting to log in with the specified
            password and username
        """
        username = LoadedProfile.rawJson.jsonData["Generic"]["Username"]
        password = LoadedProfile.rawJson.jsonData["Generic"]["Password"]

        if(username != self.Username.text):
            self.Username.error = True

        if(password != self.Password.text):
            self.Password.error = True