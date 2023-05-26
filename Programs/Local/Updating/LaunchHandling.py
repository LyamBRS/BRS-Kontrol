#====================================================================#
# File Information
#====================================================================#
"""
    LaunchHandling.py
    =================
    This file contains what's necessary to handle the launch of the
    new version of Kontrol after it has been installed successfully.
"""
#====================================================================#
# Loading Logs
#====================================================================#
import subprocess
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
# from Programs.Pages.DownloadProgress import DownloadProgress_Screens
LoadingLog.Start("LaunchHandling.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import os
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Network.APIs.GitHub import GitHub, ManualGitHub, DownloadRepositoryAtPath
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import GetFolderFromPath, GetParentPath
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import("KivyMD")
from kivymd.app import MDApp
#endregion
LoadingLog.Import("Local")
from ...Pages.PopUps import PopUpsHandler, PopUpTypeEnum
#====================================================================#
# Classes
#====================================================================#

class Shutdown():
    """
        Shutdown:
        =======================
        Summary:
        --------
        This static class holds a singular variable meant to indicate
        to the application during shutdown that it needs to perform
        a special task.
    """
    def ShutdownFunction():
        """
            ShutdownFunction:
            =================
            Summary:
            --------
            This function's purpose is to execute when the app
            closes. By default it is empty.
        """
        pass

    newAppPath:str = None
    """
        Holds the path to the new application for the shutdown function.
        Defaults to `None`.
    """

    scheduleKontrolForShutdown:bool = False
    """
        scheduleKontrolForShutdown:
        ===========================
        Summary:
        --------
        member that defines if Kontrol should
        shutdown itself when the quit button is pressed
        in its toolbar. Defaults to `False`
    """

    def Kontrol():
        """
            Kontrol:
            ========
            Summary:
            --------
            Tries to shutdown Kontrol at the very very
            end of the application's execution.
        """
        if(Shutdown.scheduleKontrolForShutdown and Information.platform == "Linux"):
            command = "sudo shutdown -h now"
            subprocess.run(command, shell=True)
#====================================================================#
# Functions
#====================================================================#
def CreateLaunchNewAppPopUp() -> Execution:
    """
        CreateLaunchNewAppPopUp:
        ========================
        Summary:
        --------
        This function creates and handles the pop up which is
        displayed to the user asking them if they want to quit
        and launch the new application.

        `Attention`:
        ----------
        - This function does not clear the pop up queue
        - This function does not set up `PopUp_screens`
    """
    Debug.Start("CreateLaunchNewAppPopUp")

    PopUpsHandler.Add(Type = PopUpTypeEnum.Question,
                      Message=_("Do you want to quit this version and launch the newly installed version?"),
                      ButtonAText=_("Yes"),
                      ButtonAHandler=QuitAndLaunchNewApp)

    Debug.End()
    return Execution.Passed
# ----------------------------------------------------------------
def CreateTransferDataPopUp(cancelHandler) -> Execution:
    """
        CreateTransferDataPopUp:
        ========================
        Summary:
        --------
        This function creates a pop up which is displayed to the
        user asking them if they want to transfer the data of this
        version to the newly, freshly installed version.

        `Attention`:
        ----------
        - This function does not clear the pop up queue
        - This function does not set up `PopUp_screens`
    """
    Debug.Start("CreateTransferDataPopUp")
    PopUpsHandler.Add(Type = PopUpTypeEnum.Question,
                      Message=_("Do you wish to transfer profiles, device drivers and BrSpand drivers to the new version?"),
                      )
    Debug.End()
    return Execution.Passed
# ----------------------------------------------------------------
def HandleDataTransfer() -> Execution:
    """
        HandleDataTransfer:
        ===================
        Summary:
        --------
        This function transfers every downloaded
        things to the new version of Kontrol installed previously.
        it will transfer:
        - Profiles
        - Device Drivers
        - BrSpand card drivers

        Returns:
        --------
        - `Execution.Passed` : Transfer is successful
        - `Execution.Unecessary` : Nothing to transfer to the new version
        - `Execution.Failed` : Some transfers could not be executed.
    """
    Debug.Start("HandleDataTransfer")
    Debug.End()
# ----------------------------------------------------------------
def QuitAndLaunchNewApp(*args) -> Execution:
    """
        QuitAndLaunchNewApp:
        ====================
        Summary:
        --------
        This function attempts to quit and sets a flag to true
        so Application.py launches the new application.

        This function will add the necessary pop ups automatically.

        `Attention`:
        ------------
        - This function does not clear pop ups
        - This function does NOT handle PopUps_Screens
        - This should be the last function you call.
    # """
    Debug.Start("QuitAndLaunchNewApp")
    from Programs.Local.Updating.GitUpdating import GetInstalledKontrolVersions
    Debug.Log("Checking if multiple versions installed")
    installedVersions = GetInstalledKontrolVersions()
    if(installedVersions == Execution.Unecessary):
        Debug.Error("No other versions are installed")
        PopUpsHandler.Add(Type=PopUpTypeEnum.FatalError,
                          Message=_("No other versions appears to be installed. Kontrol failed to launch a newly downloaded version."))
        Debug.End()
        return Execution.Failed

    if(installedVersions == Execution.Failed):
        Debug.Error("No other versions are installed")
        PopUpsHandler.Add(Type=PopUpTypeEnum.FatalError,
                          Message=_("A fatal error occured while attempting to get installed instances of Kontrol. You will need to manually launch the new version installed."))
        Debug.End()
        return Execution.Failed

    if(len(installedVersions) > 2):
        Debug.Error("Too many versions of Kontrol found.")
        PopUpsHandler.Add(Type=PopUpTypeEnum.FatalError,
                          Message=_("Too many versions of Kontrol were found to automatically find the newly installed version. Please launch it manually, or reboot and accept automatic deleting of other versions."))
        Debug.End()
        return Execution.Failed

    Debug.Log("Newly installed instance is accessible.")

    Debug.Log("Getting path to new folder.")
    currentVersion = GetFolderFromPath(os.getcwd())
    newPath = None
    for version in installedVersions:
        if(version != currentVersion):
            newPath = GetParentPath(os.getcwd()) + version

    if(newPath == None):
        Debug.Error("Failed to create path to new version")
        PopUpsHandler.Add(Type=PopUpTypeEnum.FatalError,
                          Message=_("Kontrol failed to get the path of the newly installed Kontrol version. Please launch it manually or uninstall it."))
        Debug.End()
        return Execution.Failed

    Debug.Log(f"path found: {newPath}")
    Shutdown.newAppPath = newPath
    Debug.Log("Checking if Application.py is available")
    files = os.listdir(newPath)
    if "Application.py" in files:
        Debug.Log("Success")
    else:
        Debug.Error("Application.py could not be found in the newly installed version of Kontrol.")
        PopUpsHandler.Add(Type=PopUpTypeEnum.FatalError,
                          Message=_("The newly installed version of Kontrol is missing key files and cannot be launched. It may be corrupted or too different from this one. Please attempt to launch it manually."))
        Debug.End()
        return Execution.Failed

    Debug.Log("Configurating Shutdown class.")
    # Shutdown.newAppPath = newPath
    Shutdown.ShutdownFunction = _AppShutDownFunction

    Debug.Log("Shutting down KivyMD application.")
    app = MDApp.get_running_app().stop
    Debug.End()
    return Execution.Passed
# ----------------------------------------------------------------
def _AppShutDownFunction(*args) -> Execution:
    Debug.Start("_AppShutDownFunction")

    if(Shutdown.newAppPath == None):
        Debug.Error("FAILED TO LAUNCH NEW APP DUE TO NO PATH BEING SPECIFIED")
    else:
        os.chdir(Shutdown.newAppPath)
        result = subprocess.run(['python', "Application.py"])

    Debug.End()
LoadingLog.End("LaunchHandling.py")