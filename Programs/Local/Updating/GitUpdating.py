#====================================================================#
# File Information
#====================================================================#
"""
    GitUpdating.py
    =============
    This file contains BRS Kontrol's specific functions used to update
    and download new versions of itself.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Programs.Pages.DownloadProgress import DownloadProgress_Screens
LoadingLog.Start("GitUpdating.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import os
import subprocess
import asyncio
import git
import threading
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Network.APIs.GitHub import GitHub, ManualGitHub, DownloadRepositoryAtPath
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import("KivyMD")
from kivymd.uix.progressbar import MDProgressBar
#endregion
LoadingLog.Import("Local")
from ...Pages.PopUps import PopUpsHandler, PopUpTypeEnum
#====================================================================#
# Functions
#====================================================================#
# ----------------------------------------------------------------
def CreateUpdatePopUp(cancelHandler=None) -> Execution:
    """
        CreateUpdatePopUp
        =================
        Summary:
        --------
        This function is used to create and queue a specific
        pop up displayed to the user when their Kontrol version
        is out of date. This pop up prompts the user with a 
        simple question asking them if they want to update their
        Kontrol or not.

        If they click on Yes, they will be taken to the update page
        otherwise, pop ups will exit to their caller screen.

        Args:
        --------
        - `cancelHandler`: screen handler that will be called if the user cancels

        Returns:
        --------
        - `Execution.Passed` = pop up created
        - `Execution.Unecessary` = git versions matched
        - `Execution.Failed` = Not enough git api requests left
    """
    Debug.Start("CreateUpdatePopUp")

    Debug.Log("Getting Kontrol versions")
    if(ManualGitHub.GetRequestsLeft() > 5):
        newVersion = GitHub.LatestTag
        currentVersion = GitHub.CurrentTag
        if(newVersion != currentVersion):
            Debug.Log("Creating pop up")
            PopUpsHandler.Add(Icon="update",
                              Message=(_("Do you want to update Kontrol to its latest version?") + ("\nYour version: ") + currentVersion + _("\nNew version: ") + newVersion),
                              CanContinue=True,
                              Type=PopUpTypeEnum.Custom,
                              ButtonAText=_("Update"),
                              ButtonBText=_("Cancel"),
                              ButtonAHandler=DownloadProgress_Screens,
                              ButtonBHandler=cancelHandler
                              )
        else:
            Debug.Error("Versions match.")
            return Execution.Unecessary
    else:
        Debug.Error("Not enough API requests left to update Kontrol")
        Debug.End()
        return Execution.Failed

    Debug.End()
    return Execution.Passed
# ----------------------------------------------------------------
def DownloadLatestVersion(progressBar:MDProgressBar, DownloadProgressHandler) -> Execution:
    """
        DownloadLatestVersion.py
        ========================
        Summary:
        --------
        This function will create a new folder where Kontrol's
        Git folder is located. It will then download using
        git terminal functions the new version of Kontrol
        in that folder. Doing so ensures that if Kontrol could
        not be fully downloaded, the old version is not lost.

        The name of that folder will be the name of the latest
        release of Kontrol.

        Args:
        -------
        - `progressBar` : MDProgressbar updated by download functions running asynchronously. This way your kivy app gets a live update of the download's progression.
        - `FailedDownload` : Function executed if the download fails
        - `GoodDownload` : Function to execute if the download works

        Returns:
        -------
        - `Execution.Passed` = Kontrol was successfully downloaded in a new folder
        - `Execution.Failed` = Kontrol failed to download a new version for X reason.
        - `Execution.NoConnection` = Kontrol failed to download because internet is not available
    """
    Debug.Start("DownloadLatestVersion")

    currentPath = os.getcwd()
    parentPath = currentPath.rstrip(os.path.basename(currentPath))
    Debug.Log(f"Parent folder: {parentPath}")

    Debug.Log("Creating new folder")
    directoryName = GitHub.LatestTag
    directoryName = "0.0.0"
    directoryPath = os.path.join(parentPath, directoryName)
    Debug.Log(f"New folder's path: {directoryPath}")

    try:
        os.mkdir(directoryPath)
        Debug.Log("Success: Directory created")
    except:
        Debug.Error(f"Failed to create directory with name: {directoryName}")
        Debug.End()
        return Execution.Failed

    Debug.Log("Downloading Kontrol in new folder")
    Debug.End()
    return DownloadRepositoryAtPath("https://github.com/LyamBRS/BRS-Kontrol.git", directoryPath, progressBar, DownloadProgressHandler)


LoadingLog.End("GitUpdating.py")