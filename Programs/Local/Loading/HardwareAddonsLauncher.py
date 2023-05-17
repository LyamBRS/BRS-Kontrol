#====================================================================#
# File Information
#====================================================================#
"""
    HardwareAddonsLauncher.py
    =========================
    This file contains functions used to automatically
    start all the hardware addons of your Kontrol device.

    An hardware addon is NOT A DEVICE and is NOT A BRSPAND CARD.
    An hardware addon is added directly on Kontrol's PCB such as the
    ADXL343 accelerometer.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("HardwareAddonsLauncher.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import os
import importlib.util
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import('KivyMD')
#endregion
from Programs.Pages.PopUps import PopUpTypeEnum, PopUpsHandler
#====================================================================#
# Functions
#====================================================================#
def InitializeAllHardwareAddons(CreatePopUps:bool = False) -> Execution:
    """
        InitializeAllHardwareAddons:
        ============================
        Summary:
        --------
        This function will attempt to gather all the
        hardware addons you have installed in your Kontrol
        and launch them. See the official documentation to
        understand what an hardware addon is.

        Arguments:
        ----------
        - `CreatePopUps:bool` If false, no pop ups will be created from executing this.

        Returns:
        --------
        - `Execution.Passed` : All addons were launched and added to the application.
        - `Execution.Unecessary` : No addons are installed on your Kontrol.
        - `failedAddons` : List of addons that failed to launch.
    """
    Debug.Start("InitializeAllHardwareAddons")
    
    Debug.Log("Getting path of addons folder")
    pathToAddons = os.getcwd()
    pathToAddons = AppendPath(pathToAddons, "/Local/Hardware")

    Debug.Log("Fetching installed hardware addons")
    installedAddons = GetNamesOfInstalledAddons(pathToAddons)
    if(len(installedAddons) == 0):
        Debug.Warn("Your Kontrol does not have any hardware addons installed. Please install some if you think its an error.")
        Debug.End()
        return Execution.Unecessary

    Debug.Log("Launching found addons...")
    for addon in installedAddons:
        result = LaunchAddonAtPath(addon, pathToAddons)
        if(result != Execution.Passed):
            Debug.Warn(f"Seems like {addon} failed to launch.")

            if(CreatePopUps == True):
                CreatePopUpMessage(addon, result)
    Debug.End()
#====================================================================#
def GetNamesOfInstalledAddons(pathToAddons:str) -> list:
    """
        GetNamesOfInstalledAddons:
        ==========================
        Summary:
        --------
        Returns a list of all the hardware addons
        folder's names.
    """
    Debug.Start("GetNamesOfInstalledAddons")

    Debug.Log("Finding folders at that path...")
    subdirectories = [name for name in os.listdir(pathToAddons) if os.path.isdir(os.path.join(pathToAddons, name))]

    Debug.Log(f"Found installed addons: {subdirectories}")
    Debug.End()
    return subdirectories
#====================================================================#
def LaunchAddonAtPath(nameOfAddon:str, pathOfAddonsFolder:str):
    """
        LaunchAddonAtPath:
        ==================
        Summary:
        --------
        Launches a specified addon at a 
        specified path.

        Returns:
        --------
        - `Execution.Passed` = Addon launched successfully and is now accessible through the Addons class.
        - `Execution.Failed` = Addon failed to launch.
        - `Execution.Incompatibility` = Addon cannot launch on your device.
        - `Execution.Unecessary` = Addon is already running on your device.
    """
    Debug.Start("LaunchAddonAtPath")

    Debug.Log(f"Trying to launch {nameOfAddon}...")

    # Append driver.py to specified path.
    pathOfAddonsDriver = os.path.join(pathOfAddonsFolder, nameOfAddon, "driver.py")

    Debug.Log(f"Start of {nameOfAddon}'s compiling...")
    if(os.path.isfile(pathOfAddonsDriver)):
        addonsModule = nameOfAddon
        addonsClass = nameOfAddon

        # Dynamically load the module
        specifications = importlib.util.spec_from_file_location(addonsModule, pathOfAddonsDriver)
        module = importlib.util.module_from_spec(specifications)
        specifications.loader.exec_module(module)

        # Does the class exist within that module?
        if (hasattr(module, addonsClass)):
            addonsClassObject = getattr(module, addonsClass)
            if(hasattr(addonsClassObject, "Launch")):
                result = addonsClassObject.Launch()
                if(result != Execution.Passed):
                    Debug.Error(f"{nameOfAddon} failed to launch with error code: {result}")
                    Debug.End()
                return result
            else:
                Debug.Error(f"{nameOfAddon}'s class did not have a Launch method")
                Debug.End()
                return Execution.Failed
        else:
            Debug.Error(f"{nameOfAddon}'s driver.py did not have a class named {addonsClass}")
            Debug.End()
            return Execution.Failed
    else:
        Debug.Error(f"Failed to get {nameOfAddon}'s driver.py")
        Debug.End()
        return Execution.Failed
#====================================================================#
def CreatePopUpMessage(nameOfTheAddon:str, executionReturnedByLaunch:Execution) -> Execution:
    """
        CreatePopUpMessage:
        ===================
        Summary:
        --------
        This function will create a normalized pop up containing
        informations about why that addon couldn't execute.
    """
    Debug.Start("CreatePopUpMessage")

    if(executionReturnedByLaunch == Execution.Crashed):
        PopUpsHandler.Add(PopUpTypeEnum.FatalError, Message=_("A critical error occured when Kontrol attempted to launch the following hardware extension addon: ") + nameOfTheAddon)
        Debug.Log("Pop up created")
        Debug.End()
        return Execution.Passed
    
    if(executionReturnedByLaunch == Execution.Failed):
        PopUpsHandler.Add(PopUpTypeEnum.Warning, Message=_("The following hardware extension addon failed to launch for some reasons: ") + nameOfTheAddon)
        Debug.Log("Pop up created")
        Debug.End()
        return Execution.Passed
    
    if(executionReturnedByLaunch == Execution.Incompatibility):
        PopUpsHandler.Add(PopUpTypeEnum.Warning, Message=_("The following hardware extension addon cannot operate on your hardware: ") + nameOfTheAddon)
        Debug.Log("Pop up created")
        Debug.End()
        return Execution.Passed
    
    if(executionReturnedByLaunch == Execution.NoConnection):
        PopUpsHandler.Add(PopUpTypeEnum.Warning, Message=_("The following hardware extension addon failed to launch due to a connection error: ") + nameOfTheAddon)
        Debug.Log("Pop up created")
        Debug.End()
        return Execution.Passed
    
    if(executionReturnedByLaunch == Execution.ByPassed):
        PopUpsHandler.Add(PopUpTypeEnum.FatalError, Message=_("The following hardware extension addon bypassed its launch function: ") + nameOfTheAddon)
        Debug.Log("Pop up created")
        Debug.End()
        return Execution.Passed
    
    if(executionReturnedByLaunch == Execution.Unecessary):
        PopUpsHandler.Add(PopUpTypeEnum.Warning, Message=_("The following hardware extension addon said it was unecessary to launch it when Kontrol attempted to do so: ") + nameOfTheAddon)
        Debug.Log("Pop up created")
        Debug.End()
        return Execution.Passed

    Debug.Log("Seems like you called this function for nothing...")
    Debug.Warn(f"This function does not support pop ups for executions of type: {executionReturnedByLaunch}")
    Debug.End()
    return Execution.ByPassed
#====================================================================#
# Classes
#====================================================================#
# class Example:
    # region   --------------------------- DOCSTRING
    # ''' This class is a reference style class which represents the current state that a device can be in.
        # A device can be GUI or hardware.
        # You don't have to use this class when defining the state of a device, but it is more convenient than
        # memorizing all the numbers associated by heart.
    # '''
    # endregion
    # region   --------------------------- MEMBERS
    # fakeVar : type = "sus"
    # ''' It's ugly docstring which for some annoying reason is below whatever it needs to explain... Which is hideous and hard to follow. No humans read data from bottom to top bruh.'''
    # endregion
    # region   --------------------------- METHODS
    # endregion
    # region   --------------------------- CONSTRUCTOR
    # endregion
    # pass
#====================================================================#
LoadingLog.End("HardwareAddonsLauncher.py")