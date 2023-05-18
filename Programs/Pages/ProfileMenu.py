#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Libraries.BRS_Python_Libraries.BRS.Utilities.addons import Addons
from Programs.Local.Hardware.RGB import KontrolRGB
from Programs.Pages.Startup import Startup_Screens
LoadingLog.Start("ProfileMenu.py")
#====================================================================#
# Imports
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import FilesFinder
from kivy.core.window import Window
from kivy.animation import Animation
# -------------------------------------------------------------------
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, CardTransition, SlideTransition
from kivymd.uix.boxlayout import MDBoxLayout
# -------------------------------------------------------------------
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Shadow
from Libraries.BRS_Python_Libraries.BRS.GUI.Containers.cards import ProfileCard,CreateCard
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Programs.Local.FileHandler.Profiles import ProfileGenericEnum, ProfileHandler,CheckIntegrity, structureEnum
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
# -------------------------------------------------------------------
from .ProfileLogin import ProfileLogins_Screens
from .ProfileCreation import ProfileCreation_Screens
from ..Local.FileHandler.Profiles import Profiles, ProfileHandler
from ..Pages.DriverMenu import DriverMenu
#====================================================================#
# Functions
#====================================================================#
#====================================================================#
# Screen class
#====================================================================#
LoadingLog.Log("ProfileLogin_Screens")
class ProfileMenu_Screens:
    """
        ProfileMenu_Screens:
        ================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`ProfileMenu`.

        Description:
        ------------
        This class holds the function that calls ProfileMenu.

        Members:
        ------------
        This class contains the following screens:
    """
    #region ---- Members

    #endregion
    #region ---- Methods

    def Call(*args) -> bool:
        """
            Attempt to go to the main screen that is being handled by this class.

            Returns:
                bool: `True`:  Something went wrong and the screen can't be loaded. `False`: Success
        """
        Debug.Start("ProfileMenu -> Call")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            Debug.Log("Adding widget")
            AppManager.manager.add_widget(ProfileMenu(name="ProfileMenu"))
        except:
            Debug.Error("Exception occured while handling Call()")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition.duration = 0.5
        AppManager.manager.transition.direction = "down"

        # try:
        AppManager.manager.current = "ProfileMenu"
        ProfileHandler.UnLoadProfile()
        ProfileCreation_Screens.Mode = "Creation"
        # except:
            # Debug.Error("Failed to add ProfileLogin as current screen.")
            # Debug.End()
            # return True

        Debug.End()
        return False
    #endregion

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

        # Debug.Log("Setting variables depending on wrongDisplay member")
        if(Information.usingWrongDisplay):
            cardOffset = 100
            profileCardWidth = "200sp"
            profileCardheight = "300sp"
        else:
            cardOffset = 100
            profileCardWidth = "200sp"
            profileCardheight = "300sp"

        #region ---- Background
        import os
        from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
        from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
        path = os.getcwd()

        background = GetBackgroundImage(AppendPath(path, "/Libraries/Backgrounds/AppLoading/Dark.png"),
                                        AppendPath(path, "/Libraries/Backgrounds/AppLoading/Light.png"))
        #endregion

        self.Layout = MDBoxLayout(spacing=25, padding=(0,50,0,0), orientation="vertical")
        self.Layout.TitleLayout = MDBoxLayout(orientation="horizontal")
        self.Layout.ProfilesLayout = MDBoxLayout(spacing = "10sp", padding = "0sp")
        self.Layout.TitleLayout.Title = MDLabel(text = _("Welcome"))

        self.Layout.TitleLayout.size_hint_y = 0.25
        self.Layout.ProfilesLayout.size_hint_y = 1

        # Creating the "Welcome" title shown at the top of the profile screen.
        self.Layout.TitleLayout.Title.font_style = "H1"
        self.Layout.TitleLayout.Title.halign = "center"
        self.Layout.TitleLayout.Title.opacity = 0
        self.Layout.TitleLayout.Title.size_hint = (1,1)

        # Create a horizontal box layout offset by half the screen to center the first profile in view.
        windowWidth = (Window.width/2) - cardOffset
        self.Layout.ProfilesLayout.profileBox = MDBoxLayout(orientation='horizontal', spacing="50sp", padding = (windowWidth,"100sp",windowWidth,"50sp"), size_hint_x=None)
        self.Layout.ProfilesLayout.profileBox.bind(minimum_width = self.Layout.ProfilesLayout.profileBox.setter('width'))

        # Create the scroll view and add the box layout to it
        self.Layout.ProfilesLayout.scroll = MDScrollView(scroll_type=['bars','content'])
        self.Layout.ProfilesLayout.scroll.smooth_scroll_end = 10

        # Add widgets
        self.add_widget(background)
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
        Debug.Log("Creating profile cards...")
        for profile in Profiles.fileList:
            card = ProfileCard(jsonPath, profile, CheckIntegrity, size = (profileCardWidth, profileCardheight), size_hint_x = None)
            card.SetAttributes(elevation=0)
            card.PressedEnd = self.ProfilesClicked
            self.Layout.ProfilesLayout.profileBox.add_widget(card)
        Debug.Log("All profile cards created")

        # Add the create new profile card at the end of the list
        card = CreateCard(size = (profileCardWidth, profileCardheight), size_hint_x = None)
        card.PressedEnd = self.CreateProfileClicked
        card._MDCard.Title.text = _("Create")
        self.Layout.ProfilesLayout.profileBox.add_widget(card)

        Debug.Log("Clearing profiles from addons.")
        Addons.UnloadProfile(ProfileHandler.currentName)

        Debug.End()
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            Function called when the screen is fully entered in view.
            In this case, once the view is fully loaded, the cards
            will slowly elevate to the wanted value.
        """
        Debug.Start("ProfileMenu -> on_enter")
        # Slowly make "Welcome" appear on screen
        self.animation.stop_all(self)
        self.animation = Animation(progress = 1, duration = 0.5)
        self.animation.bind(on_progress = self._Animating)
        self.animation.start(self)

        KontrolRGB.DisplayDefaultColor()
        Debug.End()
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            Function called before the screen is fully left. This gives
            us time to animate the screen leaving before destroying the
            objects and instances it created.
        """
        Debug.Start("ProfileMenu -> on_pre_leave")
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
        self.clear_widgets()
        Debug.End()
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
            # AppManager.manager.add_widget(ProfileLogin(name="ProfileLogin"))
            # AppManager.manager.transition.direction = "up"
            # AppManager.manager.current = "ProfileLogin"
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
            Also sets the ProfileLogins_Screens.
        """
        Debug.Start("ProfilesClicked")
        # ProfileHandler.LoadProfile(card.json)
        # self.Layout.ProfilesLayout.profileBox.remove_widget(card)
        ProfileHandler.LoadProfile(card.json)
        #Slowly make welcome fade off
        self.animation.stop_all(self)
        self.animation = Animation(progress = 0, duration = 0.5)
        self.animation.bind(on_progress = self._Animating)
        self.animation.start(self)

        Debug.Log("Checking if profile has no password")
        if(len(card.json.jsonData[structureEnum.Generic.value][ProfileGenericEnum.Password.value]) == 0):
            Debug.Log("No password required")

        Debug.Log("Setting profileLoging exit and callers")
        ProfileLogins_Screens.SetCaller(ProfileMenu, "ProfileMenu")
        ProfileLogins_Screens.SetBadExiter(ProfileMenu, "ProfileMenu", direction="down")
        ProfileLogins_Screens.SetGoodExiter(DriverMenu, "DriverMenu")
        ProfileLogins_Screens.Call()

        Debug.End()
# ------------------------------------------------------------------------
    def CreateProfileClicked(self, card:ProfileCard):
        """
            Called when the card allowing the user to create a new profile
            was clicked.
        """

        #Slowly make welcome fade off
        self.animation.stop_all(self)
        self.animation = Animation(progress = 0, duration = 0.5)
        self.animation.bind(on_progress = self._Animating)
        self.animation.start(self)

        ProfileCreation_Screens.SetCaller(ProfileMenu, "ProfileMenu")
        ProfileCreation_Screens.SetBadExiter(ProfileMenu, "ProfileMenu", direction="down")
        ProfileCreation_Screens.SetGoodExiter(ProfileMenu, "ProfileMenu", direction="down")
        ProfileCreation_Screens.Call()
        # AppManager.manager.add_widget(ProfileCreation_Step1(name="ProfileCreation_Step1"))
        # AppManager.manager.transition.direction = "up"
        # AppManager.manager.current = "ProfileCreation_Step1"

LoadingLog.End("ProfileMenu.py")