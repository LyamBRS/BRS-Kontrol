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
import os
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import JSONdata,FilesFinder, AppendPath
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import FileIntegrity
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from kivymd.theming import ThemeManager
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.color_definitions import palette,colors
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Dates
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import AppLanguage
from datetime import date,datetime
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
    Dates:str = "Dates"

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
    structureEnum.ProfileConfig.value:{
        ProfileConfigEnum.CanDelete.value : True,  # False, True
        ProfileConfigEnum.Type.value      : "Guest", #"Guest", "Normal", "Temporary"
        ProfileConfigEnum.Version.value   : 1.3, # the profile version.
        ProfileConfigEnum.Dates.value:{
            Dates.Creation.value:"",
            Dates.Updated.value:"",
            Dates.Open.value:"",
            Dates.Exit.value:""
        },
    },
    structureEnum.Generic.value :{
        ProfileGenericEnum.Username.value: "Username",
        ProfileGenericEnum.Password.value: "",
        ProfileGenericEnum.Biography.value: "Biography",
        ProfileGenericEnum.IconType.value: "Kivy",    # Kivy or Path
        ProfileGenericEnum.IconPath.value: "account-outline",
        ProfileGenericEnum.Language.value: "US_English"
    },
    structureEnum.Theme.value :{
        ProfileThemeEnum.Style.value  : "Light",
        ProfileThemeEnum.Primary.value  : "Purple",
        ProfileThemeEnum.Accent.value  : "Teal",
        ProfileThemeEnum.Duration.value  : 0.5,
    },
    structureEnum.Settings.value :{
        "TO DO":None
    }
}




