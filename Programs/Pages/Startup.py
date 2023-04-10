#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from kivymd.app import MDApp
LoadingLog.Start("Startup.py")
#====================================================================#
# Imports
#====================================================================#
import os
from kivy.core.window import Window
from random import randint, random
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import FilesFinder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.graphics import Canvas, Color, Rectangle, PushMatrix, PopMatrix, Rotate
# -------------------------------------------------------------------
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, CardTransition,SlideTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDIconButton
# -------------------------------------------------------------------
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
# -------------------------------------------------------------------
from Programs.Local.FileHandler.Profiles import ProfileHandler,CheckIntegrity
from Programs.Local.FileHandler.Cache import Cache
# -------------------------------------------------------------------
from .ProfileLogin import ProfileLogin
from .ProfileCreation import ProfileCreation_Step1
from ..Local.FileHandler import Profiles
#====================================================================#
# Screen Functions
#====================================================================#
class Startup_Screens:
    """
        Startup_Screens:
        ================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`Startup`.

        Description:
        ------------
        This class holds the different types of callers of the startup
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
        Startup_Screens._exitClass = screenClass
        Startup_Screens._exitName  = screenName

        Startup_Screens._exitTransition = transition
        Startup_Screens._exitDuration = duration
        Startup_Screens._exitDirection = direction
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
        Startup_Screens._callerClass = screenClass
        Startup_Screens._callerName  = screenName

        Startup_Screens._callerTransition = transition
        Startup_Screens._callerDuration = duration
        Startup_Screens._callerDirection = direction
        return False

    def _Exit() -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        # Attempt to add the screen class as a widget of the AppManager
        Debug.Start("Startup -> _Exit()")
        try:
        # Check if exit class was specified
            if(Startup_Screens._exitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True
            if(Startup_Screens._exitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                Startup_Screens._exitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(Startup_Screens._exitClass(name=Startup_Screens._exitName))
        except:
            Debug.Error("Startup_Screens: _Exit() -> Failed in add_widget")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = Startup_Screens._exitTransition()
        AppManager.manager.transition.duration = Startup_Screens._exitDuration
        AppManager.manager.transition.direction = Startup_Screens._exitDirection

        # try:
        AppManager.manager.current = Startup_Screens._exitName
        # except:
            # Debug.Error("Startup_Screens: _Exit() -> AppManager.manager.current FAILED")
            # return True
        Debug.End()
        return False

    def Call() -> bool:
        """
            Attempt to go to the main screen that is being handled by this class.

            Returns:
                bool: `True`:  Something went wrong and the screen can't be loaded. `False`: Success
        """
        Debug.Start("Startup -> Call()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            if(Startup_Screens._callerClass == None):
                Debug.Error("No caller class specified.")
                Debug.End()
                return True
            if(Startup_Screens._callerName == None):
                Debug.Error("No caller name specified.")
                Debug.End()
                return True

            AppManager.manager.add_widget(Startup(name="Startup"))
        except:
            Debug.Error("Exception occured while handling Call()")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = Startup_Screens._callerTransition()
        AppManager.manager.transition.duration = Startup_Screens._callerDuration
        AppManager.manager.transition.direction = Startup_Screens._callerDirection

        try:
            AppManager.manager.current = "Startup"
            Debug.Log("Screen successfully changed")
        except:
            Debug.Error("Failed to add AppLoading as current screen.")
            Debug.End()
            return True
        Debug.End()
        return False
    #endregion
#====================================================================#
# Classes
#====================================================================#
class Startup(Screen):
    """
        Startup:
        ================
        Summary:
        --------
        This class is a screen class used to display a specific screen.
        Please use :ref:`Startup_Screens` to call this class.

        Description:
        ------------
        This class holds the standard `ScreenManager` classes used by screen
        classes to display widgets and unload them or perform various screen
        specific actions.

        This `Startup` screen class is used to display Kontrol's startup animation
        which is displayed each time the application is started. It also loads
        the cached JSON data that was saved during the previous use of the application.

        Methods:
        ------------
        - :ref:`on_pre_enter`: Builds the widgets to display on screen
        - :ref:`on_enter`: Called once the screen is fully displayed
        - :ref:`on_pre_leave`: Called before the screen is left
        - :ref:`on_leave`: Last function called by this screen before dying. Unloads all widgets
    """
    #region   --------------------------- MEMBERS
    animationStep:int = 0
    """
        Holds which step we are at in the startup animation.
        0: Nothing shown
        1: B fades in and falls in place
        2: R fades in and falls in place
        3: S fades in and falls in place
        4: S rotates 90 degrees and boops BR out of view and fades them out
    """

    animationB = Animation()
    animationR = Animation()
    animationS = Animation()
    animationKontrol = Animation()

    letterFallDuration = 0.5
    letterFallAfter = 0.5
    letterYStart = 0.75
    letterTransition = "in_out_back"

    Step1Called:bool = False
    Step2Called:bool = False
    Step3Called:bool = False
    Step4Called:bool = False
    Step5Called:bool = False
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("ProfileMenu")
        Debug.End()
    #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
            on_pre_enter:
            =============
            Function which "builds" the :ref:`Startup` screen.
            This function is called before the screen is actually shown and
            loads all the widgets that will be displayed before :ref:`on_enter` is called.

            Screen specific actions:
            ------------------------
            The :ref:`Startup` is solely a short animation, nothing more, nothing less.
        """
        Debug.Start("Startup.py: on_pre_enter")
        self.padding = 25
        self.spacing = 25

        #region ---- Background
        from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
        from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
        path = os.getcwd()

        background = GetBackgroundImage(AppendPath(path, "/Libraries/Backgrounds/Startup/Dark.png"),
                                        AppendPath(path, "/Libraries/Backgrounds/Startup/Light.png"))
        #endregion

        #region ---- Main Layout
        self.Layout = MDFloatLayout()
        #endregion

        #region ---- B R S & Kontrol images
        icon_size = Window.width / 3
        icon_size = str(icon_size) + "sp"

        if(MDApp.get_running_app().theme_cls.theme_style == "Dark"):
            self.B = MDIconButton(icon="Libraries/Icons/Logo/White_BRS_B.png", font_style='Icon', font_size = "100sp", halign = "center", disabled = True, opacity=0)
            self.R = MDIconButton(icon="Libraries/Icons/Logo/White_BRS_R.png", font_style='Icon', font_size = "100sp", halign = "center", disabled = True, opacity=0)
            self.S = MDIconButton(icon="Libraries/Icons/Logo/White_BRS_S.png", font_style='Icon', font_size = "100sp", halign = "center", disabled = True, opacity=0)
        else:
            self.B = MDIconButton(icon="Libraries/Icons/Logo/Black_BRS_B.png", font_style='Icon', font_size = "100sp", halign = "center", disabled = True, opacity=0)
            self.R = MDIconButton(icon="Libraries/Icons/Logo/Black_BRS_R.png", font_style='Icon', font_size = "100sp", halign = "center", disabled = True, opacity=0)
            self.S = MDIconButton(icon="Libraries/Icons/Logo/Black_BRS_S.png", font_style='Icon', font_size = "100sp", halign = "center", disabled = True, opacity=0)

        self.B.icon_size = icon_size
        self.R.icon_size = icon_size
        self.S.icon_size = icon_size

        self.KontrolText = MDLabel(text=_("BRS Kontrol"), opacity=0, halign = "center")
        self.KontrolText.font_style = "H1"
        #endregion

        #region ---- Initial status of Images
        # Set the images as they are prior to the startup
        self.B.pos_hint={'center_x': 0.17, 'center_y':self.letterYStart}
        self.R.pos_hint={'center_x': 0.5,  'center_y':self.letterYStart}
        self.S.pos_hint={'center_x': 0.83, 'center_y':self.letterYStart}
        self.KontrolText.pos_hint={'center_x': 0.5, 'center_y':0}
        #endregion

        #region ---- add_widgets
        self.add_widget(background)
        self.Layout.add_widget(self.B)
        self.Layout.add_widget(self.R)
        self.Layout.add_widget(self.S)
        self.Layout.add_widget(self.KontrolText)
        self.add_widget(self.Layout)
        #endregion

        self.Step1Called = False
        self.Step2Called = False
        self.Step3Called = False
        self.Step4Called = False
        self.Step5Called = False
        Debug.End()
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            on_enter:
            =============
            Function called once the screen is fully loaded into view.

            Screen specific actions:
            ------------------------
            Starts the BRS logo's startup screen.
        """
        Debug.Start("Startup.py: on_enter")
        # First animation of letters
        self.animationB.stop_all(self.B)
        self.animationR.stop_all(self.R)
        self.animationS.stop_all(self.S)

        self.animationB = Animation(opacity=-1, duration=1, t="out_elastic")
        self.animationB.bind(on_progress = self._animationStep0)
        self.animationB.start(self.B)
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
        Debug.Start("Startup.py: on_pre_leave")
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
        Debug.Start("Startup.py: on_leave")
        Debug.Log("Attempting to remove self from AppManager's widgets")
        self.clear_widgets()
        AppManager.manager.remove_widget(self)
        Debug.End()
# ------------------------------------------------------------------------
    def _animationStep0(self, *args):
        if(args[2] > 0.9 and self.Step1Called == False):
            print("CALLING STEP 1")
            self.Step1Called = True
            self.animationB.stop_all(self.B)
            self.animationB = Animation(pos_hint={'center_x': 0.17, 'center_y':0.5}, opacity=1, duration=self.letterFallDuration, t=self.letterTransition)
            self.animationB.bind(on_progress = self._animationStep1)
            self.animationB.start(self.B)
# ------------------------------------------------------------------------
    def _animationStep1(self, *args):
        if(args[2] > self.letterFallAfter and self.Step2Called == False):
            print("CALLING STEP 2")
            self.Step2Called = True
            self.animationR = Animation(pos_hint={'center_x': 0.5, 'center_y':0.5}, opacity=1, duration=self.letterFallDuration, t=self.letterTransition)
            self.animationR.bind(on_progress = self._animationStep2)
            self.animationR.start(self.R)
# ------------------------------------------------------------------------
    def _animationStep2(self, *args):
        if(args[2] > self.letterFallAfter and self.Step3Called == False):
            print("CALLING STEP 3")
            self.Step3Called = True
            self.animationS = Animation(pos_hint={'center_x': 0.83, 'center_y':0.5}, opacity=1, duration=self.letterFallDuration, t=self.letterTransition)
            self.animationS.bind(on_progress = self._animationStep3)
            self.animationS.start(self.S)
# ------------------------------------------------------------------------
    def _animationStep3(self, *args):
        if(args[2] > 0.95 and self.Step4Called == False):
            print("CALLING STEP 4")
            self.Step4Called = True

            self.animationB = Animation(pos_hint={'center_x': -0.5, 'center_y':0.5}, opacity=0, duration=self.letterFallDuration, t=self.letterTransition)
            self.animationS = Animation(pos_hint={'center_x': 0.5, 'center_y':0.5}, opacity=1, duration=self.letterFallDuration, t=self.letterTransition)
            self.animationR = Animation(pos_hint={'center_x': -0.17, 'center_y':0.5}, opacity=0, duration=self.letterFallDuration, t=self.letterTransition)

            self.animationB.bind(on_progress = self._EmptyBind)
            self.animationR.bind(on_progress = self._EmptyBind)
            self.animationS.bind(on_progress = self._animationStep4)
            self.animationB.start(self.B)
            self.animationR.start(self.R)
            self.animationS.start(self.S)
# ------------------------------------------------------------------------
    def _animationStep4(self, *args):
        if(args[2] > 0.95 and self.Step5Called == False):
            print("CALLING STEP 5")
            self.Step5Called = True
            self.animationS = Animation(pos_hint={'center_x': 0.5, 'center_y':0.5}, opacity=2, duration=self.letterFallDuration, t="in_out_expo")
            self.animationKontrol = Animation(pos_hint={'center_x': 0.5, 'center_y':0.15}, opacity=1, duration=self.letterFallDuration, t=self.letterTransition)
            self.animationS.bind(on_progress = self._animationStep5)
            self.animationS.start(self.S)
            self.animationKontrol.start(self.KontrolText)
            pass
# ------------------------------------------------------------------------
    def _animationStep5(self, *args):
        wanted = (self.S.opacity - 1) * 90
        current = self.count
        difference = wanted-current
        self.count = self.count + difference

        with self.S.canvas.before:
            PushMatrix()
            Rotate(origin=self.S.center, angle=difference)

        with self.S.canvas.after:
            PopMatrix()

        if(args[2] == 1):
            print("=====================================")
            print("------------APP  STARTING------------")
            print("=====================================")
            Startup_Screens._Exit()
            pass
# ------------------------------------------------------------------------
    count = 0
    def _EmptyBind(self, *args):
        # print(self.count)
        pass
LoadingLog.End("ProfileMenu.py")