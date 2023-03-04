#====================================================================#
# File Information
#====================================================================#
""" Handles loading, saving and creating new profiles """
#====================================================================#
# Imports
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("Cache.py")
import os
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from datetime import date,datetime

from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import JSONdata,FilesFinder
from kivymd.theming import ThemeManager
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.color_definitions import palette,colors
#====================================================================#
# Global accessibles
#====================================================================#
cacheStructure = {
    "Cache" :{
        "Dates":{
            "Exit":"",
            "Open":"",
            "Creation":""
        },
        "ExitReason" : None, # Holds the reason the application closed: "User", "Crash", "Low Voltage", "Corrupted"
        "Version" : 1.0, # Holds the cache version
        "Type" : "Application" # Holds which type of cache this is. "Application" / "Driver" / "BrSpand"
    },
    "Profile":{
        "Loaded" : None, # holds the JSON name of the last profile loaded
        "Version" : 1.2,  # holds the version of the last profile loaded
        "Language" : "US_English" # holds the language that was used previously by the application
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
Cache: FilesFinder = None
"""
    Loaded Cache jsons by the application.
    Defaults to: `None`.
"""
#====================================================================#
# Cache class
#====================================================================#
class Cache():
    """
        Handle the cache of the application.
    """
    #region ---- Members
    loaded:bool = False
    """
        If `True`, the cache file was loaded or created successfully.
        Defaults to: `False`
    """
    fileFinder:FilesFinder = None
    """
        :ref:`FileFinder` class used to load JSONs automatically. Created when calling :ref:Load.
    """
    
    jsonData:JSONdata = None
    """
        Holds the bare, loaded JSONdata.
    """
    #endregion
    #region ---- Methods
    def Load() -> bool:
        """
            Load:
            ----------
            Handles the loading and creation of the application's cache.
            This is the first thing you should call in your application
        """
        Debug.Start("Cache: Load")
        path = os.getcwd() + "\\Local\\Cache"
        Cache.fileFinder = FilesFinder("json", path)

        if(len(Cache.fileFinder.fileList) > 0):
            Debug.Log("Some JSON files were found. Creating JSONdata")
            Cache.jsonData = JSONdata("Cache", path)
            if(Cache.jsonData.jsonData == None):
                Debug.Error("FAILED TO LOAD EXISTING JSON CACHE")
                Debug.End()
                return True
            else:
                Debug.Log("JSONdata loaded from existing cache")
                Cache.SetDate("Open")

        else:
            Debug.Log("No JSON files were found.")
            Debug.Log("Creating Cache.json")
            Cache.CreateNew()

        Cache.loaded = True
        Debug.End()
    #-------------------
    def CreateNew():
        """
            CreateNew:
            ----------
            Handles the creation of a new cache file entirely wiping out
            the old one at the location. This specific function will create
            an application, json cache file for BRS Kontrol's generic application.
    
            It will attempt to create it no matter what happens, potentially crashing the application in the event
            where it absolutely cannot be created at all.
        """
        Debug.Start("Cache: CreateNew")
        Cache.jsonData = JSONdata("Cache",os.getcwd() + "\\Local\\Cache\\")

        if(Cache.jsonData.CreateFile(cacheStructure)):
            Cache.jsonData = JSONdata("Cache",os.getcwd() + "\\Local\\Cache\\")
            Debug.Log("File created successfully")
            Cache.SetDate("Creation")
            Cache.SetDate("Open")
        else:
            Debug.Error("FAILED TO CREATE JSON FILE")
        Debug.End()
        pass
    #-------------------
    def SaveFile():
        """
            SaveFile:
            ----------
            Handles the saving of the current saved cache data. Usually called when the application exits.
            It will overwrite the currently saved applications' json file.
        """
        Debug.Start("Cache -> SaveFile")
        if(Cache.loaded):
            Debug.Log(f"jsonData path: {Cache.jsonData.pathToDirectory}")
            Debug.Log(f"jsonData name: {Cache.jsonData.fileName}")
            if(Cache.jsonData.SaveFile()):
                Debug.Log("Save of Application's cache was successful")
            else:
                Debug.Error("Failed to save Application's cache")
        Debug.End()
    #-------------------
    def SetDate(dateType:str):
        """
            SetDate:
            ----------
            Function used to save the current time as a specified cache time.
            The possible cache times to save are located in the `cacheStructure`.
            It will get the computer's current time to save it.
        """
        if(dateType=="Creation" or dateType=="Exit" or dateType=="Open"):
            today = datetime.now()
            Cache.jsonData.jsonData["Cache"]["Dates"][dateType] = today.strftime("%B %d %Y, %H:%M:%S")
    #-------------------
    def SetExit(dateType:str):
        """
            SetExit:
            ----------
            Function used to save the exit reason.
            The exit reason can be used by experienced users to quickly determine why their
            application last closed.
            It can also be used by the application to display an error screen or things like that.
        """
        if(dateType=="User" or dateType=="Low Voltage" or dateType=="Corrupted" or dateType=="Corrupted"):
            today = date.today()
            Cache.jsonData.jsonData["Cache"]["ExitReason"] = dateType
    #-------------------
    def SetInfoFromProfile(self, profile):
        """
            SetInfoFromProfile:
            ----------
            This function takes a :ref:`FileFinder` class which loaded a profile from
            a JSON file, and loads in into the cache class. It will test the profile using
            `CheckIntegrity` specific to Profiles.
        """
        pass
    #-------------------
    def LoadTheme(self):
        """
            LoadTheme:
            ----------
            This function loads the theme saved in the cache into the application.
            Be sure you loaded the cache file prior to calling this.
        """
        pass
    #endregion
#====================================================================#
# Functions
#====================================================================#
def CheckIntegrity(cacheJson:JSONdata) -> str:
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
        if(cacheJson == None):
            return "Error"
        elif(cacheJson.CreateFile == None):
            return "Error"
    except:
        print("ERROR: CheckIntegrity: Step 0")
        return "Error"
    #endregion
    #region [Step 1]: Check if the cache is blank.
    try:
        if(cacheJson.jsonData == None):
            return "Blank"
    except:
        print("ERROR: CheckIntegrity: Step 1")
        return "Error"
    #endregion
    #region [Step 2]: Check if the profile version matches the profileStructure's profile version
    try:
        if(cacheJson["ProfileConfig"]["Version"] > cacheJson.jsonData["ProfileConfig"]["Version"]):
            return "Outdated"
        if(cacheJson["ProfileConfig"]["Version"] < cacheJson.jsonData["ProfileConfig"]["Version"]):
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

LoadingLog.End("Cache.py")