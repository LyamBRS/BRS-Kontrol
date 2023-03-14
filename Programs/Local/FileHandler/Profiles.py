#====================================================================#
# File Information
#====================================================================#
""" Handles loading, saving and creating new profiles """
#====================================================================#
# Imports
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("Profiles.py")

from enum import Enum
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
class structureEnum(Enum):
    """
        structureEnum:
        --------------
        Contains each keys of the :ref:`profileStructure`
    """
    ProfileConfig:str = "ProfileConfig"
    Generic:str = "Generic"
    Theme:str = "Theme"
    Settings:str = "Settings"

class ProfileConfigEnum(Enum):
    CanDelete:str = "CanDelete"
    Type:str = "Type"
    Version:str = "Version"

class ProfileGenericEnum(Enum):
    Username:str = "Username"
    Password:str = "Password"
    Biography:str = "Biography"
    IconType:str = "IconType"
    IconPath:str = "IconPath"
    Language:str = "Language"

class ProfileThemeEnum(Enum):
    Style:str = "Style"
    Password:str = "Primary"
    Accent:str = "Accent"
    Duration:str = "Duration"

class ProfileThemeEnum(Enum):
    Style:str = "Style"
    Primary:str = "Primary"
    Accent:str = "Accent"
    Duration:str = "Duration"
#====================================================================#
profileStructure = {
    structureEnum.ProfileConfig:{
        ProfileConfigEnum.CanDelete : True,  # False, True
        ProfileConfigEnum.Type : "Guest", #"Guest", "Normal", "Temporary"
        ProfileConfigEnum.Version : 1.2 # the profile version.
    },
    structureEnum.Generic :{
        ProfileGenericEnum.Username: "Username",
        ProfileGenericEnum.Password: "",
        ProfileGenericEnum.Biography: "Biography",
        ProfileGenericEnum.IconType: "Kivy",    # Kivy or Path
        ProfileGenericEnum.IconPath: "account-outline",
        ProfileGenericEnum.Language: "US_English"
    },
    structureEnum.Theme :{
        ProfileThemeEnum.Style  : "Light",
        ProfileThemeEnum.Primary  : "Purple",
        ProfileThemeEnum.Accent  : "Teal",
        ProfileThemeEnum.Duration  : 0.5,
    },
    structureEnum.Settings :{
        "TO DO":None
    }
}




Temporary = {
    structureEnum.ProfileConfig:{
        ProfileConfigEnum.CanDelete : True,  # False, True
        ProfileConfigEnum.Type : "Guest", #"Guest", "Normal", "Temporary"
        ProfileConfigEnum.Version : 1.2 # the profile version.
    },
    structureEnum.Generic :{
        ProfileGenericEnum.Username: "Username",
        ProfileGenericEnum.Password: "",
        ProfileGenericEnum.Biography: "Biography",
        ProfileGenericEnum.IconType: "Kivy",    # Kivy or Path
        ProfileGenericEnum.IconPath: "account-outline",
        ProfileGenericEnum.Language: "US_English"
    },
    structureEnum.Theme :{
        ProfileThemeEnum.Style  : "Light",
        ProfileThemeEnum.Primary  : "Purple",
        ProfileThemeEnum.Accent  : "Teal",
        ProfileThemeEnum.Duration  : 0.5,
    },
    structureEnum.Settings :{
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
        if(profileStructure[structureEnum.ProfileConfig][ProfileConfigEnum.Version] > profileJson.jsonData[structureEnum.ProfileConfig][ProfileConfigEnum.Version]):
            Debug.Warn("File detected as outdated in Step 2")
            Debug.End()
            return FileIntegrity.Outdated
        if(profileStructure[structureEnum.ProfileConfig][ProfileConfigEnum.Version] < profileJson.jsonData[structureEnum.ProfileConfig][ProfileConfigEnum.Version]):
            Debug.Warn("File detected as ahead in Step 2")
            Debug.End()
            return FileIntegrity.Ahead
    except:
        Debug.Error(f"Exception in Step 2: {ProfileConfigEnum.Version}")
        Debug.End()
        return FileIntegrity.Error
    #endregion
    #region [Step 3]: Check if the keys match the profileStructure
    try:
        if(profileStructure.keys() != profileJson.jsonData.keys()):
            Debug.Warn("Corruption detected in Step 3: unmatching JSON keys")
            Debug.End()
            return FileIntegrity.Corrupted

        if(profileStructure[structureEnum.ProfileConfig].keys() != profileJson.jsonData[structureEnum.ProfileConfig].keys()):
            Debug.Warn("Corruption detected in Step 3: ProfileConfig JSON keys")
            Debug.End()
            return FileIntegrity.Corrupted

        if(profileStructure[structureEnum.Generic].keys() != profileJson.jsonData[structureEnum.Generic].keys()):
            Debug.Warn("Corruption detected in Step 3: Generic JSON keys")
            Debug.End()
            return FileIntegrity.Corrupted

        if(profileStructure[structureEnum.Theme].keys() != profileJson.jsonData[structureEnum.Theme].keys()):
            Debug.Warn("Corruption detected in Step 3: Theme JSON keys")
            Debug.End()
            return FileIntegrity.Corrupted

        if(profileStructure[structureEnum.Settings].keys() != profileJson.jsonData[structureEnum.Settings].keys()):
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
        A = (type(profileJson.jsonData[structureEnum.ProfileConfig][ProfileConfigEnum.CanDelete]) == bool)
        C = (type(profileJson.jsonData[structureEnum.ProfileConfig][ProfileConfigEnum.Version]) == float)
        B = profileJson.jsonData[structureEnum.ProfileConfig][ProfileConfigEnum.Type] == "Normal" or profileJson.jsonData[structureEnum.ProfileConfig][ProfileConfigEnum.Type] == "Guest" or profileJson.jsonData[structureEnum.ProfileConfig][ProfileConfigEnum.Type] == "Admin"
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
        ProfileGenericEnum.Username
        A = (type(profileJson.jsonData[structureEnum.Generic][ProfileGenericEnum.Username]) == str)
        B = (type(profileJson.jsonData[structureEnum.Generic][ProfileGenericEnum.Password]) == str)
        C = (profileJson.jsonData[structureEnum.Generic][ProfileGenericEnum.IconType] == "Kivy" or profileJson.jsonData[structureEnum.Generic][ProfileGenericEnum.IconType] == "Path")

        if(profileJson.jsonData[structureEnum.Generic][ProfileGenericEnum.IconType] == "Kivy"):
            try:
                icon = md_icons[profileJson.jsonData[structureEnum.Generic][ProfileGenericEnum.IconPath]]
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
        A = (profileJson.jsonData[structureEnum.Theme][ProfileThemeEnum.Style] == "Dark" or profileJson.jsonData[structureEnum.Theme][ProfileThemeEnum.Style] == "Light")
        B = (profileJson.jsonData[structureEnum.Theme][ProfileThemeEnum.Accent] in colors)
        C = (profileJson.jsonData[structureEnum.Theme][ProfileThemeEnum.Primary] in colors)
        D = (type(profileJson.jsonData[structureEnum.Theme][ProfileThemeEnum.Duration]) == float)

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
            Style    = LoadedProfile.rawJson.jsonData[structureEnum.Theme][ProfileThemeEnum.Style]
            Primary  = LoadedProfile.rawJson.jsonData[structureEnum.Theme][ProfileThemeEnum.Primary]
            Accent   = LoadedProfile.rawJson.jsonData[structureEnum.Theme][ProfileThemeEnum.Accent]

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