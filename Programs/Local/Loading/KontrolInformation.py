#====================================================================#
# File Information
#====================================================================#
"""
    KontrolInformation.py
    =====================
    Summary:
    --------
    This file holds functions specific to Kontrol which allows
    you to load Kontrol's information without having to do it
    manually.
"""
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Libraries.BRS_Python_Libraries.BRS.Network.APIs.GitHub import GitHub
LoadingLog.Start("KontrolInformation.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.AppScreenHandler import AppManager
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import("KivyMD")
#endregion
#region ------------------------------------------------------ Kontrol
LoadingLog.Import("Local")
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
#endregion
#====================================================================#
# Functions
#====================================================================#
def SetKontrolInformation() -> Execution:
    """
        SetKontrolInformation:
        =======================
        Summary:
        --------
        This function loads all of Kontrol's specific information
        into the Information class.

        `Attention`:
        ------------
        Most of the information stored in this class is hard coded.
    """
    Debug.Start("LoadKontrolInformation")

    Information.name = "BRS Kontrol"
    Information.description = "Python program controlling BRS Kontrol's application"
    Information.framework = "KivyMD"

    Information.hardwareVersion = "A"
    if(GitHub.CurrentTag == None):
        GitHub.GetLocalRepository()

    if(GitHub.CurrentTag == None):
        Information.softwareVersion = _("Error")
    else:
        Information.softwareVersion = GitHub.CurrentTag
    Information.deviceVersion = "Dev"

    Debug.End()
    return Execution.Passed
#====================================================================#
# Classes
#====================================================================#

LoadingLog.End("KontrolInformation.py")