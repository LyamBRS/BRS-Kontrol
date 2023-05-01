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
import shutil
from git import rmtree
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
                              ButtonAHandler=DownloadProgress_Screens.Call,
                              ButtonBHandler=cancelHandler.Call
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
        DownloadLatestVersion
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
    parentPath = GetParentPath(currentPath)
    Debug.Log(f"Parent folder: {parentPath}")

    Debug.Log("Creating new folder")
    directoryName = GitHub.LatestTag
    directoryPath = os.path.join(parentPath, directoryName)
    Debug.Log(f"New folder's path: {directoryPath}")

    try:
        os.mkdir(directoryPath)
        Debug.Log("Success: Directory created")
    except:
        Debug.Error(f"Failed to create directory with name: {directoryName}")
        DownloadProgressHandler.FailedDownload()
        Debug.End()
        return Execution.Failed

    Debug.Log("Downloading Kontrol in new folder")
    Debug.End()
    return DownloadRepositoryAtPath("https://github.com/LyamBRS/BRS-Kontrol.git", directoryPath, progressBar, DownloadProgressHandler)
# ----------------------------------------------------------------
def CreateDeleteOldVersionPopUp(cancelHandler=None) -> Execution:
    """
        CreateDeleteOldVersionPopUp:
        ============================
        Summary:
        --------
        Creates a pop up question that asks the user if they want
        to delete old versions of Kontrol located on their devices.

        An old version is detected if other folders are found in
        the parent folder that holds your Kontrol repository.
        Make sure that the folder is called "`BRS_Kontrol`".

        Arguments:
        ----------
        - `cancelHandler`: screen handler that will be called if the user cancels

        `Attention`:
        ----------
        Make sure the parent folder of your repository is called
        "`BRS_Kontrol`"
    """
    Debug.Start("CreateDeleteOldVersionPopUp")

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
                              ButtonAHandler=DownloadProgress_Screens.Call,
                              ButtonBHandler=cancelHandler.Call
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
def VerifyKontrolParentFolder() -> Execution:
    """
        VerifyKontrolParentFolder:
        ==========================
        Summary:
        --------
        Internal function which allows a quick verification
        of the parent folder that holds the current
        Kontrol repository.

        Returns:
        --------
        - `Execution.Passed`: Parent folder is correct
        - `Execution.Failed` : Parent folder is incorrect
    """
    Debug.Start("VerifyKontrolParentFolder")

    currentPath = os.getcwd()
    parentPath = GetParentPath(currentPath)
    parentFolder = GetFolderFromPath(parentPath)
    if(parentFolder == "BRS_Kontrol"):
        Debug.Log("valid parent folder")
        Debug.End()
        return Execution.Passed
    else:
        Debug.Error("Parent folder was not BRS_Kontrol.")
        Debug.End()
        return Execution.Failed
# ----------------------------------------------------------------
def GetInstalledKontrolVersions() -> Execution:
    """
        GetInstalledKontrolVersions:
        ==========================
        Summary:
        --------
        This function automatically scans for other
        versions of Kontrol downloaded on your device.
        If any are detected, a list of all of them
        is returned including the currently running one.

        `Returns`:
        ----------
        - `(list)` = List of all the found versions
        - `Execution.Failed` = Something failed when trying to get versions.
        - `Execution.Unecessary` = No other files or folder inside of parent folder.

        `Attention`:
        ----------
        For this function to work, your repository needs to
        be in a folder called `"BRS_Kontrol"`. If this is not
        the case, older versions of Kontrol will stay
        downloaded and you won't be able to automatically
        delete them when your application starts.
    """
    Debug.Start("GetInstalledKontrolVersions")

    Debug.Log("Checking parent folder...")
    result = VerifyKontrolParentFolder()
    if(result == Execution.Passed):
        Debug.Log(">>> SUCCESS")
    else:
        Debug.Error("Parent folder failed verification.")
        Debug.End()
        return Execution.Failed

    Debug.Log("Gathering all versions...")
    currentVersion = GetFolderFromPath(os.getcwd())
    parentContents = os.listdir(GetParentPath(os.getcwd()))

    if(len(parentContents) == 1):
        Debug.Log("No other versions installed on your device")
        Debug.End()
        return Execution.Unecessary
    else:
        for content in parentContents:
            if(content != currentVersion):
                Debug.Log(f">>> Found: {content}")

        Debug.Error("Other versions are installed on your device")
        Debug.End()
        return parentContents
