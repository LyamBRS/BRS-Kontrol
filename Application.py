#====================================================================#
# File Information
#====================================================================#
import os
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Libraries.BRS_Python_Libraries.BRS.Network.WiFi.WiFi import WiFiStatusUpdater
from Libraries.BRS_Python_Libraries.BRS.Utilities.pythonKiller import KillPython
from Programs.Local.Hardware.RGB import KontrolRGB
LoadingLog.Start("Application.py")
#===================================================================#
# Imports
#===================================================================#
LoadingLog.Import("Kivy")
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager
# -------------------------------------------------------------------
LoadingLog.Import("KivyMD")
from kivymd.app import MDApp
# -------------------------------------------------------------------
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.font import Font
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import AppLanguage
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
from Libraries.BRS_Python_Libraries.BRS.Utilities.addons import Addons
# -------------------------------------------------------------------
LoadingLog.Import("Local")
from Programs.Local.FileHandler.Cache import Cache
from Programs.Pages.ProfileMenu import ProfileMenu
from Programs.Pages.Startup import Startup_Screens
from Programs.Pages.AppLoading import AppLoading_Screens
from Programs.Pages.PopUps import PopUps_Screens
from Programs.Local.Updating.LaunchHandling import Shutdown

from Programs.Pages.WiFiLogin import WiFiConnecting_Screens, WiFiLogin_Screens
#====================================================================#
# Configuration
#====================================================================#
# region -- Font
ButtonFont = Font()
ButtonFont.isBold = True
ButtonFont.size = "32sp"
# endregion
#====================================================================#
# Functions
#====================================================================#
# To change the kivy default settings
# we use this module config
from kivy.config import Config

# 0 being off 1 being on as in true / false


# you can use 0 or 1 && True or False
# Config.set('graphics', 'resizable', '0')

# fix the width of the window
# Config.set('graphics', 'width', '720')
# Config. set('graphics', 'height', '576')
#====================================================================#
# Classes
#====================================================================#
# ------------------------------------------------------------------------
LoadingLog.Class("Application")
class Application(MDApp):

    # theme_cls = ThemeManager()
    LoadingLog.Method("build")
    def build(self):
        """
            This creates the Screen manager, which is stored inside of the global AppManager class.
            After which, all the screens the application uses are added as widgets to the manager.
            They each have a name unique to them.

            Last, the current screen is set as one of them.
        """
        Debug.enableConsole = True
        Debug.Start("build")

        Debug.Log("Turning off cursor")
        Window.show_cursor = False

        Debug.Log("Turning off aliasing")
        Config.set("graphics", "multisamples", 0)
        Config.write()

        Debug.Log("Setting default application's theme.")
        self.theme_cls.material_style = 'M3'
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.accent_palette = "Yellow"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0

        # Load available languages
        Debug.Log("Initializing AppLanguage. Defaulting to US_English")
        path = AppendPath(os.getcwd(), "/Local/Languages/locale")
        AppLanguage.__init__(AppLanguage, path, "US_English")

        # Set default AppInfo informations
        Debug.Log("Setting Information")

        if(AppLanguage.Current == None):
            Information.CanUse.Languages = False
        else:
            Information.CanUse.Languages = True

        # Set window to 3rd monitor.
        Debug.Log("Configuring window size and attributes")
        #Window.borderless = True
        #Window.resizable = True
        #Window.left = -1024
        #Window.top = 600
        #Window.fullscreen = False
        Window.size = (720, 576)

        # Create screen manager
        Debug.Log("Creating ScreenManager()")
        AppManager.manager = ScreenManager()

        # Load the cache
        Debug.Log("Loading the cache.")
        if(Cache.Load()):
            Debug.Error("Failed to load the application's cache")
        else:
            Debug.Log("CACHE LOAD SUCCESS")

        Debug.Log("Starting slow network information updater")
        WiFiStatusUpdater.StartUpdating()

        #Temporary pop up test
        # PopUpsHandler.Add(PopUpTypeEnum.Question, "help", "This is the question pop up. Among us among us", True)
        # PopUpsHandler.Add(PopUpTypeEnum.FatalError, "alert-octagon", "This is the Fatal Error pop up.", True)
        # PopUpsHandler.Add(PopUpTypeEnum.Remark, "bug", "This is a debugging pop up. It exist solely because without at least 1 pop up, the application would softlock.", True)
        # PopUpsHandler.Add(PopUpTypeEnum.Warning, "alert", "Where's my money, bitch?! I ain't gonna keep asking nice. Yo, alright? I want my money and my dope. Come on! What, what! What do you wanna say? Shut up! Shut... up! \nWhat business? The business you put me on, asshole! What, you already forgot? THIS business. Huh? That uh jog your memory, son of a bitch? Hey, you said... you said handle it, so you know what, I handled it. Didn't mean to kill somebody? Well, too late you know cause, dude's dead. Way dead. Oh, and hey, hey. Here's your money. Yeah, forty-six hundred and sixty bucks. Your half. Spend it in good health, you miserable son of bitch. \nI didn't say I killed him. Dude's wife crushed his head with an ATM machine. Crushed his head... with an ATM machine... right in front of me. I mean, crushed it like... Oh my god, the sound... it's still in my ears. You know and the the blood, like everywhere. Like there was so much you would not believe.", True)

        Debug.Log("Trying to start RGB class.")
        KontrolRGB.Initialize()

        Debug.Log("Setting transistion screen's callers and exiters.")
        AppLoading_Screens.SetExiter(PopUps_Screens, "PopUps")
        AppLoading_Screens.SetCaller(Startup_Screens, "Startup")

        PopUps_Screens.SetExiter(ProfileMenu, "ProfileMenu")
        PopUps_Screens.SetCaller(AppLoading_Screens, "AppLoading")

        Startup_Screens.SetExiter(AppLoading_Screens, "AppLoading")
        Startup_Screens.SetCaller(Application, "Application")

        Debug.Log("Calling startup screen")
        Startup_Screens.Call()
        # WiFiLogin_Screens.Call()
        Debug.End()
        return AppManager.manager

    LoadingLog.Method("on_start")
    def on_start(self):
        print("Application built... starting")

    LoadingLog.Method("on_stop")
    def on_stop(self):
        Debug.Start("Application -> on_stop")
        if(Cache.loaded):
            Cache.GetAppInfo()
            Cache.SetExit("User")
            Cache.SetDate("Exit")
            Cache.SaveFile()
        Debug.End()
# ------------------------------------------------------------------------
# try:
Application().run()
# except:
    # if(Cache.loaded):
        # Cache.SetExit("Crashed")
        # Cache.SetDate("Exit")
        # Cache.SaveFile()

Shutdown.ShutdownFunction()
KontrolRGB.Uninitialize()
Addons.StopAll()
WiFiStatusUpdater.StopUpdating()

Debug.Log("KILLING PYTHON PROCESS")
KillPython()

LoadingLog.End("Application.py")