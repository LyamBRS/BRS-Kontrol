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
#endregion
#region ------------------------------------------------------ KivyMD
# LoadingLog.Import('KivyMD')
#endregion
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
def LaunchBrSpandAtPath(nameOfBrSpandCard:str):
    """
        LaunchBrSpandAtPath:
        ====================
        Summary:
        --------
        Launches a specified BrSpand Card at a 
        specified path.

        Returns:
        --------
        - `Execution.Passed` = Card launched successfully and is now accessible through the Cards class.
        - `Execution.Failed` = Card failed to launch.
        - `Execution.Incompatibility` = Card cannot launch on your device.
        - `Execution.Unecessary` = Card is already running on your device.
    """
    Debug.Start("LaunchBrSpandAtPath")

    Debug.Log(f"Trying to launch {nameOfBrSpandCard}...")

    # Append driver.py to specified path.
    pathOfAddonsDriver = AppendPath(PathToBrSpandDrivers, str(f"/{nameOfBrSpandCard}/"))
    pathOfAddonsDriver = AppendPath(pathOfAddonsDriver, "driver.py")



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