# ----------------------------------------------------------------
def _DeleteOtherKontrolVersions(*args) -> Execution:
    """
        _DeleteOtherKontrolVersions:
        ===========================
        Summary:
        --------
        This function deletes any other versions
        than the currently running one.

        Returns:
        --------
        - `Execution.Passed`: Other versions deleted successfully.
        - `Execution.Unecessary` : No other versions to delete.
        - `Execution.Failed` : Failed to delete other versions.
    """
    Debug.Start("_DeleteOtherKontrolVersions")

    Debug.Log("Checking Parent folder...")
    result = VerifyKontrolParentFolder()
    if(result == Execution.Failed):
        Debug.Error(">>> VerifyKontrolParentFolder failed.")
        Debug.End()
        return Execution.Failed
    Debug.Log(">>> PASS")

    Debug.Log("Checking if there is content to delete")
    installedVersions = GetInstalledKontrolVersions()
    if(installedVersions == Execution.Failed):
        Debug.Error("Nothing to delete")
        Debug.End()
        return Execution.Unecessary
    Debug.Log(">>> THINGS TO DELETE FOUND")

    runningVersion = GetFolderFromPath(os.getcwd())

    Debug.Log(f"Other versions: {installedVersions}")
    Debug.Log(f"Running version: {runningVersion}")

    if(runningVersion in installedVersions):
        Debug.Log("Starting deleting process")
        for version in installedVersions:
            if(version != runningVersion):
                versionPath = GetParentPath(os.getcwd()) + version
                Debug.Log(f">>> Deleting: {version} ...")

                # try:
                Debug.Log(f"Trying to remove: {versionPath}")
                rmtree(versionPath)
                Debug.Log(">>> DELETED")
                # except:
                    # Debug.Error(f"Failed to delete: {version}")
                    # PopUpsHandler.Add(Type=PopUpTypeEnum.FatalError,
                                    #   Message=_("Kontrol failed to delete the following version: ")+version)
    else:
        Debug.Error("Running version not found in list of installed versions.")
        Debug.Error(f"List of versions: {installedVersions}")
        Debug.End()
        return Execution.Failed

    Debug.End()
    return Execution.Passed
# ----------------------------------------------------------------
def HandleOldVersionsDeleting() -> Execution:
    """
        HandleOldVersionsDeleting:
        ==========================
        Summary:
        --------
        This function's purpose is to handle the various levels
        of interactions required to successfully delete old
        Kontrol versions installed on your device granted you
        initially installed Kontrol by executing a setup.py file.

        `Attention`:
        ------------
        - This function should only be called in `AppLoadingHandler.py`
        - This function automatically add pop ups.
        - This function does not clear the pop up list.

        Returns:
        --------
        - `Execution.Failed` : Failed to handle deletion of old versions
        - `Execution.Passed` : Deletions are ready to be handled
        - `Execution.Unecessary` : No files to delete, no pop ups created.
    """
    Debug.Start("HandleOldVersionsDeleting")

    versions = GetInstalledKontrolVersions()
    if(versions == Execution.Failed):
        PopUpsHandler.Add(Type=PopUpTypeEnum.FatalError,
                          Icon="folder-alert",
                          Message=_("Kontrol failed to check for older installed versions. Please ensure that your installation is correct."),
                          ButtonAText="Ok")
        Debug.Error("Failed to get installed Kontrol versions.")
        Debug.End()
        return Execution.Failed

    if(versions == Execution.Unecessary):
        Debug.Log("No other versions installed.")
        Debug.End()
        return Execution.Unecessary

    if(len(versions) > 1):
        PopUpsHandler.Add(Type=PopUpTypeEnum.Custom,
                          Icon="folder-multiple",
                          Message=_("Multiple versions of Kontrol are installed. Do you wish to delete them?"),
                          ButtonAText=_("Yes"),
                          ButtonBText=_("No"),
                          ButtonAHandler=_DeleteOtherKontrolVersions,
                          ButtonBHandler=None)

    Debug.Log("Success")
    Debug.End()
    return Execution.Passed

LoadingLog.End("GitUpdating.py")