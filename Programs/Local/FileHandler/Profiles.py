#====================================================================#
# File Information
#====================================================================#
""" Handles loading, saving and creating new profiles """
#====================================================================#
# Imports
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import JSONdata,FilesFinder
from kivymd.theming import ThemeManager
from kivymd.app import MDApp
#====================================================================#
# Global accessibles
#====================================================================#
profileStructure = {
    "ProfileConfig":
    {
        "CanDelete" : True,  # False, True
        "Type" : "Guest", #"Add", "Guest", "Normal", "Temporary"
    },
    "Generic" :
    {
        "Username" : "Username",
        "Password" : "",
        "IconType" : "Kivy",
        "IconPath" : "account-outline"
    },
    "Theme" :
    {
        "Style" : "Light",
        "Primary" : "Purple",
        "Accent" : "Teal",
        "Duration" : 0.5,
    },
    "Settings" :
    {
        "TO DO":None
    }
}
#====================================================================#
# Global variables imported by other scripts
#====================================================================#
Profiles: FilesFinder = None
"""
    Loaded profiles by the application. This is globally accessible to all
    screens and menus.

    This is built at the very start of the application loading, and stores
    all the available profile files.
"""

#====================================================================#
# Classes
#====================================================================#
class LoadedProfile:
    #region   --------------------------- DOCSTRING
    '''
        Holds the profile that was selected in the ProfileMenu.py screen.
        This profile is used throughout the entire application to save
        the user's data and preferences.

        Defaults to None, as none are loaded when the application starts.
    '''
    #endregion
    #region   --------------------------- MEMBERS
    initialized:bool = False
    """
        if `True`, the LoadedProfile class was initialized with a profile.
        Otherwise, do not use the data inside of this class as it may be
        None or unwanted values.
    """

    rawJson:JSONdata = None
    """
        The raw data loaded from the profile's json. Defaults to `None`.
    """
    #region   --------------------------- METHODS
    #region   -- Public
    def LoadProfile(jsonData:JSONdata) -> bool:
        """
            Function used to initialize the LoadedProfile global class.
            if the function returns `True`, the profile specified was
            successfully loaded into the class.

            If the function returns `False`, an error occured during
            initializing of this global function
        """
        error = False
        # Saves the profile's JSON into the LoadedProfile class.
        LoadedProfile.rawJson = jsonData

        error = LoadedProfile.LoadCLSTheme()

        if(not error):
            LoadedProfile.initialized = True
        else:
            LoadedProfile.initialized = False
        return error
    #endregion
    #region   -- Private
    def LoadCLSTheme() ->bool:
        """
            Loads the CLS theme saved in rawJson, into the application's real theme.
            returns `True` if successful, `False` if not.
        """
        try:
            Style    = LoadedProfile.rawJson.jsonData["Theme"]["Style"]
            Primary  = LoadedProfile.rawJson.jsonData["Theme"]["Primary"]
            Accent   = LoadedProfile.rawJson.jsonData["Theme"]["Accent"]
    
            MDApp.get_running_app().theme_cls.theme_style = Style
            MDApp.get_running_app().theme_cls.primary_palette = Primary
            MDApp.get_running_app().theme_cls.accent_palette = Accent
            MDApp.get_running_app().theme_cls.theme_style_switch_animation_duration = 0
            return True
        except:
            print("_LoadCLSTheme ERROR")
            return False
    #endregion
    #endregion
    #endregion