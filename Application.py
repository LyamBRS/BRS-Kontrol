#====================================================================#
# File Information
#====================================================================#
import os
import sys
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("Application.py")

path = os.getcwd()
BRSpath = path + "\Libraries\BRS_Python_Libraries\BRS"

# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1,path)
sys.path.insert(2,BRSpath)
#====================================================================#
# Imports
#====================================================================#
from kivy.core.window import Window
# -------------------------------------------------------------------
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, CardTransition
from kivymd.theming import ThemeManager
from Programs.Local.FileHandler.Cache import Cache
# -------------------------------------------------------------------

# -------------------------------------------------------------------
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.font import Font
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import AppLanguage
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
# -------------------------------------------------------------------
from Programs.Pages.ProfileMenu import ProfileMenu
from Programs.Pages.Startup import Startup_Screens
from Programs.Pages.AppLoading import AppLoading,AppLoading_Screens
from Programs.Pages.PopUps import PopUps,PopUps_Screens,PopUpsHandler,Keys,PopUpTypeEnum
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

#====================================================================#
# Classes
#====================================================================#
# ------------------------------------------------------------------------
class Application(MDApp):

    # theme_cls = ThemeManager()

    def build(self):
        """
            This creates the Screen manager, which is stored inside of the global AppManager class.
            After which, all the screens the application uses are added as widgets to the manager.
            They each have a name unique to them.

            Last, the current screen is set as one of them.
        """
        Debug.enableConsole = True

        self.theme_cls.material_style = 'M3'
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.accent_palette = "Yellow"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0

        # Load available languages
        AppLanguage.__init__(AppLanguage, os.getcwd() + "\\Local\\Languages\\locale", "US_English")

        # Window.borderless = True
        # Window.resizable = True
        # Window.left = -1024
        # Window.top = 600
        # Window.fullscreen = 'auto'

        AppManager.manager = ScreenManager()
        # AppManager.manager.transition.duration = 0.5
        # AppManager.manager.add_widget(ProfileMenu(name="ProfileMenu"))
        # AppManager.manager.current = "ProfileMenu"

        if(Cache.Load()):
            Debug.Error("Failed to load the application's cache")
        else:
            Debug.Log("CACHE LOAD SUCCESS")

        #Temporary pop up test
        PopUpsHandler.Add(PopUpTypeEnum.Question, "help", "This is the question pop up. Among us among us", True)
        PopUpsHandler.Add(PopUpTypeEnum.FatalError, "alert-octagon", "This is the Fatal Error pop up.", True)
        PopUpsHandler.Add(PopUpTypeEnum.Remark, "black-mesa", "This is the remark pop up. it's very basic", True)
        PopUpsHandler.Add(PopUpTypeEnum.Warning, "alert", "Where's my money, bitch?! I ain't gonna keep asking nice. Yo, alright? I want my money and my dope. Come on! What, what! What do you wanna say? Shut up! Shut... up! \nWhat business? The business you put me on, asshole! What, you already forgot? THIS business. Huh? That uh jog your memory, son of a bitch? Hey, you said... you said handle it, so you know what, I handled it. Didn't mean to kill somebody? Well, too late you know cause, dude's dead. Way dead. Oh, and hey, hey. Here's your money. Yeah, forty-six hundred and sixty bucks. Your half. Spend it in good health, you miserable son of bitch. \nI didn't say I killed him. Dude's wife crushed his head with an ATM machine. Crushed his head... with an ATM machine... right in front of me. I mean, crushed it like... Oh my god, the sound... it's still in my ears. You know and the the blood, like everywhere. Like there was so much you would not believe.", True)

        AppLoading_Screens.SetExiter(PopUps, "PopUps")
        Startup_Screens.SetExiter(AppLoading, "AppLoading")
        Startup_Screens.SetCaller(Application, "Application")
        Startup_Screens.Call()
        return AppManager.manager
    
    def on_start(self):
        print("Application built... starting")

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

LoadingLog.End("Application.py")