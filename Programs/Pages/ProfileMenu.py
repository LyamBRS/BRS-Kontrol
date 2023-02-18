#====================================================================#
# File Information
#====================================================================#

#====================================================================#
print("ProfileMenu.py")
#====================================================================#
# Imports
#====================================================================#
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
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, CardTransition
from kivymd.uix.boxlayout import MDBoxLayout
# -------------------------------------------------------------------
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Shadow
from Libraries.BRS_Python_Libraries.BRS.GUI.Inputs.buttons import Get_RaisedButton,TextButton
from Libraries.BRS_Python_Libraries.BRS.GUI.Status.ValueDisplay import OutlineDial, LineGraph
from Libraries.BRS_Python_Libraries.BRS.GUI.Status.Indicators import SVGDisplay
from Libraries.BRS_Python_Libraries.BRS.GUI.Containers.cards import WidgetCard,ProfileCard,CreateCard
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Programs.Local.FileHandler.Profiles import LoadedProfile,CheckIntegrity
# -------------------------------------------------------------------
from .ProfileLogin import ProfileLogin
from ..Local.FileHandler import Profiles
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class ProfileMenu(Screen):
    #region   --------------------------- MEMBERS
    progress = 0
    """The animation's progress from 0 to 1"""
    animation = Animation()
    """Animation object"""
    Loaded:bool = False
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("ProfileMenu")

        # self.padding = 25
        # self.spacing = 25

        # self.Layout = MDBoxLayout(spacing=25, padding=(0,50,0,0), orientation="vertical")

        # self.Layout.TitleLayout = MDBoxLayout(orientation="horizontal")
        # self.Layout.TitleLayout.size_hint_y = 0.25
        # self.Layout.ProfilesLayout = MDBoxLayout(spacing = "10sp", padding = "0sp")
        # self.Layout.ProfilesLayout.size_hint_y = 1

        # # Creating the "Welcome" title shown at the top of the profile screen.
        # self.Layout.TitleLayout.Title = MDLabel(text = "Welcome")
        # self.Layout.TitleLayout.Title.font_style = "H1"
        # self.Layout.TitleLayout.Title.halign = "center"
        # self.Layout.TitleLayout.Title.opacity = 0
        # self.Layout.TitleLayout.Title.size_hint = (1,1)

        # # Create a horizontal box layout offset by half the screen to center the first profile in view.
        # windowWidth = str(Window.width/2) + "sp"
        # self.Layout.ProfilesLayout.profileBox = MDBoxLayout(orientation='horizontal', spacing="50sp", padding = (windowWidth,"100sp",windowWidth,"50sp"), size_hint_x=None)
        # self.Layout.ProfilesLayout.profileBox.bind(minimum_width = self.Layout.ProfilesLayout.profileBox.setter('width'))

        # # Create the scroll view and add the box layout to it
        # self.Layout.ProfilesLayout.scroll = MDScrollView(scroll_type=['bars','content'])
        # self.Layout.ProfilesLayout.scroll.smooth_scroll_end = 10

        # # Add widgets
        # self.Layout.ProfilesLayout.scroll.add_widget(self.Layout.ProfilesLayout.profileBox)
        # self.Layout.ProfilesLayout.add_widget(self.Layout.ProfilesLayout.scroll)
        # self.Layout.TitleLayout.add_widget(self.Layout.TitleLayout.Title)
        # self.Layout.add_widget(self.Layout.TitleLayout)
        # self.Layout.add_widget(self.Layout.ProfilesLayout)
        # self.add_widget(self.Layout)

        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
            Load the JSONs available, and create 1 profile card
            per available profiles.
        """
        Debug.Start("ProfileMenu.py: on_pre_enter")

        self.padding = 25
        self.spacing = 25

        self.Layout = MDBoxLayout(spacing=25, padding=(0,50,0,0), orientation="vertical")

        self.Layout.TitleLayout = MDBoxLayout(orientation="horizontal")
        self.Layout.TitleLayout.size_hint_y = 0.25
        self.Layout.ProfilesLayout = MDBoxLayout(spacing = "10sp", padding = "0sp")
        self.Layout.ProfilesLayout.size_hint_y = 1

        # Creating the "Welcome" title shown at the top of the profile screen.
        self.Layout.TitleLayout.Title = MDLabel(text = "Welcome")
        self.Layout.TitleLayout.Title.font_style = "H1"
        self.Layout.TitleLayout.Title.halign = "center"
        self.Layout.TitleLayout.Title.opacity = 0
        self.Layout.TitleLayout.Title.size_hint = (1,1)

        # Create a horizontal box layout offset by half the screen to center the first profile in view.
        windowWidth = str(Window.width/2) + "sp"
        self.Layout.ProfilesLayout.profileBox = MDBoxLayout(orientation='horizontal', spacing="50sp", padding = (windowWidth,"100sp",windowWidth,"50sp"), size_hint_x=None)
        self.Layout.ProfilesLayout.profileBox.bind(minimum_width = self.Layout.ProfilesLayout.profileBox.setter('width'))

        # Create the scroll view and add the box layout to it
        self.Layout.ProfilesLayout.scroll = MDScrollView(scroll_type=['bars','content'])
        self.Layout.ProfilesLayout.scroll.smooth_scroll_end = 10

        # Add widgets
        self.Layout.ProfilesLayout.scroll.add_widget(self.Layout.ProfilesLayout.profileBox)
        self.Layout.ProfilesLayout.add_widget(self.Layout.ProfilesLayout.scroll)
        self.Layout.TitleLayout.add_widget(self.Layout.TitleLayout.Title)
        self.Layout.add_widget(self.Layout.TitleLayout)
        self.Layout.add_widget(self.Layout.ProfilesLayout)
        self.add_widget(self.Layout)

        # Load all the available files at the profile location.
        path = os.getcwd()
        jsonPath = path + "/Local/Profiles"
        Profiles = FilesFinder(".json",path + "/Local/Profiles")

        # Add all available profiles as cards in the scrollview:
        for profile in Profiles.fileList:
            print(" ---- " + profile)
            card = ProfileCard(jsonPath, profile, CheckIntegrity, size = ("200sp","300sp"), size_hint_x = None)
            card.SetAttributes(elevation=0)
            card.PressedEnd = self.ProfilesClicked
            self.Layout.ProfilesLayout.profileBox.add_widget(card)

        # Add the create new profile card at the end of the list
        card = CreateCard(size = ("200sp","300sp"), size_hint_x = None)
        card.PressedEnd = self.ProfilesClicked
        self.Layout.ProfilesLayout.profileBox.add_widget(card)

        Debug.End()
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            Function called when the screen is fully entered in view.
            In this case, once the view is fully loaded, the cards
            will slowly elevate to the wanted value.
        """
        print("Menu: on_enter")
        # Slowly make "Welcome" appear on screen
        self.animation.stop_all(self)
        self.animation = Animation(progress = 1, duration = 0.5)
        self.animation.bind(on_progress = self._Animating)
        self.animation.start(self)
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            Function called before the screen is fully left. This gives
            us time to animate the screen leaving before destroying the
            objects and instances it created.
        """
        print("Menu: on_pre_leave")
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully out of view.
        """
        print("Menu: on_leave")
        self.clear_widgets()
