#====================================================================#
# File Information
#====================================================================#
"""
    DeviceDriver.py
    =============
    This file's purpose is to handle the files of downloaded device
    drivers such as their Jsons, integrity checks, loading their GUIs,
    and so on.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("AppLoading.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
import os
#endregion
#region --------------------------------------------------------- BRS
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import FilesFinder, JSONdata, IsPathValid
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog      import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums       import FileIntegrity
#endregion
#region -------------------------------------------------------- Kivy
#endregion
#region ------------------------------------------------------ KivyMD
#endregion
#====================================================================#
# Structures
#====================================================================#
#region -------------------------------------------------- Directories
mandatoryDriverContent = [
    "Local",
    "Pages",
    "Programs",
    "Config.json",
    "Driver.py"
]
"""
    mandatoryDriverContent:
    -----------------------
    This file structure represents the mandatory minimum folders needed
    for Kontrol to identify your device driver as a valid device driver.

    `Driver//_____`
"""
mandatoryLocalContent = [
    "Cache",
    "Languages",
    "Profiles",
]
#endregion
#region --------------------------------------------------------- JSON
JsonStructure = {
    "Information" : {
        "Authors"       : [],
        "Companies"     : [],
        "Version"       : "Driver's version",
        "Name"          : "Driver's name",
        "Description"   : "Driver's description",
        "IconPath"      : "bug",
        "IconType"      : "Kivy"
    },
    "Configuration"     : {
        "Version"       : "2023.03.21",
        "Repository"    : ""
    },
    "Requirements" : {
        "OS"            : "Any",
        "Processor"     : "Any",
        "Internet"      : False,
        "Bluethoot"     : False,
        "BrSpand"       : False,
        "Kontrol"       : False,
        "OtherDevice"   : False
    },
    "Utilizes" : {
        "Internet"      : False,
        "Bluethoot"     : False,
        "BrSpand"       : False,
        "Kontrol"       : False,
        "OtherDevice"   : False
    }
}
#endregion
#====================================================================#
# Functions
#====================================================================#
def CheckIntegrity(NameOfDeviceDriver:str) -> FileIntegrity:
    """
        CheckIntegrity:
        ---------------
        This function's purpose is to check a device driver's folder
        integrity to see if it follows standardization and BRS's way
        of creating drivers.

        Returns:
            - `FileIntegrity(Enum)` : Error message. Good if no error
    """
    Debug.Start("DeviceDriver -> CheckIntegrity")

    #region -------------------------------------------------- STEP 1
    Debug.Log("[1]: Path validation")
    pathToDeviceDriver = os.getcwd() + f"\\Local\\Drivers\\{NameOfDeviceDriver}"

    if(IsPathValid(pathToDeviceDriver)):
        Debug.Log(">>> Success")
    else:
        Debug.Error(f" -> Invalid path specified {pathToDeviceDriver}")
        Debug.End()
        return FileIntegrity.Error
    #endregion
    #region -------------------------------------------------- STEP 2
    Debug.Log("[2]: Main content verifications")

    content = os.listdir(pathToDeviceDriver)
    Debug.Log(content)
    if all(elem in content for elem in mandatoryDriverContent):
        Debug.Log(">>> SUCCESS")
    else:
        Debug.Error("-> mandatory content cannot be found in Driver")
        Debug.Error(f"Required : {mandatoryDriverContent}")
        Debug.Error(f"Found : {content}")
        Debug.End()
        return FileIntegrity.Corrupted
    #endregion
    #region -------------------------------------------------- STEP 3
    Debug.Log("[3]: Local folder verification")
    content = os.listdir(pathToDeviceDriver + "\\Local")
    Debug.Log(content)

    if all(elem in content for elem in mandatoryLocalContent):
        Debug.Log(">>> SUCCESS")
    else:
        Debug.Error("-> mandatory content cannot be found in Local folder")
        Debug.Error(f"Required : {mandatoryLocalContent}")
        Debug.Error(f"Found : {content}")
        Debug.End()
        return FileIntegrity.Corrupted
    #endregion

    Debug.End()
# -------------------------------------------------------------------
def GetDrivers(NameOfDeviceDriver) -> list:
    """
        GetDrivers:
        -----------
        This function returns a list of the device drivers downloaded
        on this Kontrol. It only returns the name of their folders in
        the form of a list of strings.
    """
    Debug.Start("GetDrivers")
    appPath = os.getcwd()
    appPath = appPath + f"\\Local\\Drivers\\{NameOfDeviceDriver}"

    Debug.Log("Found drivers:")
    drivers = os.listdir(appPath)
    new_drivers = [s for s in drivers if '.' not in s]
    Debug.Log(new_drivers)
    Debug.End()

    return drivers
#====================================================================#
# Classes
#====================================================================#

#====================================================================#
LoadingLog.End("AppLoading.py")