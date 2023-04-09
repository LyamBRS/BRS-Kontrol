#====================================================================#
# File Information
#====================================================================#
"""
    Driver.py
    =============
    This file is the generic, universal Device Driver; Driver.py.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("Driver.py")
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
class variables:
    errorMessage:str = None
#====================================================================#
# Functions
#====================================================================#
def CheckIntegrity() -> FileIntegrity:
    """
        CheckIntegrity:
        ===============
        Summary:
        -------
        This function checks this device driver for any default
        or missing file(s). As the name says, it checks for the
        integrity of itself and returns the resulted integrity.
    """
    Debug.Start("CheckIntegrity")
    variables.errorMessage = "message"
    Debug.End()
    return FileIntegrity.Good
# -------------------------------------------------------------------
def Launch() -> Execution:
    """
        Launch:
        =======
        Summary:
        -------
        attempts to launch the GUI of your device driver.
        It loads a Screen into the ScreenManager.

        It will return a value within the Execution enum.
    """
    Debug.Start("Launch")
    Debug.End()
    return Execution.ByPassed
# -------------------------------------------------------------------
def Update() -> Execution:
    """
        Update:
        =======
        Summary:
        -------
        This function attempts to update the device driver to it's
        latest version. It will return an Execution value depending
        on what happens.
    """
    Debug.Start("Update")
    Debug.End()
    return Execution.ByPassed
# -------------------------------------------------------------------
def Uninstall() -> Execution:
    """
        Uninstall:
        =======
        Summary:
        -------
        Completely uninstall this device driver without leaving any
        traces of it's existence in Kontrol's Software.
    """
    Debug.Start("Uninstall")
    Debug.End()
    return Execution.ByPassed
# -------------------------------------------------------------------
def ClearProfileCache(profileName:str) -> Execution:
    """
        ClearProfileCache:
        ==================
        Summary:
        -------
        Removes cached data of a specific profile. This is called
        when a profile is deleted, thus all it's cached information
        needs to be deleted as well.

        The name of the profile is given as a parameter. The function
        will return an Execution enum value.
    """
    Debug.Start("ClearProfileCache")
    Debug.End()
    return Execution.ByPassed
# -------------------------------------------------------------------
def GetErrorMessage() -> str:
    """
        GetErrorMessage:
        ===============
        Summary:
        -------
        Function used to get the error message of the Device Driver.
        If it crashes or cannot load, the message as to why something
        wrong happened is stored and can be accessed through this
        function.

        if there is no error to return, `None` is returned.
    """
    Debug.Start("GetErrorMessage")
    Debug.End()
    return variables.errorMessage
# -------------------------------------------------------------------
def Quit() -> Execution:
    """
        Quit:
        =====
        Summary:
        -------
        Function used to quit and close the device driver and return
        to Kontrol's GUI.
    """
    Debug.Start("GetErrorMessage")
    Debug.End()
    return None
#====================================================================#
# Classes
#====================================================================#

#====================================================================#
LoadingLog.End("Driver.py")