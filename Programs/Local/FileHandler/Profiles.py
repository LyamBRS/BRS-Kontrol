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
from kivymd.icon_definitions import md_icons
from kivymd.color_definitions import palette,colors
#====================================================================#
# Global accessibles
#====================================================================#
profileStructure = {
    "ProfileConfig":{
        "CanDelete" : True,  # False, True
        "Type" : "Guest", #"Guest", "Normal", "Temporary"
        "Version" : 1.0 # the profile version.
    },
    "Generic" :{
        "Username" : "Username",
        "Password" : "",
        "IconType" : "Kivy",    # Kivy or Path
        "IconPath" : "account-outline"
    },
    "Theme" :{
        "Style" : "Light",
        "Primary" : "Purple",
        "Accent" : "Teal",
        "Duration" : 0.5,
    },
    "Settings" :{
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
# Functions
#====================================================================#
def CheckIntegrity(profileJson:JSONdata) -> str:
    """
        This function allows you to check the integrity of a loaded
        profile JSON without having to do it manually.

        It checks every single values within the given profile `JSONdata`.
        
        Returns: (`str`)
            - `"Ahead"` : The profile version is bigger than the wanted profile version.
            - `"Outdated"` : The saved profile version does not match the current application's profile version.
            - `"Blank"` : All the profile's categories are absent.
            - `"Corrupted"` : Some of the profile's data cannot be used at all.
            - `"Good"` : The profile's integrity is good and can be loaded properly.
            - `"Error"` : Fatal error, the given JSON could not be used or salvaged at all.
    """
    #region [Step 0]: Attempt to load the JSON.
    try:
        if(profileJson == None):
            return "Error"
        elif(profileJson.CreateFile == None):
            return "Error"
    except:
        print("ERROR: CheckIntegrity: Step 0")
        return "Error"
    #endregion
    #region [Step 1]: Check if the profile is blank.
    try:
        if(profileJson.jsonData == None):
            return "Blank"
    except:
        print("ERROR: CheckIntegrity: Step 1")
        return "Error"
    #endregion
    #region [Step 2]: Check if the profile version matches the profileStructure's profile version
    try:
        if(profileStructure["ProfileConfig"]["Version"] > profileJson.jsonData["ProfileConfig"]["Version"]):
            return "Outdated"
        if(profileStructure["ProfileConfig"]["Version"] < profileJson.jsonData["ProfileConfig"]["Version"]):
            return "Ahead"
    except:
        print("ERROR: CheckIntegrity: Step 2")
        return "Error"
    #endregion
    #region [Step 3]: Check if the keys match the profileStructure
    try:
        if(profileStructure.keys() != profileJson.jsonData.keys()):
            return "Corrupted"
        if(profileStructure["ProfileConfig"].keys() != profileJson.jsonData["ProfileConfig"].keys()):
            return "Corrupted"
        if(profileStructure["Generic"].keys() != profileJson.jsonData["Generic"].keys()):
            return "Corrupted"
        if(profileStructure["Theme"].keys() != profileJson.jsonData["Theme"].keys()):
            return "Corrupted"
        if(profileStructure["Settings"].keys() != profileJson.jsonData["Settings"].keys()):
            return "Corrupted"
    except:
        print("ERROR: CheckIntegrity: Step 3")
        return "Error"
    #endregion
    #region [Step 4]: Check if ProfileConfig's elements are correct.
    try:
        A = (type(profileJson.jsonData["ProfileConfig"]["CanDelete"]) == bool)
        C = (type(profileJson.jsonData["ProfileConfig"]["Version"]) == float)
        B = profileJson.jsonData["ProfileConfig"]["Type"] == "Normal" or profileJson.jsonData["ProfileConfig"]["Type"] == "Guest" or profileJson.jsonData["ProfileConfig"]["Type"] == "Admin"
        if(not (A and B and C)):
            return "Corrupted"
    except:
        print("ERROR: CheckIntegrity: Step 4")
        return "Error"
    #endregion
    #region [Step 5]: Check if Generic's elements are correct.
    try:
        A = (type(profileJson.jsonData["Generic"]["Username"]) == str)
        B = (type(profileJson.jsonData["Generic"]["Password"]) == str)
        C = (profileJson.jsonData["Generic"]["IconType"] == "Kivy" or profileJson.jsonData["Generic"]["IconType"] == "Path")

        if(profileJson.jsonData["Generic"]["IconType"] == "Kivy"):
            try:
                icon = md_icons[profileJson.jsonData["Generic"]["IconPath"]]
            except:
                print("ERROR: profile's KivyMD icon does not exist")
                return "Corrupted"

        if(not (A and B and C)):
            return "Corrupted"

    except:
        print("ERROR: CheckIntegrity: Step 5")
        return "Error"
    #endregion
    #region [Step 6]: Check if Theme's elements are correct.
    try:
        A = (profileJson.jsonData["Theme"]["Style"] == "Dark" or profileJson.jsonData["Theme"]["Style"] == "Light")
        B = (profileJson.jsonData["Theme"]["Accent"] in colors)
        C = (profileJson.jsonData["Theme"]["Primary"] in colors)
        D = (type(profileJson.jsonData["Theme"]["Duration"]) == float)

        if(not (A and B and C and D)):
            return "Corrupted"
    except:
        print("ERROR: CheckIntegrity: Step 6")
        return "Error"
    #endregion
    #region [Step 7]: End of Integrity checks
    return "Good"
    #endregion
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