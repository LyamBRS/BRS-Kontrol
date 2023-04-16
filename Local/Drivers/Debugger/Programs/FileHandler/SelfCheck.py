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
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import CompareList, IsPathValid
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
    #region ------------------------------------- [0] - Imports
    import os
    from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import AppendPath, CompareList
    from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
    from Local.Drivers.Debugger.Driver import variables
    #endregion
    #region ------------------------------------- [1] - Define content & paths
    Debug.Log("[0]: Defining variables")

    expectedContent = {
        # Main content
        "/Local/Drivers/Debugger/" : [
            "Libraries",
            "Local",
            "Pages",
            "Programs",
            "__init__.py",
            "Config.json",
            "Driver.py"
        ],

        # Library folder content
        "/Local/Drivers/Debugger/Libraries/" : [
            "Backgrounds"
        ],

        # Backgrounds folder content
        "/Local/Drivers/Debugger/Libraries/Backgrounds/" : [
            "Menu"
        ],

        # Menu folder content
        "/Local/Drivers/Debugger/Libraries/Backgrounds/Menu/" : [
            "Dark.png",
            "Light.png"
        ],

        # Page folder content
        "/Local/Drivers/Debugger/Pages/" : [
            "DebuggerMenu.py",
            "DebuggerAbout.py",
            "DebuggerAccount.py",
            "DebuggerBluetooth.py",
            "DebuggerBrSpand.py",
            "DebuggerDevices.py",
            "DebuggerKontrol.py",
            "DebuggerNetwork.py",
        ],

        # Local folder content
        "/Local/Drivers/Debugger/Local/" : [
            "Cache",
            "Languages",
            "Profiles"
        ],

        # Program folder content
        "/Local/Drivers/Debugger/Programs/" : [
            "FileHandler",
            "GUI"
        ],

        # FileHandler folder content
        "/Local/Drivers/Debugger/Programs/FileHandler/" : [
            "SelfCheck.py"
        ],

        # GUI folder content
        "/Local/Drivers/Debugger/Programs/GUI/" : [
            "Navigation.py"
        ]
    }

    exceptions = [
        "__pycache__"
    ]

    #endregion
    #region ------------------------------------- [2] - Compare lists with expected content
    Debug.Log("[2]: Checking contents")
    variables.errorMessage = _("The driver's content did not match the expected content.")
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # For loop that checks each path's expected
    # content with the actual content found at that
    # path.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for path in expectedContent.keys():
        # [0] --------------------------- Create path
        key = path
        path = AppendPath(os.getcwd(), path)

        # [1] --------------------------- Path validity
        valid = IsPathValid(path)
        if(not valid):
            Debug.Error(">>> INVALID PATH:")
            Debug.Error(f">>> {path}")
            Debug.End()
            return FileIntegrity.Corrupted

        # [3] --------------------------- Actual content
        content = os.listdir(path)

        # [2] --------------------------- List comparaison
        execution = CompareList(expectedContent[key], content, exceptions=exceptions)
        if(execution != Execution.Passed):
            Debug.Error(f">>> {key}:\t FAILED")
            Debug.Log(f">>> Expected: {expectedContent[key]}")
            Debug.Log(f">>> Gotten:  {content}")
            Debug.End()
            return FileIntegrity.Corrupted
        else:
            Debug.Log(f">>> {key}:\t PASSED")
    #endregion
    Debug.End()
    return FileIntegrity.Good
#====================================================================#
# Classes
#====================================================================#

#====================================================================#
LoadingLog.End("SelfCheck.py")