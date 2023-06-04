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
LoadingLog.Start("deviceDriver.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
import os
from git import rmtree
#endregion
#region --------------------------------------------------------- BRS
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import FilesFinder, JSONdata, IsPathValid, CompareKeys, AppendPath
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog      import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums       import FileIntegrity, Execution
#endregion
#region -------------------------------------------------------- Kivy
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import("KivyMD")
from kivymd.uix.button import MDIconButton
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
    pathToDeviceDriver = AppendPath(os.getcwd(), f"/Local/Drivers/{NameOfDeviceDriver}")

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
    Debug.Log(f">>> {content}")
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
    content = os.listdir(AppendPath(pathToDeviceDriver, "/Local"))
    Debug.Log(f">>> {content}")

    if all(elem in content for elem in mandatoryLocalContent):
        Debug.Log(">>> SUCCESS")
    else:
        Debug.Error("-> mandatory content cannot be found in Local folder")
        Debug.Error(f"Required : {mandatoryLocalContent}")
        Debug.Error(f"Found : {content}")
        Debug.End()
        return FileIntegrity.Corrupted
    #endregion
    #region -------------------------------------------------- STEP 4
    Debug.Log("[4]: Config.json verifications")
    json = JSONdata("Config", pathToDeviceDriver)

    if (len(json.jsonData.keys()) != len(JsonStructure.keys())):
        Debug.Error("-> Number of keys don't match")
        Debug.End()
        return FileIntegrity.Corrupted
    else:
        Debug.Log(">>> SUCCESS")
    #endregion
    #region -------------------------------------------------- STEP 5
    Debug.Log("[5]: Config.json deep verifications")

    Debug.Log(">>> Checking regular keys")
    error = CompareKeys(JsonStructure, json.jsonData, "Huh")
    if(error == FileIntegrity.Good):
        Debug.Log(">>> SUCCESS")
    else:
        Debug.Error("-> JSON file is not correct.")
        Debug.End()
        return FileIntegrity.Corrupted

    #endregion
    #region -------------------------------------------------- STEP 6
    Debug.Log("[6]: Getting driver module")
    import importlib
    # try:
    module = importlib.import_module(f"Local.Drivers.{NameOfDeviceDriver}.Driver")
    # except:
        # Debug.Error(">>> Driver file crashes when loading.")
        # Debug.End()
        # return FileIntegrity.Corrupted
    #endregion
    #region -------------------------------------------------- STEP 7
    Debug.Log("[7]: Verifying Driver.py")
    try:
        Debug.Log(">>> CheckIntegrity")
        CheckIntegrity = getattr(module, "CheckIntegrity")

        Debug.Log(">>> CheckIntegrity")
        ClearProfileCache = getattr(module, "ClearProfileCache")

        Debug.Log(">>> Uninstall")
        Uninstall = getattr(module, "Uninstall")

        Debug.Log(">>> Update")
        Update = getattr(module, "Update")

        Debug.Log(">>> GetErrorMessage")
        GetErrorMessage = getattr(module, "GetErrorMessage")

        Debug.Log(">>> Quit")
        Quit = getattr(module, "Quit")

    except:
        Debug.Error(">>> Driver.py integrity is not functional")
        Debug.End()
        return FileIntegrity.Error
    #endregion

    Debug.End()
    return FileIntegrity.Good
# -------------------------------------------------------------------
def GetDrivers(NameOfDeviceDriver:str="") -> list:
    """
        GetDrivers:
        -----------
        This function returns a list of the device drivers downloaded
        on this Kontrol. It only returns the name of their folders in
        the form of a list of strings.
    """
    Debug.Start("GetDrivers")
    appPath = os.getcwd()
    appPath = AppendPath(appPath, f"/Local/Drivers")

    Debug.Log("Found drivers:")
    drivers = os.listdir(appPath)
    new_drivers = [s for s in drivers if '.' not in s]
    Debug.Log(new_drivers)
    Debug.End()

    return new_drivers
# -------------------------------------------------------------------
def GetJson(NameOfDeviceDriver:str="") -> JSONdata:
    """
        GetJson:
        ========
        Summary:
        --------
        This function is used to get the JSON data of a device driver.
        All you need to do is specify a deviceDriver name to this
        function.
    """
    Debug.Start("GetJson")

    Debug.Log("Checking if driver exist.")
    drivers = GetDrivers()
    if(NameOfDeviceDriver in drivers):
        Debug.Log(">>> SUCCESS")
        
        Debug.Log("Getting path")
        path = AppendPath(os.getcwd(), f"/Local/Drivers/{NameOfDeviceDriver}")

        Debug.Log("Checking if path is valid")
        valid = IsPathValid(path)
        if(valid):
            Debug.Log(">>> SUCCESS")

            Debug.Log("Getting JSON.")
            json = JSONdata(fileName="Config.json", path=path)
            Debug.Log(">>> SUCCESS")
            Debug.End()
            return json
        else:
            Debug.Error("-> PATH IS NOT VALID. FUNCTION RETURNED FALSE")
    else:
        Debug.Error("THE SPECIFIED DRIVER DOES NOT EXIST")
    Debug.End()
# -------------------------------------------------------------------
def Get_OSButton(jsonValue:str) -> MDIconButton:
    """
        Get_OSButton:
        =============
        Summary:
        --------
        Returns the OS button depending on the deviceDriver's
        Requirements JSON data value.
    """
    Debug.Start("Get_OSButton")
    icon = "blank"

    if(jsonValue == "Any"):
        Debug.Log("No icons required")
        Debug.End()
        return None
    else:
        if(jsonValue == "Windows"):
            icon = "microsoft-windows"
        elif(jsonValue == "Linux"):
            icon = "linux"
        elif(jsonValue == "ios"):
            icon = "apple-ios"
        elif(jsonValue == "apple"):
            icon = "apple"

    Debug.End()
    return MDIconButton(icon=icon)
# -------------------------------------------------------------------
def Get_ProcessorButton(jsonValue:str) -> MDIconButton:
    """
        Get_ProcessorButton:
        =============
        Summary:
        --------
        Returns the processor button depending on the deviceDriver's
        Requirements JSON data value.
    """
    Debug.Start("Get_ProcessorButton")
    icon = "blank"

    if(jsonValue == "Any"):
        Debug.Log("No icons required")
        Debug.End()
        return None
    else:
        if(jsonValue == "raspberry"):
            icon = "raspberry-pi"
        else:
            icon = "chip"

    Debug.End()
    return MDIconButton(icon=icon)
# -------------------------------------------------------------------
def Get_InternetButton(jsonValue:str) -> MDIconButton:
    """
        Get_InternetButton:
        =============
        Summary:
        --------
        Returns the processor button depending on the deviceDriver's
        Requirements JSON data value.
    """
    Debug.Start("Get_ProcessorButton")
    icon = "blank"

    if(jsonValue == False):
        Debug.Log("No icons required")
        Debug.End()
        return None
    else:
        icon = "server"

    Debug.End()
    return MDIconButton(icon=icon)
# -------------------------------------------------------------------
def Get_BluetoothButton(jsonValue:str) -> MDIconButton:
    """
        Get_BluetoothButton:
        =============
        Summary:
        --------
        Returns the processor button depending on the deviceDriver's
        Requirements JSON data value.
    """
    Debug.Start("Get_BluetoothButton")
    icon = "blank"

    if(jsonValue == False):
        Debug.Log("No icons required")
        Debug.End()
        return None
    else:
        icon = "bluetooth"

    Debug.End()
    return MDIconButton(icon=icon)
# -------------------------------------------------------------------
def Get_BrSpandButton(jsonValue:str) -> MDIconButton:
    """
        Get_BrSpandButton:
        =============
        Summary:
        --------
        Returns the processor button depending on the deviceDriver's
        Requirements JSON data value.
    """
    Debug.Start("Get_BrSpandButton")
    icon = "blank"

    if(jsonValue == False):
        Debug.Log("No icons required")
        Debug.End()
        return None
    else:
        icon = "expansion-card"

    Debug.End()
    return MDIconButton(icon=icon)
# -------------------------------------------------------------------
def Get_KontrolButton(jsonValue:str) -> MDIconButton:
    """
        Get_KontrolButton:
        =============
        Summary:
        --------
        Returns the processor button depending on the deviceDriver's
        Requirements JSON data value.
    """
    Debug.Start("Get_KontrolButton")
    icon = "blank"

    if(jsonValue == False):
        Debug.Log("No icons required")
        Debug.End()
        return None
    else:
        icon = "alpha-k-box"

    Debug.End()
    return MDIconButton(icon=icon)
# -------------------------------------------------------------------
def Get_OtherDeviceButton(jsonValue:str) -> MDIconButton:
    """
        Get_OtherDeviceButton:
        =============
        Summary:
        --------
        Returns the processor button depending on the deviceDriver's
        Requirements JSON data value.
    """
    Debug.Start("Get_OtherDeviceButton")
    icon = "blank"

    if(jsonValue == False):
        Debug.Log("No icons required")
        Debug.End()
        return None
    else:
        icon = "devices"

    Debug.End()
    return MDIconButton(icon=icon)
# -------------------------------------------------------------------
def GetFunction(functionName:str, driverName:str) -> Execution:
    """
        GetFunction:
        ============
        Summary:
        --------
        This function is used to get a general function from a
        device driver. Be sure you have checked the integrity of
        that device driver is good.

        Returns:
        --------
        This function returns a value from the `Execution` enum.
        If it returns `Execution.Pass`, the function was executed
        successfully.

        - `Execution.Crashed` = Failed to import Driver.py
        - `Execution.Failed` = Failed to import the function
        - function -> the function executed successfully.
    """
    Debug.Start("ExecuteFunction")

    Debug.Log(f"Getting module: {driverName}")
    import importlib
    try:
        module = importlib.import_module(f"Local.Drivers.{driverName}.Driver")
    except:
        Debug.Error("Driver crashed when importing.")
        Debug.End()
        return Execution.Crashed
    
    try:
        Debug.Log(f"Getting: {functionName}")
        function = getattr(module, functionName)
    except:
        Debug.Error(f"Function {functionName} could not be imported from {driverName}")
        Debug.End()
        return Execution.Failed


    Debug.End()
    return function
# -------------------------------------------------------------------
def DeleteDriver(deviceDriver:str) -> Execution:
    """
        DeleteDriver:
        =============
        Summary:
        --------
        This attempts to delete a specific device driver
        based off its name given as an argument to this
        function.

        Arguments:
        ----------
        - `deviceDriver:str` = name of the device driver to delete. Must be the name of the git repository it got downloaded from.

        Returns:
        --------
        - `Execution.Passed` = Driver deleted.
        - `Execution.Unecessary` = The driver cannot be deleted cuz it doesn't exist.
        - `Execution.Failed` = Something went wrong and we couldn't delete that driver.
    """
    Debug.Start("DeleteDriver")

    installedDrivers = GetDrivers()
    if(deviceDriver not in installedDrivers):
        Debug.Log(f"{deviceDriver} isn't a valid, installed device driver.")
        Debug.End()
        return Execution.Failed

    path = os.getcwd()
    pathToDriver = AppendPath(path, f"/Local/Drivers/{deviceDriver}")

    try:
        os.remove(pathToDriver)
    except:
        Debug.Error("failed to os.remove the folder.")

        rmtree(pathToDriver)
        Debug.Log("Success")

    Debug.End()
    return Execution.Passed
#====================================================================#
# Classes
#====================================================================#

#====================================================================#
LoadingLog.End("deviceDriver.py")