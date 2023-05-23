#====================================================================#
# File Information
#====================================================================#
"""
    AppLoading.py
    =============
    This file is used to control and coordinate the loading of the
    application's various things. It uses a list of things to do where
    each element is paired with a function that returns `True` if an
    error occured and `False` if that loading step was successful.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import LoadingLog
LoadingLog.Start("controls.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
# LoadingLog.Import("Libraries")
#endregion
#region -------------------------------------------------------- Kivy
# LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
# LoadingLog.Import('KivyMD')
#endregion
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
LoadingLog.Class("BatiscanControls")
class BatiscanControls:
    #region   --------------------------- DOCSTRING
    """
        BatiscanControls:
        =================
        Summary:
        ========
        Holds each possible controls that can
        be read or sent to Batiscan.
    """
    #endregion
    #region   --------------------------- MEMBERS
    wantedLeftLight:bool = False
    wantedRightLight:bool = False

    wantedBallast:bool = False
    currentBallast:bool = False

    currentLeftLight:bool = False
    currentRightLight:bool = False
    # -----------------------------------
    currentCameraStatus:bool = False
    wantedCameraStatus:bool = False
    # -----------------------------------
    currentCameraAngle:int = 0
    wantedCameraAngle:int = 0

    currentMode:str = "N"
    wantedMode:str = "N"

    waterDetected:bool = False
    lowBattery:bool = False
    inEmergency:bool = False
    isCommunicating:bool = False

    pressure:int = 0
    temperature:int = 0
    
    currentTemperatureUnit:str = "C"
    wantedTemperatureUnit:str = "C"

    currentXAxis:int = 0
    currentYAxis:int = 0
    currentZAxis:int = 0
    currentPitch:int = 0
    currentRoll:int = 0
    currentYaw:int = 0

    wantedPitch:int = 0
    wantedRoll:int = 0
    wantedYaw:int = 0
    wantedSpeed:int = 0
    currentSpeed:int = 0

    currentServoA:int = 0
    currentServoB:int = 0
    currentServoC:int = 0
    currentServoD:int = 0
    currentServoE:int = 0

    wantedServoA:int = 0
    wantedServoB:int = 0
    wantedServoC:int = 0
    wantedServoD:int = 0
    wantedServoE:int = 0

    #endregion
    #region   --------------------------- METHODS
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
LoadingLog.End("AppLoading.py")