Temporary = {
    structureEnum.ProfileConfig.value:{
        ProfileConfigEnum.CanDelete.value : True,  # False, True
        ProfileConfigEnum.Type.value      : "Guest", #"Guest", "Normal", "Temporary"
        ProfileConfigEnum.Version.value   : 1.3, # the profile version.
        ProfileConfigEnum.Dates.value:{
            Dates.Creation.value:"",
            Dates.Updated.value:"",
            Dates.Open.value:"",
            Dates.Exit.value:""
        },
    },
    structureEnum.Generic.value :{
        ProfileGenericEnum.Username.value: "",
        ProfileGenericEnum.Password.value: "",
        ProfileGenericEnum.Biography.value: "",
        ProfileGenericEnum.IconType.value: "Kivy",    # Kivy or Path
        ProfileGenericEnum.IconPath.value: "account-outline",
        ProfileGenericEnum.Language.value: "US_English"
    },
    structureEnum.Theme.value :{
        ProfileThemeEnum.Style.value  : "Light",
        ProfileThemeEnum.Primary.value  : "Purple",
        ProfileThemeEnum.Accent.value  : "Teal",
        ProfileThemeEnum.Duration.value  : 0.5,
    },
    structureEnum.Settings.value :{
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
        if(profileStructure[structureEnum.ProfileConfig.value][ProfileConfigEnum.Version.value] > profileJson.jsonData[structureEnum.ProfileConfig.value][ProfileConfigEnum.Version.value]):
            Debug.Warn("File detected as outdated in Step 2")
            Debug.End()
            return FileIntegrity.Outdated
        if(profileStructure[structureEnum.ProfileConfig.value][ProfileConfigEnum.Version.value] < profileJson.jsonData[structureEnum.ProfileConfig.value][ProfileConfigEnum.Version.value]):
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

        if(profileStructure[structureEnum.ProfileConfig.value].keys() != profileJson.jsonData[structureEnum.ProfileConfig.value].keys()):
            Debug.Warn("Corruption detected in Step 3: ProfileConfig JSON keys")
            Debug.End()
            return FileIntegrity.Corrupted

        if(profileStructure[structureEnum.Generic.value].keys() != profileJson.jsonData[structureEnum.Generic.value].keys()):
            Debug.Warn("Corruption detected in Step 3: Generic JSON keys")
            Debug.End()
            return FileIntegrity.Corrupted

        if(profileStructure[structureEnum.Theme.value].keys() != profileJson.jsonData[structureEnum.Theme.value].keys()):
            Debug.Warn("Corruption detected in Step 3: Theme JSON keys")
            Debug.End()
            return FileIntegrity.Corrupted

        if(profileStructure[structureEnum.Settings.value].keys() != profileJson.jsonData[structureEnum.Settings.value].keys()):
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
        A = (type(profileJson.jsonData[structureEnum.ProfileConfig.value][ProfileConfigEnum.CanDelete.value]) == bool)
        C = (type(profileJson.jsonData[structureEnum.ProfileConfig.value][ProfileConfigEnum.Version.value]) == float)
        B = profileJson.jsonData[structureEnum.ProfileConfig.value][ProfileConfigEnum.Type.value] == "Normal" or profileJson.jsonData[structureEnum.ProfileConfig.value][ProfileConfigEnum.Type.value] == "Guest" or profileJson.jsonData[structureEnum.ProfileConfig.value][ProfileConfigEnum.Type.value] == "Admin"
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
        A = (type(profileJson.jsonData[structureEnum.Generic.value][ProfileGenericEnum.Username.value]) == str)
        B = (type(profileJson.jsonData[structureEnum.Generic.value][ProfileGenericEnum.Password.value]) == str)
        C = (profileJson.jsonData[structureEnum.Generic.value][ProfileGenericEnum.IconType.value] == "Kivy" or profileJson.jsonData[structureEnum.Generic.value][ProfileGenericEnum.IconType.value] == "Path")

        if(profileJson.jsonData[structureEnum.Generic.value][ProfileGenericEnum.IconType.value] == "Kivy"):
            try:
                icon = md_icons[profileJson.jsonData[structureEnum.Generic.value][ProfileGenericEnum.IconPath.value]]
            except:
                Debug.Warn("Corruption detected in Step 5. Kivy Icon does not exist")
                Debug.End()
                return FileIntegrity.Corrupted

        if(not (A and B and C)):
            Debug.Warn("Corruption detected in Step 5.")
            Debug.Warn("")
            Debug.End()
            return FileIntegrity.Corrupted

    except:
        Debug.Error("Exception in Step 5")
        Debug.End()
        return FileIntegrity.Corrupted
    #endregion
    #region [Step 6]: Check if Theme's elements are correct.
    try:
        A = (profileJson.jsonData[structureEnum.Theme.value][ProfileThemeEnum.Style.value] == "Dark" or profileJson.jsonData[structureEnum.Theme.value][ProfileThemeEnum.Style.value] == "Light")
        B = (profileJson.jsonData[structureEnum.Theme.value][ProfileThemeEnum.Accent.value] in colors)
        C = (profileJson.jsonData[structureEnum.Theme.value][ProfileThemeEnum.Primary.value] in colors)
        D = (type(profileJson.jsonData[structureEnum.Theme.value][ProfileThemeEnum.Duration.value]) == float)

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
#--------------------------------------------------------------------
def CheckUsername(username:str) -> bool:
    """
        CheckUsername:
        -------------
        This function checks a username string and returns a boolean
        value if the username is correct.
    
        Returns:
            - (`bool`): `False` = Username can be used.
            - (`str`)
    """
    Debug.Start("CheckUsername")
    maxLenght = 10
    bannedChars = {'#', '<', '>', '*', '?', '/', '%', '&', '\\', '{', '}', '$', '!', '+', '"', '\'', '`', ':', '@', '=', '|', '.'}

    Debug.Log("Checking if profile already exists")
    Profiles = FilesFinder(".json", AppendPath(os.getcwd(), "/Local/Profiles"))
    if((username)+".json" in Profiles.fileList):
        Debug.Log("username already exists")
        Debug.End()
        return "Already exists"

    if(len(username) < maxLenght):

        if(len(username) == 0):
            Debug.Error("Cannot be empty")
            Debug.End()
            return "Cannot be empty"

        for char in bannedChars:
            if char in username:
                Debug.Error("Username contains illegal character(s)")
                Debug.End()
                return "Illegal characters"
        Debug.Log("Username is good")
        Debug.End()
        return False
    else:
        Debug.Error("Too long")
        Debug.End()
        return "Too long"
#--------------------------------------------------------------------
def CheckPassword(password:str) -> bool:
    """
        CheckPassword:
        -------------
        This function checks a password string and returns a boolean
        value if the password is correct.
    
        Returns:
            - (`bool`): `False` = Password can be used.
            - (`str`)
    """
    Debug.Start("CheckPassword")
    maxLenght = 32
    bannedChars = {'"', '\\'}

    if(len(password) < maxLenght):

        # if(len(password) == 0):
        #     Debug.Error("Lenght 0")
        #     Debug.End()
        #     return "Username cannot be nothing"

        for char in bannedChars:
            if char in password:
                Debug.Error("Password contains illegal character(s)")
                Debug.End()
                return "Illegal characters"
        Debug.Log("Password is good")
        Debug.End()
        return False
    else:
        Debug.Error("Too long")
        Debug.End()
        return "Too long"
#--------------------------------------------------------------------
def CheckBiography(biography:str) -> bool:
    """
        CheckBiography:
        -------------
        This function checks a biography string and returns a boolean
        value if the biography is correct.
    
        Returns:
            - (`bool`): `False` = biography can be used.
            - (`str`)
    """
    Debug.Start("CheckBiography")
    maxLenght = 1024
    bannedChars = {'"', '\\'}

    if(len(biography) < maxLenght):

        if(len(biography) == 0):
            Debug.Error("Lenght 0")
            Debug.End()
            return False#"Username cannot be nothing"

        for char in bannedChars:
            if char in biography:
                Debug.Error("biography contains illegal character(s)")
                Debug.End()
                return "Illegal characters"
        Debug.Log("biography is good")
        Debug.End()
        return False
    else:
        Debug.Error("Too long")
        Debug.End()
        return "Too long"

#====================================================================#
# Classes
#====================================================================#
class ProfileHandler:
    #region   --------------------------- DOCSTRING
    '''
        ProfileHandler:
        ---------------
        Holds the profile that was selected in the ProfileMenu.py screen.
        This profile is used throughout the entire application to save
        the user's data and preferences.

        Also holds various functions used to handle the loaded profile
        or create new profiles from Temporary for example.

        Defaults to None, as none are loaded when the application starts.
    '''
    #endregion
    #region   --------------------------- MEMBERS
    initialized:bool = False
    """
        if `True`, the ProfileHandler class was initialized with a profile.
        Otherwise, do not use the data inside of this class as it may be
        `None` or unwanted values.
    """

    rawJson:JSONdata = None
    """
        The raw data loaded from the profile's json. Defaults to `None`.
    """
    #endregion
    #region   --------------------------- METHODS
    #region   -- Public
    def LoadProfile(jsonData:JSONdata) -> bool:
        """
            Function used to initialize the ProfileHandler global class.
            if the function returns `True`, the profile specified was
            successfully loaded into the class.

            If the function returns `False`, an error occured during
            initializing of this global function
        """
        Debug.Start("ProfileHandler -> LoadProfile")
        error = False

        error = CheckIntegrity(jsonData)
        if(error == FileIntegrity.Good):
            # Saves the profile's JSON into the ProfileHandler class.
            ProfileHandler.rawJson = jsonData

            # Load profile's CLS theme into the application
            error = ProfileHandler.LoadCLSTheme()
            if(error):
                Debug.Log("Profile initialized successfully")
                ProfileHandler.initialized = True

                AppLanguage.LoadLanguage(ProfileHandler.rawJson.jsonData[structureEnum.Generic.value][ProfileGenericEnum.Language.value])

                Debug.Log("Setting new dates")
                ProfileHandler.SetDate(Dates.Open)

                Debug.Log("Setting Cache")
                Debug.Error("TO DO")
            else:
                Debug.Error("Profile failed to load")
                ProfileHandler.initialized = False

            Debug.End()
            return error
        else:
            Debug.Error("Specified program failed CheckIntegrity")
            Debug.Log(f"Error code: {error}")
            Debug.End()
            return error
    #------------------------------------
    def CreateProfile(profileStructure:list) -> bool:
        """
            CreateProfile:
            --------------
            This function allows you to create a new profile from
            a :ref:`profileStructure` styled list such as :ref:`Temporary`.
            The created profile will be the latest profile version and
            will be automatically loaded in :ref:`rawJson` for the application
            to use as the current LoadedProfile.
        """
        Debug.Start("ProfileHandler -> CreateProfile")

        Debug.Log("Getting profile directory")
        profileDirectory = AppendPath(os.getcwd(), "/Local/Profiles/")

        sus = {"among us" : 1}

        Debug.Log(profileStructure)

        Json = JSONdata(profileStructure[structureEnum.Generic.value][ProfileGenericEnum.Username.value], profileDirectory)
        Json.jsonData = profileStructure
        if(not Json.CreateFile(profileStructure)):
            Debug.Log("New profile successfully created and saved")
            Json = JSONdata(profileStructure[structureEnum.Generic.value][ProfileGenericEnum.Username.value], profileDirectory)
            # Json.jsonData = profileStructure
            ProfileHandler.LoadProfile(Json)
            ProfileHandler.SetDate(Dates.Creation)
            Json.SaveFile()
        else:
            Debug.Error("Profile could not be saved.", FileName="Profiles.py", Line=487)

        Debug.End()
    #------------------------------------
    def SetDate(dateType:Dates):
        """
            SetDate:
            ----------
            Function used to save the current time as a specified profile time.
            The possible profile times to save are located in the :ref:`ProfileConfigEnum`.
            It will get the computer's current time to save it.
        """
        Debug.Start("ProfileHandler -> SetDate")
        Debug.Log("Getting datetime.now()")
        today = datetime.now()

        if(dateType == Dates.Updated or dateType == Dates.Creation or dateType == Dates.Exit or dateType == Dates.Open):
            Debug.Log(f"Saving profile's {dateType} date.")
            ProfileHandler.rawJson.jsonData[structureEnum.ProfileConfig.value][ProfileConfigEnum.Dates.value][dateType.value] = today.strftime("%B %d %Y, %H:%M:%S")

            # Saving the file's new data.
            if(ProfileHandler.rawJson.SaveFile()):
                Debug.Log("Profile has been saved")
            else:
                Debug.Error("Failed to save profile")
        else:
            Debug.Error("ATTEMPTED TO SAVE UNKOWN DATE INTO PROFILE JSON.")
        Debug.End()
    #endregion
    #region   -- Private
    def LoadCLSTheme() ->bool:
        """
            Loads the CLS theme saved in rawJson, into the application's real theme.
            returns `True` if successful, `False` if not.
        """
        Debug.Start("ProfileHandler -> LoadCLSTheme")
        try:
            Style    = ProfileHandler.rawJson.jsonData[structureEnum.Theme.value][ProfileThemeEnum.Style.value]
            Primary  = ProfileHandler.rawJson.jsonData[structureEnum.Theme.value][ProfileThemeEnum.Primary.value]
            Accent   = ProfileHandler.rawJson.jsonData[structureEnum.Theme.value][ProfileThemeEnum.Accent.value]

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

LoadingLog.End("Profiles.py")