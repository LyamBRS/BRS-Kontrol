#====================================================================#
# File Information
#====================================================================#
"""
    SelfCheck.py
    =============
    Summary:
    --------
    This file contains functions specific to Driver.py that allows
    it to correctly perform an in depth check of it's own integrity.

    Functions:
    ----------
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("SelfCheck.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution, FileIntegrity
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import CompareList
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import('KivyMD')
#endregion
#====================================================================#
# Variables
#====================================================================#

#====================================================================#
# Functions
#====================================================================#
def CheckContent() -> FileIntegrity:
    """
        CheckContent:
        =============
        Summary:
        --------
        This function compares all the folders and sub folders of this
        device driver for any problems or mismatches or unexpected
        data.

        Returns:
        --------
        Returns a value from the `FileIntegrity` enumeration.
    """
    Debug.Start("CheckFolders")
    #region ------------------------------------- [0]
    import os
    from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath, CompareList
    from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
    from Local.Drivers.Debugger.Driver import variables
    #endregion
    #region ------------------------------------- [1]
    Debug.Log("[0]: Defining variables")

    exceptions = [
        "__pycache__"
    ]

    wantedMainContent = [
        "Libraries",
        "Local",
        "Pages",
        "Programs",
        "__init__.py",
        "Config.json",
        "Driver.py"
    ]

    wantedLibraryContent = [
        "Backgrounds"
    ]

    wantedPagesContent = [
        "DebuggerMenu.py"
    ]

    wantedLocalContent = [
        "Cache",
        "Languages",
        "Profiles"
    ]

    wantedProgramContent = [
        "FileHandler"
    ]
    #endregion
    #region ------------------------------------- [2]
    Debug.Log("[1]: Getting paths")
    mainContentPath     = AppendPath(os.getcwd(),       "/Local/Drivers/Debugger/")
    libraryContentPath  = AppendPath(mainContentPath,   "Libraries/")
    localContentPath    = AppendPath(mainContentPath,   "Local/")
    pagesContentPath    = AppendPath(mainContentPath,   "Pages/")
    programsContentPath = AppendPath(mainContentPath,   "Programs/")
    #endregion
    #region ------------------------------------- [3]
    Debug.Log("[3]: Getting contents")
    mainContent     = os.listdir(mainContentPath)
    libraryContent  = os.listdir(libraryContentPath)
    localContent    = os.listdir(localContentPath)
    pagesContent    = os.listdir(pagesContentPath)
    programsContent = os.listdir(programsContentPath)
    #endregion
    #region ------------------------------------- [4]
    Debug.Log("Checking contents")

    variables.errorMessage = _("The driver's content did not match the expected content.")
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    execution = CompareList(wantedMainContent, mainContent, exceptions=exceptions)
    if(execution != Execution.Passed):
        Debug.Error(">>> mainContent:\t FAILED")
        Debug.Log(f">>> Expected: {wantedMainContent}")
        Debug.Log(f">>> Gotten:  {mainContent}")
        return FileIntegrity.Corrupted
    else:
        Debug.Log(">>> mainContent:\t PASSED")
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    execution = CompareList(wantedLocalContent, localContent, exceptions=exceptions)
    if(execution != Execution.Passed):
        Debug.Error(">>> localContent:\t FAILED")
        Debug.Log(f">>> Expected: {wantedLocalContent}")
        Debug.Log(f">>> Gotten:  {localContent}")
        Debug.End()
        return FileIntegrity.Corrupted
    else:
        Debug.Log(">>> localContent:\t PASSED")
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    execution = CompareList(wantedLibraryContent, libraryContent, exceptions=exceptions)
    if(execution != Execution.Passed):
        Debug.Error(">>> libraryContent:\t FAILED")
        Debug.Log(f">>> Expected: {wantedLibraryContent}")
        Debug.Log(f">>> Gotten:  {libraryContent}")
        Debug.End()
        return FileIntegrity.Corrupted
    else:
        Debug.Log(">>> libraryContent:\t PASSED")
   # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    execution = CompareList(wantedPagesContent, pagesContent, exceptions=exceptions)
    if(execution != Execution.Passed):
        Debug.Error(">>> pagesContent:\t FAILED")
        Debug.Log(f">>> Expected: {wantedPagesContent}")
        Debug.Log(f">>> Gotten:  {pagesContent}")
        Debug.End()
        return FileIntegrity.Corrupted
    else:
        Debug.Log(">>> pagesContent:\t PASSED")
   # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    execution = CompareList(wantedProgramContent, programsContent, exceptions=exceptions)
    if(execution != Execution.Passed):
        Debug.Error(">>> programsContent:\t FAILED")
        Debug.Log(f">>> Expected: {wantedProgramContent}")
        Debug.Log(f">>> Gotten:  {programsContent}")
        Debug.End()
        return FileIntegrity.Corrupted
    else:
        Debug.Log(">>> programsContent:\t PASSED")
    #endregion
    Debug.End()
    return FileIntegrity.Good
#====================================================================#
# Classes
#====================================================================#

#====================================================================#
LoadingLog.End("SelfCheck.py")