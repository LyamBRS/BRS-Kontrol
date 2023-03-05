#====================================================================#
# File Information
#====================================================================#
""" Handles loading, saving and creating new profiles """
#====================================================================#
# Imports
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("Profiles.py")

from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import JSONdata,FilesFinder
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import FileIntegrity
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
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
        "Version" : 1.2 # the profile version.
    },
    "Generic" :{
        "Username" : "Username",
        "Password" : "",
        "Biography" : "Biography",
        "IconType" : "Kivy",    # Kivy or Path
        "IconPath" : "account-outline",
        "Language" : "US_English"
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

Temporary = {
    "ProfileConfig":{
        "CanDelete" : True,  # False, True
        "Type" : "Normal", #"Guest", "Normal", "Temporary"
        "Version" : 1.2 # the profile version.
    },
    "Generic" :{
        "Username" : "Username",
        "Password" : "Password",
        "Biography" : "Biography",
        "IconType" : "Kivy",    # Kivy or Path
        "IconPath" : "account-outline",
        "Language" : "US_English"
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
"""Used to store profile data when creating a new profile"""
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
def CheckIntegrity(profileJson:JSONdata) -> FileIntegrity:
    """
        This function allows you to check the integrity of a loaded
        profile JSON without having to do it manually.

        It checks every single values within the given profile `JSONdata`.
        
        Returns: (`FileIntegrity`)
            - `Ahead` : The profile version is bigger than the wanted profile version.
            - `Outdated` : The saved profile version does not match the current application's profile version.
            - `Blank` : All the profile's categories are absent.
            - `Corrupted` : Some of the profile's data cannot be used at all.
            - `Good` : The profile's integrity is good and can be loaded properly.
            - `Error` : Fatal error, the given JSON could not be used or salvaged at all.
    """
    Debug.Start("CheckIntegrity")
    #region [Step 0]: Attempt to load the JSON.
    try:
        if(profileJson == None):
            Debug.Warn("Error detected in Step 0. Parameter is blank")
            Debug.End()
            return FileIntegrity.Error
        elif(profileJson.CreateFile == None):
            Debug.Warn("Error detected in Step 0. Parameter is an unrelated class")
            Debug.End()
            return FileIntegrity.Error
    except:
        Debug.Error("Exception in Step 0")
        Debug.End()
        return FileIntegrity.Error
    #endregion
    #region [Step 1]: Check if the profile is blank.
    try:
        if(profileJson.jsonData == None):
            Debug.Warn("File is blank")
            Debug.End()
            return FileIntegrity.Blank
    except:
        Debug.Error("Exception in Step 1")
        Debug.End()
        return FileIntegrity.Error
    #endregion
    #region [Step 2]: Check if the profile version matches the profileStructure's profile version
    try:
        if(profileStructure["ProfileConfig"]["Version"] > profileJson.jsonData["ProfileConfig"]["Version"]):
            Debug.Warn("File detected as outdated in Step 2")
            Debug.End()
            return FileIntegrity.Outdated
        if(profileStructure["ProfileConfig"]["Version"] < profileJson.jsonData["ProfileConfig"]["Version"]):
            Debug.Warn("File detected as ahead in Step 2")
            Debug.End()
            return FileIntegrity.Ahead
    except:
        Debug.Error("Exception in Step 2")
        Debug.End()
        return FileIntegrity.Error
    #endregion
    #region [Step 3]: Check if the keys match the profileStructure
    try:
        if(profileStructure.keys() != profileJson.jsonData.keys()):
            Debug.Warn("Corruption detected in Step 3: unmatching JSON keys")
            Debug.End()
            return FileIntegrity.Corrupted

        if(profileStructure["ProfileConfig"].keys() != profileJson.jsonData["ProfileConfig"].keys()):
            Debug.Warn("Corruption detected in Step 3: ProfileConfig JSON keys")
            Debug.End()
            return FileIntegrity.Corrupted

        if(profileStructure["Generic"].keys() != profileJson.jsonData["Generic"].keys()):
            Debug.Warn("Corruption detected in Step 3: Generic JSON keys")
            Debug.End()
            return FileIntegrity.Corrupted

        if(profileStructure["Theme"].keys() != profileJson.jsonData["Theme"].keys()):
            Debug.Warn("Corruption detected in Step 3: Theme JSON keys")
            Debug.End()
            return FileIntegrity.Corrupted

        if(profileStructure["Settings"].keys() != profileJson.jsonData["Settings"].keys()):
            Debug.Warn("Corruption detected in Step 3: Settings JSON keys")
            Debug.End()
            return FileIntegrity.Corrupted
    except:
        Debug.Error("Exception in Step 3")
        Debug.End()
        return FileIntegrity.Error
    #endregion
    #region [Step 4]: Check if ProfileConfig's elements are correct.
    try:
        A = (type(profileJson.jsonData["ProfileConfig"]["CanDelete"]) == bool)
        C = (type(profileJson.jsonData["ProfileConfig"]["Version"]) == float)
        B = profileJson.jsonData["ProfileConfig"]["Type"] == "Normal" or profileJson.jsonData["ProfileConfig"]["Type"] == "Guest" or profileJson.jsonData["ProfileConfig"]["Type"] == "Admin"
        if(not (A and B and C)):
            Debug.Warn("Corruption detected in Step 4: ProfileConfig")
            Debug.End()
            return FileIntegrity.Corrupted
    except:
        Debug.Error("Exception in Step 4")
        Debug.End()
        return FileIntegrity.Error
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
                Debug.Warn("Corruption detected in Step 5. Kivy Icon does not exist")
                Debug.End()
                return FileIntegrity.Corrupted

        if(not (A and B and C)):
            Debug.Warn("Corruption detected in Step 5.")
            Debug.End()
            return FileIntegrity.Corrupted

    except:
        Debug.Error("Exception in Step 5")
        Debug.End()
        return FileIntegrity.Corrupted
    #endregion
    #region [Step 6]: Check if Theme's elements are correct.
    try:
        A = (profileJson.jsonData["Theme"]["Style"] == "Dark" or profileJson.jsonData["Theme"]["Style"] == "Light")
        B = (profileJson.jsonData["Theme"]["Accent"] in colors)
        C = (profileJson.jsonData["Theme"]["Primary"] in colors)
        D = (type(profileJson.jsonData["Theme"]["Duration"]) == float)

        if(not (A and B and C and D)):
            Debug.Warn("Corruption detected in Step 6")
            Debug.End()
            return FileIntegrity.Corrupted
    except:
        Debug.Error("Exception in Step 6")
        Debug.End()
        return FileIntegrity.Error
    #endregion
    #region [Step 7]: End of Integrity checks
    Debug.Log("SUCCESS")
    Debug.End()
    return FileIntegrity.Good
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
        Debug.Start("LoadedProfile -> LoadProfile")
        error = False
        # Saves the profile's JSON into the LoadedProfile class.
        LoadedProfile.rawJson = jsonData

        error = LoadedProfile.LoadCLSTheme()

        if(not error):
            Debug.Log("Profile initialized successfully")
            LoadedProfile.initialized = True
        else:
            Debug.Log("Profile failed to load")
            LoadedProfile.initialized = False

        Debug.End()
        return error
    #endregion
    #region   -- Private
    def LoadCLSTheme() ->bool:
        """
            Loads the CLS theme saved in rawJson, into the application's real theme.
            returns `True` if successful, `False` if not.
        """
        Debug.Start("LoadedProfile -> LoadCLSTheme")
        try:
            Style    = LoadedProfile.rawJson.jsonData["Theme"]["Style"]
            Primary  = LoadedProfile.rawJson.jsonData["Theme"]["Primary"]
            Accent   = LoadedProfile.rawJson.jsonData["Theme"]["Accent"]

            MDApp.get_running_app().theme_cls.theme_style = Style
            MDApp.get_running_app().theme_cls.primary_palette = Primary
            MDApp.get_running_app().theme_cls.accent_palette = Accent
            MDApp.get_running_app().theme_cls.theme_style_switch_animation_duration = 0

            Debug.Log("SUCCESS")
            Debug.End()
            return True
        except:
            Debug.Error("_LoadCLSTheme ERROR")
            Debug.End()
            return False
    #endregion
    #endregion
    #endregion

LoadingLog.End("Profiles.py")