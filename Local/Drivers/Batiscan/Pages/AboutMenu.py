#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Local.Drivers.Batiscan.Programs.Communications.UDP import BatiscanUDP
from Local.Drivers.Batiscan.Programs.Communications.bfio import PlaneIDs, getters
from Local.Drivers.Batiscan.Programs.Controls.controls import BatiscanControls
LoadingLog.Start("AboutMenu.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import os
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Shadow, Rounding
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
from Libraries.BRS_Python_Libraries.BRS.PnP.controls import Controls
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
from kivy.uix.screenmanager import Screen, SlideTransition
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import("KivyMD")
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.recyclegridlayout import MDRecycleGridLayout
from kivymd.uix.recycleview import RecycleView
from kivymd.uix.list import ThreeLineListItem
    
#endregion
#region ------------------------------------------------------ Kontrol
LoadingLog.Import("Local")
from Programs.Local.Hardware.RGB import KontrolRGB
from Local.Drivers.Batiscan.Programs.Controls.actions import batiscanAxesActions, batiscanButtonsActions
from Local.Drivers.Batiscan.Programs.GUI.Cards import ListCard
# from Programs.Local.GUI.Cards import ButtonCard, DeviceDriverCard
# from Programs.Pages.PopUps import PopUpsHandler, PopUps_Screens, PopUpTypeEnum
#endregion
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Screen class
#====================================================================#
LoadingLog.Class("AboutMenu_Screens")
class AboutMenu_Screens:
    """
        AboutMenu_Screens:
        ================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`AboutMenu`.

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
        AboutMenu_Screens._exitClass = screenClass
        AboutMenu_Screens._exitName  = screenName

        AboutMenu_Screens._exitTransition = transition
        AboutMenu_Screens._exitDuration = duration
        AboutMenu_Screens._exitDirection = direction
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
        AboutMenu_Screens._callerClass = screenClass
        AboutMenu_Screens._callerName  = screenName

        AboutMenu_Screens._callerTransition = transition
        AboutMenu_Screens._callerDuration = duration
        AboutMenu_Screens._callerDirection = direction
        return False

    def _Exit(*args) -> Execution:
        """
            Attempt to go to the specified screen that was set using :ref:`SetExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("AboutMenu_Screens -> _Exit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(AboutMenu_Screens._exitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(AboutMenu_Screens._exitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                AboutMenu_Screens._exitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(AboutMenu_Screens._exitClass(name=AboutMenu_Screens._exitName))
        except:
            Debug.Error("AppLoading -> Exception occured.")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = AboutMenu_Screens._exitTransition()
        AppManager.manager.transition.duration = AboutMenu_Screens._exitDuration
        AppManager.manager.transition.direction = AboutMenu_Screens._exitDirection

        # try:
        AppManager.manager.current = AboutMenu_Screens._exitName
        # except:
            # return True
        Debug.End()
        return False

    def Call(*args) -> Execution:
        """
            Attempt to go to the main screen that is being handled by this class.

            Returns:
                Execution
        """
        Debug.Start("AboutMenu_Screens -> Call()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if caller class was specified
            Debug.Log("Checking caller class")
            if(AboutMenu_Screens._callerClass == None):
                Debug.Error("No caller class specified.")
                Debug.End()
                return True

            Debug.Log("Checking caller name")
            if(AboutMenu_Screens._callerName == None):
                Debug.Error("No caller name specified.")
                Debug.End()
                return True

            Debug.Log("Attempting to add widget")
            AppManager.manager.add_widget(AboutMenu(name="AboutMenu"))
        except:
            Debug.Error("Exception occured while handling Call()")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = AboutMenu_Screens._callerTransition()
        AppManager.manager.transition.duration = AboutMenu_Screens._callerDuration
        AppManager.manager.transition.direction = AboutMenu_Screens._callerDirection

        # try:
        AppManager.manager.current = "AboutMenu"
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
LoadingLog.Class("AboutMenu")
class AboutMenu(Screen):
    """
        AboutMenu:
        ==========
        Summary:
        --------
        This class's purpose is to handle a Kivymd screen
        that displays informations to the user such as Batiscan's
        live sensor and state values, currently wanted values,
        aswell as current action binded and which ones Batiscan
        uses.
    """
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("AboutMenu -> __init__")
        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
        """
        Debug.Start("AboutMenu -> on_pre_enter")
        KontrolRGB.FastLoadingAnimation()
        self.padding = 0
        self.spacing = 0

        #region ---------------------------- Background
        path = os.getcwd()
        background = GetBackgroundImage(AppendPath(path, "/Local/Drivers/Batiscan/Libraries/Backgrounds/Menu/Dark.png"),
                                        AppendPath(path, "/Local/Drivers/Batiscan/Libraries/Backgrounds/Menu/Light.png"))
        #endregion

        #region ---------------------------- Layouts
        self.Layout = MDFloatLayout()
        #endregion

        #region ---------------------------- Scrollview
        # Create a horizontal box layout offset by half the screen to center the first profile in view.
        self.ScrollItems = MDBoxLayout(size_hint=(1,1), pos_hint = {'top': 1, 'left': 0}, orientation='horizontal', spacing="100sp", padding = (50,50,50,50), size_hint_x=None)
        self.ScrollItems.bind(minimum_width = self.ScrollItems.setter('width'))

        # Create the ScrollView view and add the box layout to it
        self.ScrollView = MDScrollView(pos_hint = {'top': 1, 'left': 0}, scroll_type=['bars','content'], size_hint = (1,1))
        self.ScrollView.smooth_scroll_end = 10

        # Add widgets
        self.ScrollView.add_widget(self.ScrollItems)
        #endregion

        #region ---------------------------- Get Lists

        #endregion

        #region ---------------------------- Cards
        self.CurrentValueCard   = ListCard(title=_("Current Values"), initialDataList = self._GetActionBindingLists())
        self.WantedValueCard    = ListCard(title=_("Wanted Values"), initialDataList = self._GetActionBindingLists())
        self.ActionBindingCard  = ListCard(title=_("Actions Bindings"), initialDataList = self._GetActionBindingLists())
        self.AboutInfoCard      = ListCard(title=_("About Batiscan"), initialDataList = self._GetActionBindingLists())
        #endregion

        #region ---------------------------- Cards to Scrollview
        self.ScrollItems.add_widget(self.AboutInfoCard)
        self.ScrollItems.add_widget(self.ActionBindingCard)
        self.ScrollItems.add_widget(self.WantedValueCard)
        self.ScrollItems.add_widget(self.CurrentValueCard)
        #endregion


        #region ---------------------------- ToolBar
        from Local.Drivers.Batiscan.Programs.GUI.Navigation import DebugNavigationBar
        self.ToolBar = DebugNavigationBar(pageTitle=_("About"))
        #endregion

        self.Layout.add_widget(self.ScrollView)
        self.Layout.add_widget(self.ToolBar.ToolBar)
        self.Layout.add_widget(self.ToolBar.NavDrawer)
        self.add_widget(background)
        self.add_widget(self.Layout)
        Debug.End()
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            Function called when the screen is fully entered in view.
            In this case, once the view is fully loaded, the cards
            will slowly elevate to the wanted value.
        """
        Debug.Start("AboutMenu -> on_enter")
        KontrolRGB.DisplayDefaultColor()

        self.AboutInfoCard.CreateRecycleLayout()
        self.ActionBindingCard.CreateRecycleLayout()
        self.WantedValueCard.CreateRecycleLayout()
        self.CurrentValueCard.CreateRecycleLayout()

        Debug.End()
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            Function called before the screen is fully left. This gives
            us time to animate the screen leaving before destroying the
            objects and instances it created.
        """
        Debug.Start("AboutMenu -> on_pre_leave")
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
        Debug.End()
        self.clear_widgets()
# ------------------------------------------------------------------------
    def _Animating(self, *args):
        """
            Call back function called each time an animation tick happens.
            We use it to add/remove the shadow of cards when entering or
            leaving the application.
        """
        pass
# ------------------------------------------------------------------------
    def create_layouts(self,*args):
        Debug.Start("create_layouts")
        self._CreateAboutRecycleView()
        self._CreateWantedValueRecycleView()
        self._CreateCurrentValueRecycleView()
        self._CreateActionBindingRecycleView()
        Debug.End()
# ------------------------------------------------------------------------
    def _CreateAboutRecycleView(self):
        Debug.Start("_CreateAboutRecycleView")
        self.AboutRecyleBoxLayout = MDRecycleGridLayout(default_size=(None,72),
                                                        default_size_hint=(1, None),
                                                        size_hint=(1, None),
                                                        orientation='lr-tb')
        self.AboutRecyleBoxLayout.padding = 25
        self.AboutRecyleBoxLayout.spacing = 5
        self.AboutRecyleBoxLayout.cols = 1

        self.AboutRecyleBoxLayout.bind(minimum_height=self.AboutRecyleBoxLayout.setter("height"))

        self.AboutRecycleView = RecycleView()
        self.AboutRecycleView.add_widget(self.AboutRecyleBoxLayout)
        self.AboutRecycleView.viewclass = ThreeLineListItem
        self.AboutInfoCardLayout.add_widget(self.AboutRecycleView)

        # for name,dictionary in BFIO_Functions.items():
# 
            # self.recycleView.data.insert(0,
                                        #  {
                                            #  "text" : name,
                                            #  "secondary_text" : str(dictionary["Callsign"]),
                                            #  "halign" : "left",
                                            #  "on_release" : (lambda x: lambda: self.ButtonPressed(x))([name, dictionary]),
                                            #  "icon" : "trash-can"
                                        #  })
        Debug.End()
# ------------------------------------------------------------------------
    def _CreateWantedValueRecycleView(self):
        Debug.Start("_CreateWantedValueRecycleView")
        self.WantedValueRecyleBoxLayout = MDRecycleGridLayout(default_size=(None,72),
                                                default_size_hint=(1, None),
                                                size_hint=(1, None),
                                                orientation='lr-tb')
        self.WantedValueRecyleBoxLayout.padding = 25
        self.WantedValueRecyleBoxLayout.spacing = 5
        self.WantedValueRecyleBoxLayout.cols = 1

        self.WantedValueRecyleBoxLayout.bind(minimum_height=self.WantedValueRecyleBoxLayout.setter("height"))

        self.WantedValueRecycleView = RecycleView()
        self.WantedValueRecycleView.add_widget(self.WantedValueRecyleBoxLayout)
        self.WantedValueRecycleView.viewclass = ThreeLineListItem
        self.WantedValueCardLayout.add_widget(self.WantedValueRecycleView)

        # for name,dictionary in BFIO_Functions.items():
# 
            # self.recycleView.data.insert(0,
                                        #  {
                                            #  "text" : name,
                                            #  "secondary_text" : str(dictionary["Callsign"]),
                                            #  "halign" : "left",
                                            #  "on_release" : (lambda x: lambda: self.ButtonPressed(x))([name, dictionary]),
                                            #  "icon" : "trash-can"
                                        #  })
        Debug.End()
# ------------------------------------------------------------------------
    def _CreateCurrentValueRecycleView(self):
        Debug.Start("_CreateCurrentValueRecycleView")
        self.CurrentValueRecyleBoxLayout = MDRecycleGridLayout(default_size=(None,72),
                                                default_size_hint=(1, None),
                                                size_hint=(1, None),
                                                orientation='lr-tb')
        self.CurrentValueRecyleBoxLayout.padding = 25
        self.CurrentValueRecyleBoxLayout.spacing = 5
        self.CurrentValueRecyleBoxLayout.cols = 1

        self.CurrentValueRecyleBoxLayout.bind(minimum_height=self.CurrentValueRecyleBoxLayout.setter("height"))

        self.CurrentValueRecycleView = RecycleView()
        self.CurrentValueRecycleView.add_widget(self.CurrentValueRecyleBoxLayout)
        self.CurrentValueRecycleView.viewclass = ThreeLineListItem
        self.CurrentValueCardLayout.add_widget(self.CurrentValueRecycleView)

        # for name,dictionary in BFIO_Functions.items():
# 
            # self.recycleView.data.insert(0,
                                        #  {
                                            #  "text" : name,
                                            #  "secondary_text" : str(dictionary["Callsign"]),
                                            #  "halign" : "left",
                                            #  "on_release" : (lambda x: lambda: self.ButtonPressed(x))([name, dictionary]),
                                            #  "icon" : "trash-can"
                                        #  })
        Debug.End()
# ------------------------------------------------------------------------
    def _CreateActionBindingRecycleView(self):
        Debug.Start("_CreateActionBindingRecycleView")
        self.ActionBindingRecyleBoxLayout = MDRecycleGridLayout(default_size=(None,72),
                                                default_size_hint=(1, None),
                                                size_hint=(1, None),
                                                orientation='lr-tb')
        self.ActionBindingRecyleBoxLayout.padding = 25
        self.ActionBindingRecyleBoxLayout.spacing = 5
        self.ActionBindingRecyleBoxLayout.cols = 1

        self.ActionBindingRecyleBoxLayout.bind(minimum_height=self.ActionBindingRecyleBoxLayout.setter("height"))

        self.ActionBindingRecycleView = RecycleView()
        self.ActionBindingRecycleView.add_widget(self.ActionBindingRecyleBoxLayout)
        self.ActionBindingRecycleView.viewclass = ThreeLineListItem
        self.ActionBindingCardLayout.add_widget(self.ActionBindingRecycleView)

        for name,dictionary in batiscanAxesActions.items():

            firstLine = _("Axis: ") + name
            secondLine = _(batiscanAxesActions[name]["description"])

            # Is the current axis binded to any hardware addons / BrSpand cards?
            if(Controls._axes[name]["binded"]):
                # That axis is binded
                thirdText:str = _("Controlled by") + ": " + Controls._axes[name]["bindedTo"]
            else:
                thirdText:str = _("Not binded")

            self.ActionBindingRecycleView.data.insert(0,
                                         {
                                             "text" : firstLine,
                                             "secondary_text" : secondLine,
                                             "tertiary_text" : thirdText,
                                             "halign" : "left",
                                         })

        for name,dictionary in batiscanButtonsActions.items():

            firstLine = _("Button") + ": " + name
            secondLine = _(dictionary["description"])

            # Is the current axis binded to any hardware addons / BrSpand cards?
            if(Controls._buttons[name]["binded"]):
                # That axis is binded
                thirdText:str = _("Controlled by") + ": " + Controls._buttons[name]["bindedTo"]
            else:
                thirdText:str = _("Not binded")

            self.ActionBindingRecycleView.data.insert(0,
                                         {
                                             "text" : firstLine,
                                             "secondary_text" : secondLine,
                                             "tertiary_text" : thirdText,
                                             "halign" : "left",
                                         })
        Debug.End()
# ------------------------------------------------------------------------
    def _GetActionBindingLists(self):
        Debug.Start("_GetActionBindingLists")

        resultedList = []

        for name,dictionary in batiscanAxesActions.items():

            firstLine = _("Axis: ") + name
            secondLine = _(batiscanAxesActions[name]["description"])

            # Is the current axis binded to any hardware addons / BrSpand cards?
            if(Controls._axes[name]["binded"]):
                # That axis is binded
                thirdLine:str = _("Controlled by") + ": " + Controls._axes[name]["bindedTo"]
            else:
                thirdLine:str = _("Not binded")

            resultedList.append({"text" : firstLine, "secondary_text":secondLine, "tertiary_text":thirdLine})

        for name,dictionary in batiscanButtonsActions.items():

            firstLine = _("Button") + ": " + name
            secondLine = _(dictionary["description"])

            # Is the current axis binded to any hardware addons / BrSpand cards?
            if(Controls._buttons[name]["binded"]):
                # That axis is binded
                thirdLine:str = _("Controlled by") + ": " + Controls._buttons[name]["bindedTo"]
            else:
                thirdLine:str = _("Not binded")

            resultedList.append({"text" : firstLine, "secondary_text":secondLine, "tertiary_text":thirdLine})
        Debug.End()
        return resultedList
# ------------------------------------------------------------------------
LoadingLog.End("AboutMenu.py")