# ------------------------------------------------------------------------
    def _Animating(self, *args):
        """
            Call back function called each time an animation tick happens.
            We use it to add/remove the shadow of cards when entering or
            leaving the application.
        """
        self.Layout.TitleLayout.Title.opacity = self.progress

        if(self.progress == 1 and not self.Loaded):
            # Lift the cards upwards
            for card in self.Layout.ProfilesLayout.profileBox.children:
                card.animated = True
                card.Elevation = Shadow.Elevation.default
            self.Loaded = True

        if(self.progress == 1 and self.Loaded):
            # Lift the cards upwards
            for card in self.Layout.ProfilesLayout.profileBox.children:
                card.Elevation = 0

        # Go to profile login screen
        if(self.progress == 0 and self.Loaded):
            AppManager.manager.add_widget(ProfileLogin(name="ProfileLogin"))
            AppManager.manager.transition.direction = "up"
            AppManager.manager.current = "ProfileLogin"
            self.Loaded = False
# ------------------------------------------------------------------------
    def ProfilesClicked(self, card:ProfileCard):
        """
            Called when one of the profile cards was clicked,
            and successfully executes if the profile clicked was usable.

            This will search through all the available profile cards and
            take the first pressed one. It will then put the wanted leaving
            variable to 1 in the animation.

            Loads the profile in Profiles.py for global access.
        """
        LoadedProfile.LoadProfile(card.json)

        #Slowly make welcome fade off
        self.animation.stop_all(self)
        self.animation = Animation(progress = 0, duration = 0.5)
        self.animation.bind(on_progress = self._Animating)
        self.animation.start(self)
        # AppManager.manager.add_widget(ProfileLogin(name="ProfileLogin"))
        # AppManager.manager.current = "ProfileLogin"
