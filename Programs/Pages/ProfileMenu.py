#====================================================================#
# File Information
#====================================================================#

#====================================================================#
print("ProfileMenu.py")
#====================================================================#
# Imports
#====================================================================#
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.animation import Animation
# -------------------------------------------------------------------
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, CardTransition
# -------------------------------------------------------------------
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Shadow
from Libraries.BRS_Python_Libraries.BRS.GUI.Inputs.buttons import Get_RaisedButton,TextButton
from Libraries.BRS_Python_Libraries.BRS.GUI.Status.ValueDisplay import OutlineDial, LineGraph
from Libraries.BRS_Python_Libraries.BRS.GUI.Status.Indicators import SVGDisplay
from Libraries.BRS_Python_Libraries.BRS.GUI.Containers.cards import WidgetCard
from Libraries.BRS_Python_Libraries.BRS.Utilities.states import StatesColors,States
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from kivymd.uix.boxlayout import MDBoxLayout
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class ProfileMenu(Screen):
    progress = 0
    animation = Animation()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("ProfileMenu")

        self.padding = 25
        self.spacing = 25

        self.Layout = MDBoxLayout(spacing=25, padding=(0,50,0,0), orientation="vertical")

        self.Layout.TitleLayout = MDBoxLayout(orientation="horizontal")
        self.Layout.TitleLayout.size_hint_y = 0.25
        self.Layout.ProfilesLayout = MDBoxLayout(spacing = 10, padding = 0)
        self.Layout.ProfilesLayout.size_hint_y = 1

        # Creating the "Welcome" title shown at the top of the profile screen.
        self.Layout.TitleLayout.Title = MDLabel(text = "Welcome")
        self.Layout.TitleLayout.Title.font_style = "H1"
        self.Layout.TitleLayout.Title.halign = "center"
        self.Layout.TitleLayout.Title.opacity = 0
        self.Layout.TitleLayout.Title.size_hint = (1,1)

        # Create a horizontal box layout
        self.Layout.ProfilesLayout.profileBox = MDBoxLayout(orientation='horizontal', spacing=25, padding = (0,50,0,25), size_hint_x=None)
        self.Layout.ProfilesLayout.profileBox.bind(minimum_width = self.Layout.ProfilesLayout.profileBox.setter('width'))

        # Create 10 MDCards and add them to the box layout
        for i in range(50):
            card = WidgetCard(size = (300, 500), size_hint_x = None)
            self.Layout.ProfilesLayout.profileBox.add_widget(card)

        # Create the scroll view and add the box layout to it
        self.Layout.ProfilesLayout.scroll = MDScrollView(scroll_type=['bars','content'])
        self.Layout.ProfilesLayout.scroll.smooth_scroll_end = 10
        self.Layout.ProfilesLayout.scroll.add_widget(self.Layout.ProfilesLayout.profileBox)
        self.Layout.ProfilesLayout.add_widget(self.Layout.ProfilesLayout.scroll)

        self.Layout.TitleLayout.add_widget(self.Layout.TitleLayout.Title)
        self.Layout.add_widget(self.Layout.TitleLayout)
        self.Layout.add_widget(self.Layout.ProfilesLayout)
        self.add_widget(self.Layout)
        Debug.End()
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """ Load the JSONs available, and sets what profiles are available """
        # Load all the available files at the profile location.
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        print("on_enter")
        # Slowly make "Welcome" appear on screen
        self.animation.stop_all(self)
        self.animation = Animation(progress = 1, duration = 0.5)
        self.animation.bind(on_progress = self._Animating)
        self.animation.start(self)
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        print("on_pre_leave")
        # self.Layout.card.SetAttributes(elevation=0,shadowSoftness=0)
# ------------------------------------------------------------------------
    def _Animating(self, *args):
        self.Layout.TitleLayout.Title.opacity = self.progress

        if(self.progress == 1):
            # Lift the cards upwards
            self.Layout.ProfilesLayout.CardA.animated = True
            self.Layout.ProfilesLayout.CardB.animated = True
            self.Layout.ProfilesLayout.CardC.animated = True
            self.Layout.ProfilesLayout.CardA.SetAttributes(elevation=Shadow.Elevation.default, shadowSoftness=Shadow.Smoothness.default)
            self.Layout.ProfilesLayout.CardB.SetAttributes(elevation=Shadow.Elevation.default, shadowSoftness=Shadow.Smoothness.default)
            self.Layout.ProfilesLayout.CardC.SetAttributes(elevation=Shadow.Elevation.default, shadowSoftness=Shadow.Smoothness.default)
