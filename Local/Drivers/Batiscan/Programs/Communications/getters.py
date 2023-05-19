#====================================================================#
# File Information
#====================================================================#
"""
    getters.py
    =============
    This file contains individual getters used to get live informations
    from Batiscan
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("getters.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import('KivyMD')
#endregion
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class Getters:
    #region   --------------------------- DOCSTRING
    """
        Getters:
        ========
        Summary:
        --------
        This class is a static class that
        contains various methods used to get
        information through WiFi with Batiscan.
    """
    #endregion
    #region   --------------------------- MEMBERS
    #endregion
    #region   --------------------------- METHODS
    def GetEverything() -> int:
        pass

    def GetBatteryLevel() -> int:
        pass

    def GetCurrentPressure() -> int:
        pass

    def GetErrorMessage() -> int:
        pass

    def GetCurrentStatus() -> int:
        pass

    def GetLightState() -> int:
        pass

    def GetBallastState() -> int:
        pass

    def GetCameraStatus() -> int:
        pass

    def GetMotorSpeed() -> int:
        pass

    def GetAxes() -> list:
        pass

    def GetFinsRotations() -> list:
        pass

    def GetUniversalInfos() -> list:
        pass
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
LoadingLog.End("AppLoading.py")