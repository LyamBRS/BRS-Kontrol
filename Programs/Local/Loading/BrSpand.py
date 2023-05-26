#====================================================================#
# File Information
#====================================================================#
"""
    BrSpand.py
    =========================
    This file contains whats necessary to handle BFIO
    drivers such as launching them, stopping them, checking if
    they are downloaded, listing them and much more.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("BrSpand.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import os
import importlib.util
import subprocess
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
from Libraries.BRS_Python_Libraries.BRS.Utilities.addons import Addons
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
from kivy.clock import Clock
#endregion
#region ------------------------------------------------------ KivyMD
# LoadingLog.Import('KivyMD')
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

    Debug.Log("Starting periodic updater callback.")
    Clock.schedule_once(PeriodicCallbackExecuter, 5)
    Debug.End()
#====================================================================#
def InstalledBrSpandCards() -> list:
    """
        GetNamesOfInstalledBrSpandCards:
        ================================
        Summary:
        --------
        Returns a list of all the installed BrSpand cards.
    """
    Debug.Start("GetNamesOfInstalledBrSpandCards")
    path = PathToBrSpandDrivers()
    Debug.Log("Finding folders at that path...")
    subdirectories = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

    Debug.Log(f"Found installed addons: {subdirectories}")
    Debug.End()
    return subdirectories
#====================================================================#
def LaunchBrSpandAtPath(nameOfBrSpandCard:str, pathToTheBrSpandDrivers:str):
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
    Debug.Start("LaunchBrSpandAtPath")

    Debug.Log(f"Trying to launch {nameOfBrSpandCard}...")

    # Append driver.py to specified path.
    pathOfAddonsDriver = os.path.join(pathToTheBrSpandDrivers, nameOfBrSpandCard, "driver.py")

    Debug.Log(f"Start of {nameOfBrSpandCard}'s compiling...")
    if(os.path.isfile(pathOfAddonsDriver)):
        addonsModule = nameOfBrSpandCard
        addonsClass = nameOfBrSpandCard

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
                    Debug.Error(f"{nameOfBrSpandCard} failed to launch with error code: {result}")
                    Debug.End()
                return result
            else:
                Debug.Error(f"{nameOfBrSpandCard}'s class did not have a Launch method")
                Debug.End()
                return Execution.Failed
        else:
            Debug.Error(f"{nameOfBrSpandCard}'s driver.py did not have a class named {addonsClass}")
            Debug.End()
            return Execution.Failed
    else:
        Debug.Error(f"Failed to get {nameOfBrSpandCard}'s driver.py")
        Debug.End()
        return Execution.Failed
#====================================================================#
def PathToBrSpandDrivers() -> str:
    """
        PathToBrSpandDrivers:
        =====================
        Summary:
        --------
        Gets you the path to the BrSpand drivers.
    """
    Debug.Start("PathToBrSpandDrivers")
    pathToDrivers = os.getcwd()
    pathToDrivers = AppendPath(pathToDrivers, "/BrSpand/Drivers")
    Debug.End()
    return pathToDrivers
#====================================================================#
def IsCardDriversInstalled(nameOfTheCard:str):
    """
        IsCardDriversInstalled:
        =======================
        Summary:
        --------
        Checks if a BrSpand card's drivers
        are installed on your machine.
    """
    Debug.Start("IsCardDriversInstalled")

    installedCards = InstalledBrSpandCards()
    if(nameOfTheCard in installedCards):
        Debug.Log(f"{nameOfTheCard}'s drivers are installed on your device.")
        Debug.End()
        return Execution.Passed
    else:
        Debug.Error(f"{nameOfTheCard} is not installed on your device.")
        Debug.End()
        return Execution.Failed
#====================================================================#
def InstallCardsDrivers(nameOfTheCard:str, gitRepoURL:str) -> Execution:
    """
        InstallCardsDrivers:
        ====================
        Summary:
        --------
        Clones a Git repository from the specified URL to the desired folder path with a specific name.
        
        Arguments:
        ----------
        - gitRepoURL (str): The URL of the Git repository.
        - nameOfTheCard (str): The desired name for the cloned repository folder.
        
        Returns:
        --------
        - `Execution.Passed`: The cloning process succeeded.
        - `Execution.Failed`: The cloning process failed.
    """
    try:

        pathToDrivers = PathToBrSpandDrivers()
        pathToRepository = AppendPath(pathToDrivers, f"/{nameOfTheCard}")

        if(os.path.exists(pathToRepository)):
            try:
                from git import rmtree
                rmtree(pathToRepository)
            except:
                Debug.Error("Failed to delete old repository.")
                Debug.End()
                return Execution.Crashed

        # Clone the repository using the git command-line tool
        result = subprocess.run(['git', 'clone', gitRepoURL, pathToRepository])
        if(result.returncode == 0):
            Debug.Log(">>> SUCCESS")
        else:
            Debug.Error("Failed to download BrSpand drivers.")
            Debug.End()
            return Execution.Failed

        Debug.End()
        return Execution.Passed
    except subprocess.CalledProcessError:
        # An error occurred during the cloning process
        Debug.Error("Subprocesses failed")
        Debug.End()
        return Execution.Failed
#====================================================================#
LoadingLog.End("BrSpand.py")