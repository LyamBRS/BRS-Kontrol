#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("AppLoading.py")
#====================================================================#
# Imports
#====================================================================#
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, CardTransition, SlideTransition
from kivy.graphics import Color
from kivy.animation import Animation
from kivy.graphics import Canvas, Color, Rectangle, PushMatrix, PopMatrix, Rotate
# -------------------------------------------------------------------
from kivymd.color_definitions import colors
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDIconButton
# -------------------------------------------------------------------
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Shadow
from Libraries.BRS_Python_Libraries.BRS.GUI.Inputs.buttons import Get_RaisedButton,TextButton
from Libraries.BRS_Python_Libraries.BRS.GUI.Status.ValueDisplay import OutlineDial, LineGraph
from Libraries.BRS_Python_Libraries.BRS.GUI.Status.Indicators import SVGDisplay
from Libraries.BRS_Python_Libraries.BRS.GUI.Containers.cards import WidgetCard,ProfileCard,CreateCard
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
# -------------------------------------------------------------------
from ..Local.Loading.AppLoadingHandler import LoadApplication

#====================================================================#
# Screen Functions
#====================================================================#
class AppLoading_Screens:
    """
        AppLoading_Screens:
        ================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`AppLoading`.

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
        AppLoading_Screens._exitClass = screenClass
        AppLoading_Screens._exitName  = screenName

        AppLoading_Screens._exitTransition = transition
        AppLoading_Screens._exitDuration = duration
        AppLoading_Screens._exitDirection = direction
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
        AppLoading_Screens._callerClass = screenClass
        AppLoading_Screens._callerName  = screenName

        AppLoading_Screens._callerTransition = transition
        AppLoading_Screens._callerDuration = duration
        AppLoading_Screens._callerDirection = direction
        return False

    def _Exit() -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("AppLoading -> _Exit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(AppLoading_Screens._exitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(AppLoading_Screens._exitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                AppLoading_Screens._exitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(AppLoading_Screens._exitClass(name=AppLoading_Screens._exitName))
        except:
            Debug.Error("AppLoading -> Exception occured.")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = AppLoading_Screens._exitTransition()
        AppManager.manager.transition.duration = AppLoading_Screens._exitDuration
        AppManager.manager.transition.direction = AppLoading_Screens._exitDirection

        # try:
        AppManager.manager.current = AppLoading_Screens._exitName
        # except:
            # return True
        Debug.End()
        return False

    def Call() -> bool:
        """
            Attempt to go to the main screen that is being handled by this class.

            Returns:
                bool: `True`:  Something went wrong and the screen can't be loaded. `False`: Success
        """
        Debug.Start("AppLoading -> Call()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if caller class was specified
            Debug.Log("Checking caller class")
            if(AppLoading_Screens._callerClass == None):
                Debug.Error("No caller class specified.")
                Debug.End()
                return True
    
            Debug.Log("Checking caller name")
            if(AppLoading_Screens._callerName == None):
                Debug.Error("No caller name specified.")
                Debug.End()
                return True
    
            Debug.Log("Attempting to add widget")
            AppManager.manager.add_widget(AppLoading(name="AppLoading"))
        except:
            Debug.Error("Exception occured while handling Call()")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = AppLoading_Screens._callerTransition()
        AppManager.manager.transition.duration = AppLoading_Screens._callerDuration
        AppManager.manager.transition.direction = AppLoading_Screens._callerDirection

        # try:
        AppManager.manager.current = "AppLoading"
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
class AppLoading(Screen):
    """
        AppLoading:
        ================
        Summary:
        --------
        This class is a screen class used to display a specific screen.
        Please use :ref:`AppLoading_Screens` to call this class.

        Description:
        ------------
        This class holds the loading application's screen.
        It also loads the application while displaying each steps of the loading.

        Methods:
        ------------
        - :ref:`on_pre_enter`: Builds the widgets to display on screen
        - :ref:`on_enter`: Called once the screen is fully displayed
        - :ref:`on_pre_leave`: Called before the screen is left
        - :ref:`on_leave`: Last function called by this screen before dying. Unloads all widgets
    """
    #region   --------------------------- MEMBERS
    wantedRotation = 0
    currentRotation = 0
    ReadyForNextWindow:bool = False
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("AppLoading")
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
            The :ref:`Startup` screen will check, verify and load the cached JSON of the application
            so that the application's last values will be loaded as they were before it closed.
            This means that anything like themes and languages will stay in memory and won't reset
            to default values each time the application is started.
            If no cached json is found, it will be created automatically and default values will be stored
            in it.
        """
        Debug.Start("AppLoading.py: on_pre_enter")
        self.padding = 25
        self.spacing = 25

        #region ---- Background
        import os
        from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
        from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
        path = os.getcwd()

        background = GetBackgroundImage(AppendPath(path, "/Libraries/Backgrounds/AppLoading/Dark.png"),
                                        AppendPath(path, "/Libraries/Backgrounds/AppLoading/Light.png"))
        #endregion
        #region ---- Layouts
        self.Layout = MDFloatLayout()
        self.LoadingWheelLayout = MDBoxLayout()
        self.LoadingWheelLayout.size_hint = (0.5,0.5)
        self.LoadingWheelLayout.pos_hint = {'center_x': 0.5, 'center_y':0.5}
        self.LoadingWheelLayout.size_hint_max = (Window.width/2.5, Window.width/2.5)
        self.LoadingWheelLayout.size_hint_min = (Window.width/2.5, Window.width/2.5)
        #endregion

        #region ---- Widgets
        # Regular widgets
        self.LoadingStep = MDLabel(text="Loading", halign="center", valign="bottom")
        self.LoadingWheel = OutlineDial(trackWidth=5, fillingWidth=10)
        self.LoadingWheel.Min = 0
        self.LoadingWheel.Value = 0

        # Centered Kontrol logo
        if(MDApp.get_running_app().theme_cls.theme_style == "Dark"):
            self.KontrolLogo = MDIconButton(icon="Libraries/Icons/Logo/White_BRS_K.png", font_style='Icon', font_size = "100sp", halign = "center", valign = "center", disabled = True, opacity=1)
        else:
            self.KontrolLogo = MDIconButton(icon="Libraries/Icons/Logo/Black_BRS_K.png", font_style='Icon', font_size = "100sp", halign = "center", valign = "center", disabled = True, opacity=1)

        # self.LoadingWheel.UseCustomFillingColor = get_color_from_hex(colors[MDApp.get_running_app().theme_cls.primary_palette]["500"])
        self.LoadingWheel.UseCustomFillingColor = get_color_from_hex(colors[MDApp.get_running_app().theme_cls.primary_palette]["500"])
        self.LoadingWheel.ShowTrack = False
        self.LoadingWheel.EndAngle = 180
        self.LoadingWheel.StartAngle = -180

        # Widget settings
        self.LoadingStep.font_style = "H4"
        self.LoadingStep.size_hint = (1,0.125)
        self.LoadingWheel.ShowShadow = False
        self.LoadingWheel.ShowBackground = False
        self.KontrolLogo.icon_size = Window.height/2.5
        self.KontrolLogo.pos_hint = {'center_x': 0.5, 'center_y':0.5}
        #endregion

        #region ---- Initial status of Images
        #endregion

        #region ---- add_widgets
        self.add_widget(background)
        self.LoadingWheelLayout.add_widget(self.LoadingWheel)
        self.Layout.add_widget(self.LoadingWheelLayout)
        self.Layout.add_widget(self.KontrolLogo)
        self.Layout.add_widget(self.LoadingStep)
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
            Starts the BRS logo's startup screen.
        """
        Debug.Start("AppLoading.py: on_enter")
        self.LoadingWheel.animated = True

        #starting the spinning animation
        self.KontrolLogo.opacity = 1
        self.Animation = Animation(pos_hint={'center_x': 0.5, 'center_y':0.5}, opacity=2, duration=1.5, t="in_out_quart")
        self.Animation.bind(on_progress = self.RotateLetter)
        self.Animation.start(self.KontrolLogo)

        #Scheduling loaders
        LoadApplication(self.Update, self.SetStepTotalCount)
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
        Debug.Start("AppLoading.py: on_pre_leave")
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
        Debug.Start("AppLoading.py: on_leave")
        Debug.Log("Attempting to remove self from AppManager's widgets")
        self.clear_widgets()
        AppManager.manager.remove_widget(self)
        Debug.End()
# ------------------------------------------------------------------------
    def Update(self, loadingMessage:str, loadingStep:float):
        """
            Update:
            -------
            This function updates what is shown on the AppLoading screen.
            it changes the text to display below the loading wheel as well
            as the :ref:`OutlineDial`'s value to indicate a progression
            in the application's loading steps.
        """
        Debug.Start("AppLoading -> Update", DontDebug=True)
        Debug.Log("Updating loading message")
        self.LoadingStep.text = _(loadingMessage)
        Debug.Log("Updating loading wheel's value")
        self.LoadingWheel.Value = loadingStep
        Debug.End(ContinueDebug=True)
# ------------------------------------------------------------------------
    def SetStepTotalCount(self, count):
        """
            SetStepTotalCount:
            ------------------
            This function puts the amount of steps to load into the
            OutlineDial's maximum value.
        """
        Debug.Start("AppLoading -> SetStepTotalCount")
        self.LoadingWheel.Max = count
        Debug.End()
# ------------------------------------------------------------------------
    def RotateLetter(self, *args):
        # Debug.Start("RotateLetter")
        wanted = (self.KontrolLogo.opacity - 1) * -360
        current = self.currentRotation
        difference = wanted-current
        self.currentRotation = self.currentRotation + difference

        with self.KontrolLogo.canvas.before:
            PushMatrix()
            Rotate(origin=self.KontrolLogo.center, angle=difference)

        with self.KontrolLogo.canvas.after:
            PopMatrix()

        if(self.KontrolLogo.opacity >= 2 and (self.LoadingWheel.Value != self.LoadingWheel.Max)):
            #reset opacity to 1 as it's what we use to trick it into turning
            self.KontrolLogo.opacity = 1
            self.Animation = Animation(pos_hint={'center_x': 0.5, 'center_y':0.5}, opacity=2, duration=1.5, t="in_out_quart")
            self.Animation.bind(on_progress = self.RotateLetter)
            self.Animation.start(self.KontrolLogo)
            self.ReadyForNextWindow = False

        if(self.LoadingWheel.Value >= self.LoadingWheel.Max and self.KontrolLogo.opacity >= 2):
            self.ReadyForNextWindow = True
            AppLoading_Screens._Exit()

        # Debug.End()

LoadingLog.End("AppLoading.py")