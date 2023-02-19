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
# -------------------------------------------------------------------

# -------------------------------------------------------------------
from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.font import Font
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import AppLanguage
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
# -------------------------------------------------------------------
from Programs.Pages.ProfileMenu import ProfileMenu
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
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0

        # Load available languages
        AppLanguage.__init__(AppLanguage, os.getcwd() + "\\Local\\Languages\\locale", "CAN_French")

        Window.borderless = True
        Window.resizable = True
        Window.left = -1024
        Window.top = 600
        Window.fullscreen = 'auto'

        AppManager.manager = ScreenManager()
        AppManager.manager.transition.duration = 0.5
        AppManager.manager.add_widget(ProfileMenu(name="ProfileMenu"))
        AppManager.manager.current = "ProfileMenu"
        return AppManager.manager
    
    def on_start(self):
        print("Application built... starting")

# ------------------------------------------------------------------------

Application().run()
LoadingLog.End("Application.py")