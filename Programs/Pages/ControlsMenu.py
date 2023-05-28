#====================================================================#
# File Information
#====================================================================#

#====================================================================#
from ast import Add
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
LoadingLog.Start("ControlMenu.py")
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
# from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import FilesFinder, AppendPath
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
from Libraries.BRS_Python_Libraries.BRS.Utilities.addons import Addons, AddonEnum
from Programs.Local.GUI.Cards import WidgetCard
from Libraries.BRS_Python_Libraries.BRS.GUI.Containers.cards import ControlsCard, ControlsCardData
from Libraries.BRS_Python_Libraries.BRS.PnP.controls import Controls, SoftwareButtons, SoftwareAxes
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.recycleview import RecycleView
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.clock import Clock
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import("KivyMD")
# from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
# from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.swiper import MDSwiper, MDSwiperItem
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import ThreeLineListItem, ThreeLineRightIconListItem, IconRightWidget
from kivymd.uix.dialog import MDDialog
#endregion
#region ------------------------------------------------------ Kontrol
LoadingLog.Import("Local")
from ..Local.GUI.Navigation import AppNavigationBar
from ..Local.Hardware.RGB import KontrolRGB
# from ..Local.GUI.Cards import ButtonCard, DeviceDriverCard
# from ..Local.FileHandler.deviceDriver import GetDrivers, CheckIntegrity
from ..Pages.PopUps import PopUpsHandler,PopUps_Screens, PopUpTypeEnum
#endregion
#====================================================================#
# Functions
#====================================================================#
#====================================================================#
# Screen class
#====================================================================#
LoadingLog.Class("ControlMenu_Screens")
class ControlMenu_Screens:
    """
        ControlMenu_Screens:
        ================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`ControlMenu`.

        Description:
        ------------
        This class holds the different types of callers of the ControlMenu
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
        ControlMenu_Screens._exitClass = screenClass
        ControlMenu_Screens._exitName  = screenName

        ControlMenu_Screens._exitTransition = transition
        ControlMenu_Screens._exitDuration = duration
        ControlMenu_Screens._exitDirection = direction
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
        ControlMenu_Screens._callerClass = screenClass
        ControlMenu_Screens._callerName  = screenName

        ControlMenu_Screens._callerTransition = transition
        ControlMenu_Screens._callerDuration = duration
        ControlMenu_Screens._callerDirection = direction
        return False

    def _Exit(*args) -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("ControlMenu_Screens -> _Exit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(ControlMenu_Screens._exitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(ControlMenu_Screens._exitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                ControlMenu_Screens._exitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(ControlMenu_Screens._exitClass(name=ControlMenu_Screens._exitName))
        except:
            Debug.Error("ControlMenu_Screens -> Exception occured.")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = ControlMenu_Screens._exitTransition()
        AppManager.manager.transition.duration = ControlMenu_Screens._exitDuration
        AppManager.manager.transition.direction = ControlMenu_Screens._exitDirection

        # try:
        AppManager.manager.current = ControlMenu_Screens._exitName
        # except:
            # return True
        Debug.End()
        return False

    def Call(*args) -> bool:
        """
            Attempt to go to the main screen that is being handled by this class.

            Returns:
                bool: `True`:  Something went wrong and the screen can't be loaded. `False`: Success
        """
        Debug.Start("NetworkMenu_Screens -> Call()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if caller class was specified
            # Debug.Log("Checking caller class")
            # if(AccountMenu_Screens._callerClass == None):
                # Debug.Error("No caller class specified.")
                # Debug.End()
                # return True

            # Debug.Log("Checking caller name")
            # if(AccountMenu_Screens._callerName == None):
                # Debug.Error("No caller name specified.")
                # Debug.End()
                # return True

            Debug.Log("Attempting to add widget")
            AppManager.manager.add_widget(ControlMenu(name="ControlMenu"))
        except:
            Debug.Error("Exception occured while handling Call()")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = ControlMenu_Screens._callerTransition()
        AppManager.manager.transition.duration = ControlMenu_Screens._callerDuration
        AppManager.manager.transition.direction = ControlMenu_Screens._callerDirection

        # try:
        AppManager.manager.current = "ControlMenu"
        Debug.Log("Screen successfully changed")
        # except:
            # Debug.Error("Failed to add AppLoading as current screen.")
            # Debug.End()
            # return True
        Debug.End()
        return False
    #endregion
#--------------------------------------------------------------------
class ButtonMenu_Screens:
    """
        ButtonMenu_Screens:
        ================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`ButtonMenu`.

        Description:
        ------------
        This class holds the different types of callers of the ButtonMenu
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
    def SetExiter(screenClass, screenName:str, transition=SlideTransition, duration:float=0.5, direction:str="left") -> bool:
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
        ButtonMenu_Screens._exitClass = screenClass
        ButtonMenu_Screens._exitName  = screenName

        ButtonMenu_Screens._exitTransition = transition
        ButtonMenu_Screens._exitDuration = duration
        ButtonMenu_Screens._exitDirection = direction
        return False

    def SetCaller(screenClass, screenName:str, transition=SlideTransition, duration:float=0.5, direction:str="right") -> bool:
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
        ButtonMenu_Screens._callerClass = screenClass
        ButtonMenu_Screens._callerName  = screenName

        ButtonMenu_Screens._callerTransition = transition
        ButtonMenu_Screens._callerDuration = duration
        ButtonMenu_Screens._callerDirection = direction
        return False

    def _Exit(*args) -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("ButtonMenu_Screens -> _Exit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(ButtonMenu_Screens._exitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(ButtonMenu_Screens._exitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                ButtonMenu_Screens._exitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(ButtonMenu_Screens._exitClass(name=ButtonMenu_Screens._exitName))
        except:
            Debug.Error("ButtonMenu_Screens -> Exception occured.")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = ButtonMenu_Screens._exitTransition()
        AppManager.manager.transition.duration = ButtonMenu_Screens._exitDuration
        AppManager.manager.transition.direction = ButtonMenu_Screens._exitDirection

        # try:
        AppManager.manager.current = ButtonMenu_Screens._exitName
        # except:
            # return True
        Debug.End()
        return False

    def Call(*args) -> bool:
        """
            Attempt to go to the main screen that is being handled by this class.

            Returns:
                bool: `True`:  Something went wrong and the screen can't be loaded. `False`: Success
        """
        Debug.Start("ButtonMenu_Screens -> Call()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if caller class was specified
            # Debug.Log("Checking caller class")
            # if(AccountMenu_Screens._callerClass == None):
                # Debug.Error("No caller class specified.")
                # Debug.End()
                # return True

            # Debug.Log("Checking caller name")
            # if(AccountMenu_Screens._callerName == None):
                # Debug.Error("No caller name specified.")
                # Debug.End()
                # return True

            Debug.Log("Attempting to add widget")
            AppManager.manager.add_widget(ButtonMenu(name="ButtonMenu"))
        except:
            Debug.Error("Exception occured while handling Call()")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = ButtonMenu_Screens._callerTransition()
        AppManager.manager.transition.duration = ButtonMenu_Screens._callerDuration
        AppManager.manager.transition.direction = ButtonMenu_Screens._callerDirection

        # try:
        AppManager.manager.current = "ButtonMenu"
        Debug.Log("Screen successfully changed")
        # except:
            # Debug.Error("Failed to add AppLoading as current screen.")
            # Debug.End()
            # return True
        Debug.End()
        return False
    #endregion
#--------------------------------------------------------------------
class AxisMenu_Screens:
    """
        ButtonMenu_Screens:
        ================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`ButtonMenu`.

        Description:
        ------------
        This class holds the different types of callers of the ButtonMenu
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
    def SetExiter(screenClass, screenName:str, transition=SlideTransition, duration:float=0.5, direction:str="left") -> bool:
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
        AxisMenu_Screens._exitClass = screenClass
        AxisMenu_Screens._exitName  = screenName

        AxisMenu_Screens._exitTransition = transition
        AxisMenu_Screens._exitDuration = duration
        AxisMenu_Screens._exitDirection = direction
        return False

    def SetCaller(screenClass, screenName:str, transition=SlideTransition, duration:float=0.5, direction:str="left") -> bool:
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
        AxisMenu_Screens._callerClass = screenClass
        AxisMenu_Screens._callerName  = screenName

        AxisMenu_Screens._callerTransition = transition
        AxisMenu_Screens._callerDuration = duration
        AxisMenu_Screens._callerDirection = direction
        return False

    def _Exit(*args) -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("AxisMenu_Screens -> _Exit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(AxisMenu_Screens._exitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(AxisMenu_Screens._exitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                AxisMenu_Screens._exitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(AxisMenu_Screens._exitClass(name=AxisMenu_Screens._exitName))
        except:
            Debug.Error("AxisMenu_Screens -> Exception occured.")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = AxisMenu_Screens._exitTransition()
        AppManager.manager.transition.duration = AxisMenu_Screens._exitDuration
        AppManager.manager.transition.direction = AxisMenu_Screens._exitDirection

        # try:
        AppManager.manager.current = AxisMenu_Screens._exitName
        # except:
            # return True
        Debug.End()
        return False

    def Call(*args) -> bool:
        """
            Attempt to go to the main screen that is being handled by this class.

            Returns:
                bool: `True`:  Something went wrong and the screen can't be loaded. `False`: Success
        """
        Debug.Start("AxisMenu_Screens -> Call()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if caller class was specified
            # Debug.Log("Checking caller class")
            # if(AccountMenu_Screens._callerClass == None):
                # Debug.Error("No caller class specified.")
                # Debug.End()
                # return True

            # Debug.Log("Checking caller name")
            # if(AccountMenu_Screens._callerName == None):
                # Debug.Error("No caller name specified.")
                # Debug.End()
                # return True

            Debug.Log("Attempting to add widget")
            AppManager.manager.add_widget(AxisMenu(name="AxisMenu"))
        except:
            Debug.Error("Exception occured while handling Call()")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = AxisMenu_Screens._callerTransition()
        AppManager.manager.transition.duration = AxisMenu_Screens._callerDuration
        AppManager.manager.transition.direction = AxisMenu_Screens._callerDirection

        # try:
        AppManager.manager.current = "AxisMenu"
        Debug.Log("Screen successfully changed")
        # except:
            # Debug.Error("Failed to add AppLoading as current screen.")
            # Debug.End()
            # return True
        Debug.End()
        return False
    #endregion
#--------------------------------------------------------------------
class BinderSelector_Screens:
    """
        BinderSelector_Screens:
        =======================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`ButtonMenu`.

        Description:
        ------------
        This class holds the different types of callers of the ButtonMenu
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
    def SetExiter(screenClass, screenName:str, transition=SlideTransition, duration:float=0.5, direction:str="right") -> bool:
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
        BinderSelector_Screens._exitClass = screenClass
        BinderSelector_Screens._exitName  = screenName

        BinderSelector_Screens._exitTransition = transition
        BinderSelector_Screens._exitDuration = duration
        BinderSelector_Screens._exitDirection = direction
        return False

    def SetCaller(screenClass, screenName:str, transition=SlideTransition, duration:float=0.5, direction:str="right") -> bool:
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
        BinderSelector_Screens._callerClass = screenClass
        BinderSelector_Screens._callerName  = screenName

        BinderSelector_Screens._callerTransition = transition
        BinderSelector_Screens._callerDuration = duration
        BinderSelector_Screens._callerDirection = direction
        return False

    def _Exit(*args) -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("BinderSelector_Screens -> _Exit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(BinderSelector_Screens._exitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(BinderSelector_Screens._exitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                BinderSelector_Screens._exitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(BinderSelector_Screens._exitClass(name=BinderSelector_Screens._exitName))
        except:
            Debug.Error("BinderSelector_Screens -> Exception occured.")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = BinderSelector_Screens._exitTransition()
        AppManager.manager.transition.duration = BinderSelector_Screens._exitDuration
        AppManager.manager.transition.direction = BinderSelector_Screens._exitDirection

        # try:
        AppManager.manager.current = BinderSelector_Screens._exitName
        # except:
            # return True
        Debug.End()
        return False

    def Call(*args) -> bool:
        """
            Attempt to go to the main screen that is being handled by this class.

            Returns:
                bool: `True`:  Something went wrong and the screen can't be loaded. `False`: Success
        """
        Debug.Start("BinderSelector_Screens -> Call()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if caller class was specified
            # Debug.Log("Checking caller class")
            # if(AccountMenu_Screens._callerClass == None):
                # Debug.Error("No caller class specified.")
                # Debug.End()
                # return True

            # Debug.Log("Checking caller name")
            # if(AccountMenu_Screens._callerName == None):
                # Debug.Error("No caller name specified.")
                # Debug.End()
                # return True

            Debug.Log("Attempting to add widget")
            AppManager.manager.add_widget(BinderSelectorMenu(name="BinederSelectorMenu"))
        except:
            Debug.Error("Exception occured while handling Call()")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = BinderSelector_Screens._callerTransition()
        AppManager.manager.transition.duration = BinderSelector_Screens._callerDuration
        AppManager.manager.transition.direction = BinderSelector_Screens._callerDirection

        # try:
        AppManager.manager.current = "BinederSelectorMenu"
        Debug.Log("Screen successfully changed")
        # except:
            # Debug.Error("Failed to add AppLoading as current screen.")
            # Debug.End()
            # return True
        Debug.End()
        return False
    #endregion
#--------------------------------------------------------------------
class BindSelectMenu_Screens:
    """
        BindSelectMenu_Screens:
        =======================
        Summary:
        --------
        This class allows the handling of the transitional screen
        :class:`BindSelectMenu`.

        Description:
        ------------
        This class holds the different types of callers of the ButtonMenu
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
    def SetExiter(screenClass, screenName:str, transition=SlideTransition, duration:float=0.5, direction:str="right") -> bool:
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
        BindSelectMenu_Screens._exitClass = screenClass
        BindSelectMenu_Screens._exitName  = screenName

        BindSelectMenu_Screens._exitTransition = transition
        BindSelectMenu_Screens._exitDuration = duration
        BindSelectMenu_Screens._exitDirection = direction
        return False

    def SetCaller(screenClass, screenName:str, transition=SlideTransition, duration:float=0.5, direction:str="right") -> bool:
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
        BindSelectMenu_Screens._callerClass = screenClass
        BindSelectMenu_Screens._callerName  = screenName

        BindSelectMenu_Screens._callerTransition = transition
        BindSelectMenu_Screens._callerDuration = duration
        BindSelectMenu_Screens._callerDirection = direction
        return False

    def _Exit(*args) -> bool:
        """
            Attempt to go to the specified screen that was set using :ref:`SetExiter`.

            Returns:
                bool: `True`:  Something went wrong and the wanted exiter screen can't be loaded. `False`: Success
        """
        Debug.Start("BindSelectMenu_Screens -> _Exit()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if exit class was specified
            Debug.Log("Checking exit class")
            if(BindSelectMenu_Screens._exitClass == None):
                Debug.Error("Attempted to call exit while no exit class were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit name")
            if(BindSelectMenu_Screens._exitName == None):
                Debug.Error("Attempted to call exit while no exit name were specified")
                Debug.End()
                return True

            Debug.Log("Checking exit class Call()")
            try:
                Debug.Log("Trying to call exit class caller.")
                BindSelectMenu_Screens._exitClass.Call()
                Debug.Log("Success")
                Debug.End()
                return False
            except:
                Debug.Log("Class specified wasn't an _Screen class.")
                AppManager.manager.add_widget(BindSelectMenu_Screens._exitClass(name=BindSelectMenu_Screens._exitName))
        except:
            Debug.Error("BindSelectMenu_Screens -> Exception occured.")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = BindSelectMenu_Screens._exitTransition()
        AppManager.manager.transition.duration = BindSelectMenu_Screens._exitDuration
        AppManager.manager.transition.direction = BindSelectMenu_Screens._exitDirection

        # try:
        AppManager.manager.current = BindSelectMenu_Screens._exitName
        # except:
            # return True
        Debug.End()
        return False

    def Call(*args) -> bool:
        """
            Attempt to go to the main screen that is being handled by this class.

            Returns:
                bool: `True`:  Something went wrong and the screen can't be loaded. `False`: Success
        """
        Debug.Start("BindSelectMenu_Screens -> Call()")
        # Attempt to add the screen class as a widget of the AppManager
        try:
            # Check if caller class was specified
            # Debug.Log("Checking caller class")
            # if(AccountMenu_Screens._callerClass == None):
                # Debug.Error("No caller class specified.")
                # Debug.End()
                # return True

            # Debug.Log("Checking caller name")
            # if(AccountMenu_Screens._callerName == None):
                # Debug.Error("No caller name specified.")
                # Debug.End()
                # return True

            Debug.Log("Attempting to add widget")
            AppManager.manager.add_widget(BindSelectMenu(name="BindSelectMenu"))
        except:
            Debug.Error("Exception occured while handling Call()")
            Debug.End()
            return True

        # Attempt to call the added screen
        AppManager.manager.transition = BindSelectMenu_Screens._callerTransition()
        AppManager.manager.transition.duration = BindSelectMenu_Screens._callerDuration
        AppManager.manager.transition.direction = BindSelectMenu_Screens._callerDirection

        # try:
        AppManager.manager.current = "BindSelectMenu"
        Debug.Log("Screen successfully changed")
        # except:
            # Debug.Error("Failed to add AppLoading as current screen.")
            # Debug.End()
            # return True
        Debug.End()
        return False
    #endregion
#--------------------------------------------------------------------

def DeleteHardwareBinding(*args):
    """
        DeleteHardwareBinding:
        ======================
        Summary:
        --------
        Function that attempts
        to delete whats currently binded
        to something.
    """
    Debug.Start("DeleteBindings")

    Debug.Log(f"Attempting to unbind {HeldData.whoHasItCurrentlyBinded}'s hardware from {HeldData.nameOfTheSoftwareBind}")
    if(HeldData.whatIsBeingBinded == "axes"):
        Addons.UnbindHardwareAxisFromEveryone(HeldData.nameOfTheSoftwareBind)
    else:
        Addons.UnbindHardwareButtonFromEveryone(HeldData.nameOfTheSoftwareBind)

    Debug.End()

from kivy.properties import StringProperty
class CustomThreeLineIconListItem(ThreeLineRightIconListItem):
    icon = StringProperty()

    def __init__(self, **kwargs):
        super(CustomThreeLineIconListItem, self).__init__(**kwargs)
        self.icon_widget = IconRightWidget(icon="trash-can")
        self.ids._right_container.add_widget(self.icon_widget)
        self.icon_widget.bind(on_release=lambda x: self.on_icon_press(x))

    def on_icon_press(self, *args):
        Debug.Start("on_icon_press")

        Debug.Log("Gathering informations...")
        textFromLine1 = self.text
        textFromLine2 = self.secondary_text
        textFromLine3 = self.tertiary_text

        Debug.Log(f">>> line1: {textFromLine1}")
        Debug.Log(f">>> line2: {textFromLine2}")
        Debug.Log(f">>> line3: {textFromLine3}")

        if(HeldData.whatIsBeingBinded == "axes"):
            PopUps_Screens.SetCaller(AxisMenu_Screens, "AxisMenu")
            PopUps_Screens.SetExiter(AxisMenu_Screens, "AxisMenu")
        else:
            PopUps_Screens.SetCaller(ButtonMenu_Screens, "ButtonMenu")
            PopUps_Screens.SetExiter(ButtonMenu_Screens, "ButtonMenu")

        if("binded as:" in textFromLine3):
            Debug.Log("Clearing a software representation.")
            name = self.text
            theFuckerThatBindedIt = self.secondary_text.split(": ")[1]
            whatItBindedItAs = self.tertiary_text.split(": ")[1]

            HeldData.nameOfTheSoftwareBind = name
            HeldData.whoHasItCurrentlyBinded = theFuckerThatBindedIt

            PopUpsHandler.Add(
                PopUpTypeEnum.Question,
                Message=_("Do you really want to unbind") + ": [" + name + "] ?",
                ButtonBHandler=PopUps_Screens._Exit,
                ButtonAHandler=DeleteHardwareBinding
            )
            PopUps_Screens.Call()
            Debug.End()
            return

        if("value:" in textFromLine3):
            Debug.Log("Clearing an hardware representation.")
            PopUps_Screens.SetCaller(BindSelectMenu_Screens, "BindSelectMenu")
            PopUps_Screens.SetExiter(BindSelectMenu_Screens, "BindSelectMenu")
            PopUpsHandler.Clear()

        if(textFromLine2 == "Available"):
            Debug.Log("Nothing to delete.")
            PopUpsHandler.Add(
                PopUpTypeEnum.Warning,
                Message=_("There is nothing to un-bind.")
            )
            PopUps_Screens.Call()
            Debug.End()
            return

        Debug.End()


class HeldData:
    """
        HeldData:
        =========
        Summary:
        --------
        Used to temporarly hold what is being
        changed currently by these screens.
    """
    whoHasItCurrentlyBinded:str = None
    """
        Name of an addon.
    """
    whoIsTryingToBindIt:str = None
    """
        Name of an addon.
    """

    whatIsBeingBinded:str = None
    """
        either "axes" or "buttons"
    """
    nameOfTheSoftwareBind:str = None
    """
        SoftwareAxes or SoftwareButton
    """
#====================================================================#
# Classes
#====================================================================#
LoadingLog.Class("ControlMenu")
class ControlMenu(Screen):
    """
        ControlMenu:
        -----------
        This class handles the screen of the account menu which shows
        to the user some actions that they can do with their user profiles
    """
    #region   --------------------------- MEMBERS
    ToolBar:AppNavigationBar = None
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("ControlMenu -> __init__")
        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
        """
        Debug.Start("ControlMenu -> on_pre_enter")
        KontrolRGB.FastLoadingAnimation()
        self.padding = 0
        self.spacing = 0

        #region ---- Background
        import os
        from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
        from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
        path = os.getcwd()

        background = GetBackgroundImage(AppendPath(path, "/Libraries/Backgrounds/Menus/Dark.png"),
                                        AppendPath(path, "/Libraries/Backgrounds/Menus/Light.png"))
        #endregion

        #region ---------------------------- Layouts
        self.Layout = MDFloatLayout()
        # Add widgets
        self.add_widget(background)
        #endregion
        #region ---------------------------- ToolBar
        self.ToolBar = AppNavigationBar(pageTitle=_("Controls & Keybinds"))
        #endregion

        #region ---------------------------- Cards
        self.GoToButtonsCard = WidgetCard(icon="gamepad", name=_("Buttons"))
        self.GoToAxesCard = WidgetCard(icon="sine-wave", name=_("Axes"))
        #endregion

        #region ----------------------------- Swiper
        self.SwiperLayout = MDSwiper()
        self.SwiperLayout.items_spacing = 35

        self.SwiperButtonLayout = MDSwiperItem()
        self.SwiperButtonLayout.padding = 40
        self.SwiperButtonLayout.add_widget(self.GoToButtonsCard)
        self.SwiperAxesLayout = MDSwiperItem(padding = 40)
        self.SwiperAxesLayout.add_widget(self.GoToAxesCard)

        self.SwiperLayout.add_widget(self.SwiperButtonLayout)
        self.SwiperLayout.add_widget(self.SwiperAxesLayout)
        #endregion

        ButtonMenu_Screens.SetCaller(ControlMenu_Screens, "ControlMenu")
        ButtonMenu_Screens.SetExiter(ControlMenu_Screens, "ControlMenu")
        AxisMenu_Screens.SetCaller(ControlMenu_Screens, "ControlMenu")
        AxisMenu_Screens.SetExiter(ControlMenu_Screens, "ControlMenu")
        
        self.GoToButtonsCard.PressedEnd = ButtonMenu_Screens.Call
        self.GoToAxesCard.PressedEnd = AxisMenu_Screens.Call

        self.Layout.add_widget(self.SwiperLayout)
        self.Layout.add_widget(self.ToolBar.ToolBar)
        self.Layout.add_widget(self.ToolBar.NavDrawer)
        self.add_widget(self.Layout)
        Debug.End()
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            Function called when the screen is fully entered in view.
            In this case, once the view is fully loaded, the cards
            will slowly elevate to the wanted value.
        """
        Debug.Start("ControlMenu -> on_enter")
        KontrolRGB.DisplayDefaultColor()
        Debug.End()
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            Function called before the screen is fully left. This gives
            us time to animate the screen leaving before destroying the
            objects and instances it created.
        """
        Debug.Start("ControlMenu -> on_pre_leave")
        Debug.End()
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully out of view.
        """
        Debug.Start("ControlMenu -> on_leave")
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
class ButtonMenu(Screen):
    """
        ButtonMenu:
        -----------
        This class handles the screen of the account menu which shows
        to the user some actions that they can do with their user profiles
    """
    #region   --------------------------- MEMBERS
    ToolBar:AppNavigationBar = None
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("ControlMenu -> __init__")
        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
        """
        Debug.Start("ButtonMenu -> on_pre_enter")
        KontrolRGB.FastLoadingAnimation()
        self.padding = 0
        self.spacing = 0

        #region ---- Background
        import os
        from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
        from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
        path = os.getcwd()

        background = GetBackgroundImage(AppendPath(path, "/Libraries/Backgrounds/Menus/Dark.png"),
                                        AppendPath(path, "/Libraries/Backgrounds/Menus/Light.png"))
        #endregion

        #region ---------------------------- Layouts
        self.Layout = MDFloatLayout()
        # Add widgets
        self.add_widget(background)
        #endregion
        #region ---------------------------- ToolBar
        self.ToolBar = AppNavigationBar(pageTitle=_("Controls & Keybinds"))
        #endregion

        self.create_layouts()
        HeldData.whatIsBeingBinded = "buttons"

        self.Layout.add_widget(self.ToolBar.ToolBar)
        self.Layout.add_widget(self.ToolBar.NavDrawer)
        self.add_widget(self.Layout)
        Debug.End()
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            Function called when the screen is fully entered in view.
            In this case, once the view is fully loaded, the cards
            will slowly elevate to the wanted value.
        """
        Debug.Start("ButtonMenu -> on_enter")
        KontrolRGB.DisplayDefaultColor()
        Debug.End()
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            Function called before the screen is fully left. This gives
            us time to animate the screen leaving before destroying the
            objects and instances it created.
        """
        Debug.Start("ButtonMenu -> on_pre_leave")
        Debug.End()
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully out of view.
        """
        Debug.Start("ButtonMenu -> on_leave")
        Debug.Log("Attempting to remove self from AppManager's widgets")
        self.clear_widgets()
        AppManager.manager.remove_widget(self)
        Debug.End()
        self.clear_widgets()
# ------------------------------------------------------------------------
    def create_layouts(self,*args):
        Debug.Start("create_layouts")
        self.create_recycle_view()
        Debug.End()
# ------------------------------------------------------------------------
    def create_recycle_view(self):
        Debug.Start("create_recycle_view")
        self.RecyleBoxLayout = RecycleGridLayout(default_size=(None,72),
                                                default_size_hint=(1, None),
                                                size_hint=(1, None),
                                                orientation='lr-tb')
        self.RecyleBoxLayout.padding = 25
        self.RecyleBoxLayout.spacing = 5
        self.RecyleBoxLayout.cols = 1
        # self.RecyleBoxLayout.orientation
        self.RecyleBoxLayout.bind(minimum_height=self.RecyleBoxLayout.setter("height"))

        amountOfCard = len(ControlsCardData.dataList)
        Debug.Log(f"There is {amountOfCard} cards to display")

        self.recycleView = RecycleView()
        self.recycleView.add_widget(self.RecyleBoxLayout)
        self.recycleView.viewclass = CustomThreeLineIconListItem
        self.Layout.add_widget(self.recycleView)

        for name,dictionary in Controls._buttons.items():

            theFuckerThatBindedIt = dictionary["bindedTo"]
            whatItBindedItAs = dictionary["bindedAs"]

            if(theFuckerThatBindedIt == None):
                secondaryText = _("Available")
                tertiaryText = ""
            else:
                secondaryText =  _("binded to: ") + theFuckerThatBindedIt
                tertiaryText = _("binded as: ") + whatItBindedItAs

            self.recycleView.data.insert(0,
                                         {
                                             "text" : name,
                                             "secondary_text" : secondaryText,
                                             "tertiary_text" : tertiaryText,
                                             "halign" : "left",
                                             "on_release" : (lambda x: lambda: self.ButtonPressed(x))([name, theFuckerThatBindedIt, whatItBindedItAs]),
                                             "icon" : "trash-can"
                                         })
        Debug.End()
# ------------------------------------------------------------------------
    def ButtonPressed(self, *args):
        """
            ButtonPressed:
            ==============
            Summary:
            --------
            Callback function executed when a button is
            pressed.
        """
        Debug.Start("ButtonPressed")
        Debug.Log(args)
        HeldData.whatIsBeingBinded = "buttons"
        HeldData.nameOfTheSoftwareBind = args[0][0]
        HeldData.whoHasItCurrentlyBinded = args[0][1]
        HeldData.whoHasItCurrentlyBinded = args[0][2]
        BinderSelector_Screens.SetCaller(ButtonMenu_Screens, "ButtonMenu")
        BinderSelector_Screens.SetExiter(ButtonMenu_Screens, "ButtonMenu")
        BinderSelector_Screens.Call()
        Debug.End()
# ------------------------------------------------------------------------
class AxisMenu(Screen):
    """
        AxisMenu:
        ---------
        This class handles the screen of the account menu which shows
        to the user some actions that they can do with their user profiles
    """
    #region   --------------------------- MEMBERS
    ToolBar:AppNavigationBar = None
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("ControlMenu -> __init__")
        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
        """
        Debug.Start("AxisMenu -> on_pre_enter")
        KontrolRGB.FastLoadingAnimation()
        self.padding = 0
        self.spacing = 0

        #region ---- Background
        import os
        from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
        from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
        path = os.getcwd()

        background = GetBackgroundImage(AppendPath(path, "/Libraries/Backgrounds/Menus/Dark.png"),
                                        AppendPath(path, "/Libraries/Backgrounds/Menus/Light.png"))
        #endregion

        #region ---------------------------- Layouts
        self.Layout = MDFloatLayout()
        # Add widgets
        self.add_widget(background)
        #endregion
        #region ---------------------------- ToolBar
        self.ToolBar = AppNavigationBar(pageTitle=_("Controls & Keybinds"))
        #endregion

        self.create_layouts()
        HeldData.whatIsBeingBinded = "axes"

        self.Layout.add_widget(self.ToolBar.ToolBar)
        self.Layout.add_widget(self.ToolBar.NavDrawer)
        self.add_widget(self.Layout)
        Debug.End()
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            Function called when the screen is fully entered in view.
            In this case, once the view is fully loaded, the cards
            will slowly elevate to the wanted value.
        """
        Debug.Start("AxisMenu -> on_enter")
        KontrolRGB.DisplayDefaultColor()
        Debug.End()
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            Function called before the screen is fully left. This gives
            us time to animate the screen leaving before destroying the
            objects and instances it created.
        """
        Debug.Start("AxisMenu -> on_pre_leave")
        Debug.End()
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully out of view.
        """
        Debug.Start("AxisMenu -> on_leave")
        Debug.Log("Attempting to remove self from AppManager's widgets")
        self.clear_widgets()
        AppManager.manager.remove_widget(self)
        Debug.End()
        self.clear_widgets()
# ------------------------------------------------------------------------
    def create_layouts(self,*args):
        Debug.Start("create_layouts")
        self.create_recycle_view()
        Debug.End()
# ------------------------------------------------------------------------
    def create_recycle_view(self):
        Debug.Start("create_recycle_view")
        self.RecyleBoxLayout = RecycleGridLayout(default_size=(None,72),
                                                default_size_hint=(1, None),
                                                size_hint=(1, None),
                                                orientation='lr-tb')
        self.RecyleBoxLayout.padding = 25
        self.RecyleBoxLayout.spacing = 5
        self.RecyleBoxLayout.cols = 1
        # self.RecyleBoxLayout.orientation
        self.RecyleBoxLayout.bind(minimum_height=self.RecyleBoxLayout.setter("height"))

        amountOfCard = len(ControlsCardData.dataList)
        Debug.Log(f"There is {amountOfCard} cards to display")

        self.recycleView = RecycleView()
        self.recycleView.pos_hint = {"center_x" : 0.5, "center_y" : 0.40}
        self.recycleView.size_hint = (1,0.80)
        self.recycleView.add_widget(self.RecyleBoxLayout)
        self.recycleView.viewclass = CustomThreeLineIconListItem
        self.Layout.add_widget(self.recycleView)

        for name,dictionary in Controls._axes.items():

            theFuckerThatBindedIt = dictionary["bindedTo"]
            whatItBindedItAs = dictionary["bindedAs"]

            if(theFuckerThatBindedIt == None):
                secondaryText = _("Available")
                tertiaryText = ""
            else:
                secondaryText =  _("binded to: ") + theFuckerThatBindedIt
                tertiaryText = _("binded as: ") + whatItBindedItAs

            self.recycleView.data.insert(0,
                                         {
                                             "text" : name,
                                             "secondary_text" : secondaryText,
                                             "tertiary_text" : tertiaryText,
                                             "halign" : "left",
                                             "on_release" : (lambda x: lambda: self.ButtonPressed(x))([name, theFuckerThatBindedIt, whatItBindedItAs])
                                         })
        Debug.End()
# ------------------------------------------------------------------------
    def ButtonPressed(self, *args):
        """
            ButtonPressed:
            ==============
            Summary:
            --------
            Callback function executed when an axis is
            pressed.
        """
        Debug.Start("ButtonPressed")

        Debug.Log(args)
        
        HeldData.whatIsBeingBinded = "axes"
        HeldData.nameOfTheSoftwareBind = args[0][0]
        HeldData.whoHasItCurrentlyBinded = args[0][1]
        HeldData.whoHasItCurrentlyBinded = args[0][2]

        BinderSelector_Screens.SetCaller(AxisMenu_Screens, "AxisMenu")
        BinderSelector_Screens.SetExiter(AxisMenu_Screens, "AxisMenu")
        BinderSelector_Screens.Call()
        Debug.End()
# ------------------------------------------------------------------------
class BinderSelectorMenu(Screen):
    """
        BinderSelectorMenu:
        -----------
        Displays who can bind their hardware functions
        to that hardware control.
    """
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("ControlMenu -> __init__")
        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
        """
        Debug.Start("BinderSelectorMenu -> on_pre_enter")
        KontrolRGB.FastLoadingAnimation()
        self.padding = 0
        self.spacing = 0

        #region ---- Background
        import os
        from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
        from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
        path = os.getcwd()

        background = GetBackgroundImage(AppendPath(path, "/Libraries/Backgrounds/Menus/Dark.png"),
                                        AppendPath(path, "/Libraries/Backgrounds/Menus/Light.png"))
        #endregion

        self.TopLayout = MDBoxLayout(padding=("20sp","20sp","20sp","20sp"), size_hint_y = 0.25, pos_hint = {"center_x" : 0.5, "center_y" : 0.90})
        self.Previous = MDIconButton(text="chevron-left", icon="chevron-left")
        self.Previous.icon_size = "75sp"
        self.Previous.pos_hint={"center_x": 0.25, "center_y": 0.5}
        self.Previous.on_release = self.GoToPrevious

        # Page title
        self.PageTitle = MDLabel(text=_("Select a binder"),
                                    font_style = "H2",
                                    halign = "center")

        # Top layout widgets
        self.TopLayout.add_widget(self.Previous)
        self.TopLayout.add_widget(self.PageTitle)


        #region ---------------------------- Layouts
        self.Layout = MDFloatLayout()
        self.Layout.add_widget(self.TopLayout)
        # Add widgets
        self.add_widget(background)
        #endregion

        #region ----------------------------- Swiper
        self.SwiperLayout = MDSwiper()
        self.SwiperLayout.items_spacing = 35

        #region ---------------------------- Cards
        if(HeldData.whatIsBeingBinded == "axes"):
            Debug.Log("Listing addon's hardware axes")
            for addonName, addonData in Addons._listedAddons.items():
                Debug.Log(f"it is {addonData[AddonEnum.information][AddonEnum.Information.isCompatible]} that {addonData[AddonEnum.information][AddonEnum.Information.name]} is compatible and it is {addonData[AddonEnum.information][AddonEnum.Information.hasHardwareAxes]} that it has axes to bind.")
                if(addonData[AddonEnum.information][AddonEnum.Information.hasHardwareAxes] and addonData[AddonEnum.information][AddonEnum.Information.isCompatible]):
                    swiperLayout = MDSwiperItem()
                    swiperLayout.padding = 40
                    card = WidgetCard(icon=addonData[AddonEnum.information][AddonEnum.Information.MDIcon], name=addonName)
                    card.PressedEnd = self.BinderCardPressed
                    swiperLayout.add_widget(card)
                    self.SwiperLayout.add_widget(swiperLayout)
        else:
            Debug.Log("Listing addon's hardware buttons")
            for addonName, addonData in Addons._listedAddons.items():
                if(addonData[AddonEnum.information][AddonEnum.Information.hasHardwareButtons] and addonData[AddonEnum.information][AddonEnum.Information.isCompatible]):
                    swiperLayout = MDSwiperItem()
                    swiperLayout.padding = 40
                    card = WidgetCard(icon=addonData[AddonEnum.information][AddonEnum.Information.MDIcon], name=addonName)
                    card.PressedEnd = self.BinderCardPressed
                    swiperLayout.add_widget(card)
                    self.SwiperLayout.add_widget(swiperLayout)
        #endregion
        #endregion

        self.Layout.add_widget(self.SwiperLayout)
        self.add_widget(self.Layout)
        Debug.End()
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            Function called when the screen is fully entered in view.
            In this case, once the view is fully loaded, the cards
            will slowly elevate to the wanted value.
        """
        Debug.Start("ControlMenu -> on_enter")
        KontrolRGB.DisplayDefaultColor()
        Debug.End()
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            Function called before the screen is fully left. This gives
            us time to animate the screen leaving before destroying the
            objects and instances it created.
        """
        Debug.Start("ControlMenu -> on_pre_leave")
        Debug.End()
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully out of view.
        """
        Debug.Start("ControlMenu -> on_leave")
        Debug.Log("Attempting to remove self from AppManager's widgets")
        self.clear_widgets()
        AppManager.manager.remove_widget(self)
        Debug.End()
        self.clear_widgets()
# ------------------------------------------------------------------------
    def GoToPrevious(self, *args):
        """
            GoToPrevious:
            =============
            Summary:
            --------
            Returns to the previous screen being either
            buttons or axes selection.
        """
        Debug.Start("GoToPrevious")
        BinderSelector_Screens._Exit()
        Debug.End()
# ------------------------------------------------------------------------
    def BinderCardPressed(self, *args):
        """
            BinderCardPressed:
            ==================
            Summary:
            --------
            Callback method called when an Addon card is pressed.
            It takes the user to the next screen, which allows
            them to see each hardware or actions that they can
            bind with that.
        """
        Debug.Start("BinderCardPressed")
        card:WidgetCard = args[0]
        HeldData.whoIsTryingToBindIt = card.Name.text

        BindSelectMenu_Screens.SetCaller(BinderSelector_Screens, "BinderSelectorMenu")
        BindSelectMenu_Screens.SetExiter(BinderSelector_Screens, "BinderSelectorMenu")
        BindSelectMenu_Screens.Call()
        Debug.Log(args)
        Debug.End()
# ------------------------------------------------------------------------
class BindSelectMenu(Screen):
    """
        BindSelectMenu:
        ===============
        This class handles the screen of the account menu which shows
        to the user some actions that they can do with their user profiles
    """
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- CONSTRUCTOR
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Debug.Start("ControlMenu -> __init__")
        Debug.End()
        #endregion
# ------------------------------------------------------------------------
    def on_pre_enter(self, *args):
        """
        """
        Debug.Start("BindSelectMenu -> on_pre_enter")
        KontrolRGB.FastLoadingAnimation()
        self.padding = 0
        self.spacing = 0

        #region ---- Background
        import os
        from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.Application_Themes import GetBackgroundImage
        from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
        path = os.getcwd()

        background = GetBackgroundImage(AppendPath(path, "/Libraries/Backgrounds/PopUps/Dark.png"),
                                        AppendPath(path, "/Libraries/Backgrounds/PopUps/Light.png"))
        #endregion

        self.TopLayout = MDBoxLayout(padding=("20sp","20sp","20sp","20sp"), size_hint_y = 0.25, pos_hint = {"center_x" : 0.5, "center_y" : 0.90})
        self.Previous = MDIconButton(text="chevron-left", icon="chevron-left")
        self.Previous.icon_size = "75sp"
        self.Previous.pos_hint={"center_x": 0.25, "center_y": 0.5}
        self.Previous.on_release = self.GoToPrevious

        # Page title
        self.PageTitle = MDLabel(text=_("Select a new binder for: ") + HeldData.nameOfTheSoftwareBind,
                                    font_style = "H4",
                                    halign = "center")

        # Top layout widgets
        self.TopLayout.add_widget(self.Previous)
        self.TopLayout.add_widget(self.PageTitle)

        #region ---------------------------- Layouts
        self.Layout = MDFloatLayout()
        # Add widgets
        self.add_widget(background)
        #endregion
        #region ---------------------------- ToolBar
        #endregion

        self.Layout.add_widget(self.TopLayout)
        self.create_layouts()
        self.add_widget(self.Layout)
        Debug.End()
# ------------------------------------------------------------------------
    def on_enter(self, *args):
        """
            Function called when the screen is fully entered in view.
            In this case, once the view is fully loaded, the cards
            will slowly elevate to the wanted value.
        """
        Debug.Start("BindSelectMenu -> on_enter")
        KontrolRGB.DisplayDefaultColor()
        Clock.schedule_once(self.UpdateShownValues, 1)
        Debug.End()
# ------------------------------------------------------------------------
    def on_pre_leave(self, *args):
        """
            Function called before the screen is fully left. This gives
            us time to animate the screen leaving before destroying the
            objects and instances it created.
        """
        Debug.Start("BindSelectMenu -> on_pre_leave")
        Debug.End()
# ------------------------------------------------------------------------
    def on_leave(self, *args):
        """
            Function called when the screen is fully out of view.
        """
        Debug.Start("BindSelectMenu -> on_leave")
        Debug.Log("Attempting to remove self from AppManager's widgets")
        self.clear_widgets()
        AppManager.manager.remove_widget(self)
        Debug.End()
        self.clear_widgets()
# ------------------------------------------------------------------------
    def create_layouts(self,*args):
        Debug.Start("create_layouts")
        self.create_recycle_view()
        Debug.End()
# ------------------------------------------------------------------------
    def create_recycle_view(self):
        Debug.Start("create_recycle_view")
        self.RecyleBoxLayout = RecycleGridLayout(default_size=(None,72),
                                                default_size_hint=(1, None),
                                                size_hint=(1, None),
                                                orientation='lr-tb')
        self.RecyleBoxLayout.padding = 25
        self.RecyleBoxLayout.spacing = 5
        self.RecyleBoxLayout.cols = 1
        # self.RecyleBoxLayout.orientation
        self.RecyleBoxLayout.bind(minimum_height=self.RecyleBoxLayout.setter("height"))

        self.recycleView = RecycleView()
        self.recycleView.pos_hint = {"center_x" : 0.5, "center_y" : 0.35}
        self.recycleView.size_hint = (1,0.75)
        self.recycleView.add_widget(self.RecyleBoxLayout)
        self.recycleView.viewclass = ThreeLineListItem
        self.Layout.add_widget(self.recycleView)

        Debug.Log(f"Getting hardware controls from {HeldData.whoIsTryingToBindIt}")
        hardwareData = Addons._listedAddons[HeldData.whoIsTryingToBindIt][AddonEnum.GetAllHardwareControls]()
        for name,dictionary in hardwareData[HeldData.whatIsBeingBinded].items():

            try:
                currentValue = dictionary["getter"]()
                currentValue = str(currentValue)
                currentValue = _("value: ") + currentValue
            except:
                currentValue = "GETTER ERROR"

            if(dictionary["binded"] == True):
                secondaryText:str = _("Binded to: ") + dictionary["bindedTo"]
            else:
                secondaryText:str = _("Available")

            self.recycleView.data.insert(0,
                                         {
                                             "text" : name,
                                             "secondary_text" : secondaryText,
                                             "tertiary_text" : currentValue,
                                             "halign" : "left",
                                             "on_release" : (lambda x: lambda: self.ButtonPressed(x))([name])
                                         })
        Debug.End()
# ------------------------------------------------------------------------
    def ButtonPressed(self, *args):
        """
            ButtonPressed:
            ==============
            Summary:
            --------
            Callback function executed when a button is
            pressed.
        """
        Debug.Start("ButtonPressed")
        hardwareName = args[0][0]

        PopUps_Screens.SetCaller(BindSelectMenu_Screens, "BindSelectMenu")
        PopUps_Screens.SetExiter(ControlMenu_Screens, "ControlMenu")
        PopUpsHandler.Clear()

        Debug.enableConsole = True

        Debug.Log(f"Unbinding {HeldData.nameOfTheSoftwareBind} from {HeldData.whoHasItCurrentlyBinded}")
        if(HeldData.whatIsBeingBinded == "axes"):
            Addons.UnbindHardwareAxisFromEveryone(HeldData.nameOfTheSoftwareBind)
            Debug.Log(f"Binding {HeldData.whoIsTryingToBindIt}'s {hardwareName} to {HeldData.nameOfTheSoftwareBind}")
            result = Addons.BindHardwareAxis(HeldData.whoIsTryingToBindIt, HeldData.nameOfTheSoftwareBind, hardwareName)
        else:
            Addons.UnbindHardwareButtonFromEveryone(HeldData.nameOfTheSoftwareBind)
            result = Addons.BindHardwareButton(HeldData.whoIsTryingToBindIt, HeldData.nameOfTheSoftwareBind, hardwareName)

        if(result != Execution.Passed):
            Debug.Log(f"Some errors occured when trying to bind {HeldData.whoIsTryingToBindIt}'s {hardwareName} {HeldData.whatIsBeingBinded} to {HeldData.nameOfTheSoftwareBind}")
            PopUpsHandler.Add(PopUpTypeEnum.FatalError,
                              Message=_("Kontrol failed to bind the specified addon's hardware with the specified software representation. ") + _("Addon") + ": " + HeldData.whoIsTryingToBindIt + " " + _("Software") + ": " + HeldData.nameOfTheSoftwareBind + " " + _("Hardware") + ": " + hardwareName,
                              )
        else:
            Debug.Log(f"Successfully binded {HeldData.whoIsTryingToBindIt}'s {hardwareName} {HeldData.whatIsBeingBinded} to {HeldData.nameOfTheSoftwareBind}")
            PopUpsHandler.Add(PopUpTypeEnum.Remark,
                              Message=_("Successfully binded the specified addon's hardware with a new software representation. Kontrol automatically removed other hardware's binds associated with this software representation.")
                              )

        Debug.enableConsole = False
        PopUps_Screens.Call()
        Debug.End()
# ------------------------------------------------------------------------
    def GoToPrevious(self, *args):
        """
            GoToPrevious:
            =============
            Summary:
            --------
            returns to the binder selector screen.
        """
        Debug.Start("GoToPrevious")
        BinderSelector_Screens.Call()
        Debug.End
# ------------------------------------------------------------------------
    def _GoToErrorPopUp(self, *args):
        """
            _GoToErrorPopUp:
            ============
            Summary:
            --------
            Goes to the error pop up displayed
            when something fucks up. Like an addon
            stopping randomly in the middle of bindings.
        """
        Debug.Start("_GoToErrorPopUp")

        PopUpsHandler.Add(PopUpTypeEnum.FatalError, Message=_("A critical error occured while attempting to bind or update binder values. Maybe the driver stopped?"))
        PopUps_Screens.SetCaller(ControlMenu_Screens, "ControlMenu")
        PopUps_Screens.SetExiter(ControlMenu_Screens, "ControlMenu")
        PopUps_Screens.Call()
        Debug.End()
# ------------------------------------------------------------------------
    def UpdateShownValues(self, *args):
        """
            UpdateShownValues:
            ==================
            Summary:
            --------
            This method updates the third text
            shown in each of the ThreeLinesIconWidget
            displayed in the binder.
        """
        Debug.Start("UpdateShownValues")

        if(AppManager.manager.current == "BindSelectMenu"):
            Debug.Log(f"Getting hardware controls from {HeldData.whoIsTryingToBindIt}")
            hardwareData = Addons._listedAddons[HeldData.whoIsTryingToBindIt][AddonEnum.GetAllHardwareControls]()

            if(hardwareData == Execution.Failed):
                Debug.Error("Failed to get hardware data")
                self._GoToErrorPopUp()
                Debug.End()
                return

            if(hardwareData == Execution.Incompatibility):
                Debug.Error("Failed to get hardware data")
                self._GoToErrorPopUp()
                Debug.End()
                return

            if(hardwareData == Execution.Crashed):
                Debug.Error("Failed to get hardware data")
                self._GoToErrorPopUp()
                Debug.End()
                return

            if(hardwareData == Execution.Unecessary):
                Debug.Error("Failed to get hardware data")
                self._GoToErrorPopUp()
                Debug.End()
                return

            if(hardwareData == Execution.Passed):
                Debug.Error("Failed to get hardware data")
                self._GoToErrorPopUp()
                Debug.End()
                return

            if(hardwareData == Execution.ByPassed):
                Debug.Error("Failed to get hardware data")
                self._GoToErrorPopUp()
                Debug.End()
                return

            self.recycleView.data = []

            for name,dictionary in hardwareData[HeldData.whatIsBeingBinded].items():

                try:
                    currentValue = dictionary["getter"]()
                    currentValue = str(currentValue)
                    currentValue = _("value: ") + currentValue
                except:
                    currentValue = "GETTER ERROR"

                if(dictionary["binded"] == True):
                    secondaryText:str = _("Binded to: ") + dictionary["bindedTo"]
                else:
                    secondaryText:str = _("Available")

                self.recycleView.data.insert(0,
                                            {
                                                "text" : name,
                                                "secondary_text" : secondaryText,
                                                "tertiary_text" : currentValue,
                                                "halign" : "left",
                                                "on_release" : (lambda x: lambda: self.ButtonPressed(x))([name])
                                            })
            Clock.schedule_once(self.UpdateShownValues, 3)
            self.recycleView.refresh_from_data()
        else:
            Debug.Warn("Stopping value updates.")
        Debug.End()
LoadingLog.End("ControlMenu.py")