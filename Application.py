#====================================================================#
# File Information
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Programs.Local.Hardware.RGB import KontrolRGB
LoadingLog.Start("Application.py")
#===================================================================#
# Imports
#===================================================================#
LoadingLog.Import("Python")
import os

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
from Libraries.BRS_Python_Libraries.BRS.Network.WiFi.WiFi import WiFiStatusUpdater
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
from Programs.Local.Hardware.RGB import KontrolRGB
# from Programs.Pages.WiFiLogin import WiFiConnecting_Screens, WiFiLogin_Screens
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


    def SetDefaultTheme(self):
        """
            SetDefaultTheme:
            ================
            Summary:
            --------
            This function sets the default theme
            that the application will have before
            cache is loaded in. This function is
            called in :ref:`build` automatically.
        """
        Debug.Start("SetDefaultTheme")
        self.theme_cls.material_style = 'M3'
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.accent_palette = "Yellow"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.theme_style_switch_animation = False
        self.theme_cls.theme_style_switch_animation_duration = 0
        Debug.End()

    def SetDefaultLanguage(self):
        """
            SetDefaultLanguage:
            ===================
            Summary:
            --------
            This function initializes the
            :ref:`AppLanguage` class. It defaults
            the language of the application to
            US_English until the cache is initialized.
            This function is called automatically in
            :ref:`build`
        """
        Debug.Start("SetDefaultLanguage")

        # Load available languages
        Debug.Log("Initializing AppLanguage. Defaulting to US_English")
        path = AppendPath(os.getcwd(), "/Local/Languages/locale")
        AppLanguage.__init__(AppLanguage, path, "US_English")

        # Set default AppInfo informations
        Debug.Log("Setting Information")

        if(AppLanguage.Current == None):
            Debug.Warn("Your application cannot use languages")
            Information.CanUse.Languages = False
        else:
            Information.CanUse.Languages = True
        Debug.End()

    def SetKivyConfig(self):
        """
            SetKivyConfig:
            ==============
            Summary:
            --------
            This function's purpose is
            to set the default application
            kivy settings in the Config before
            the application is fully loaded in.
            Such configurations can be wether the
            mouse is displayed or not.
        """
        Debug.Start("SetKivyConfig")

        if(Information.platform == "Linux"):
            Debug.Log("Turning off cursor")
            Window.show_cursor = False
            Debug.enableConsole = False
            Debug.Log("Turning off aliasing")
            Config.set("graphics", "multisamples", 0)
            Config.write()
            Debug.End()
            return

        if(Information.platform == "Windows"):
            Window.show_cursor = True
            Debug.End()
            return

        Debug.End()

    def StartGlobalThreads(self):
        """
            StartGlobalThreads:
            ===================
            Summary:
            --------
            Starts the threads of multiple
            background processes used to
            constantly show up to date informations
            such as if your device can access the
            internet or if your device can use RGB
            lights and so on.
        """
        Debug.Start("StartGlobalThreads")

        Debug.Log("Starting slow network information updater")
        WiFiStatusUpdater.StartUpdating()

        Debug.Log("Trying to start RGB class.")
        KontrolRGB.Initialize()

        Debug.End()

    def LoadSavedCache(self):
        """
            LoadSavedCache:
            ===============
            Summary:
            --------
            Initializes the saved cache
            of your application. This needs
            to be called AFTER the following:
            - :ref:`SetDefaultTheme`
            - :ref:`SetDefaultLanguage`
            - :ref:`SetKivyConfig`
        """
        Debug.Start("LoadSavedCache")

        if(Cache.Load()):
            Debug.Error("Failed to load the application's cache")
        else:
            Debug.Log("CACHE LOAD SUCCESS")

        Debug.End()

    def ConfigureAndLoadStartScreen(self):
        """
            ConfigureAndLoadStartScreen:
            ============================
            Summary:
            --------
            This function configures the
            _Screens classes of the following
            transitional screens:
            - :ref:`Startup_Screens`
            - :ref:`AppLoading_Screens`
            - :ref:`PopUps_Screens`

            It then calls the Call function of :ref:`Startup_Screens`
            so that Kontrol can launch. This needs to be the last
            function in :ref:`build` right before the return statement.
        """
        Debug.Start("ConfigureAndLoadStartScreen")

        # Create screen manager
        Debug.Log("Creating ScreenManager()")
        AppManager.manager = ScreenManager()

        AppLoading_Screens.SetExiter(PopUps_Screens, "PopUps")
        AppLoading_Screens.SetCaller(Startup_Screens, "Startup")

        PopUps_Screens.SetExiter(ProfileMenu, "ProfileMenu")
        PopUps_Screens.SetCaller(AppLoading_Screens, "AppLoading")

        Startup_Screens.SetExiter(AppLoading_Screens, "AppLoading")
        Startup_Screens.SetCaller(Application, "Application")
        Startup_Screens.Call()

        Debug.End()

    def ConfigureWindowAttributes(self):
        """
            ConfigureWindowAttributes:
            ==========================
            Summary:
            --------
            Sets the default values of
            Kivy's :ref:`Window` class
            such as if it's border less,
            in full screen etc.
        """
        Debug.Start("SetWindowInformations")

        #Window.borderless = True
        #Window.resizable = True
        #Window.left = -1024
        #Window.top = 600
        #Window.fullscreen = False
        Window.size = (720, 576)
        Debug.End()

    LoadingLog.Method("build")
    def build(self):
        """
            build:
            ======
            Summary:
            --------
            This creates the Screen manager, which is stored inside of the global AppManager class.
            After which, all the screens the application uses are added as widgets to the manager.
            They each have a name unique to them.

            The build function is execute when the application launches.
            It creates language handlers, cache handlers or any other handler necessary
            for Kontrol to function properly.
        """
        Debug.enableConsole = False
        Debug.Start("build")

        self.SetKivyConfig()
        self.SetDefaultTheme()
        self.SetDefaultLanguage()

        self.ConfigureWindowAttributes()
        self.LoadSavedCache()
        self.StartGlobalThreads()
        self.ConfigureAndLoadStartScreen()

        Debug.End()
        return AppManager.manager

    LoadingLog.Method("on_start")
    def on_start(self):
        print("Application built... starting")

    LoadingLog.Method("on_stop")
    def on_pre_stop(self):
        Debug.Start("Application -> on_stop")
        if(Cache.loaded):
            try:
                Cache.GetAppInfo()
                Cache.SetExit("User")
                Cache.SetDate("Exit")
                Cache.SaveFile()
            except:
                Debug.Warn("Cache failed to save on_stop. This might be normal tho.")
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

# Debug.Log("KILLING PYTHON PROCESS")
# KillPython()
Shutdown.Kontrol()

LoadingLog.End("Application.py")