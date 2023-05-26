#====================================================================#
# File Information
#====================================================================#
"""
    kontrolBFIO.py
    =============
    This file hosts getter functions that gets the mandatory
    functions made specifically for Kontrol master output for
    function requests towards BrSpand cards.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import LoadingLog, Debug
LoadingLog.Start("kontrolBFIO.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
# LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("BFIO")
from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import BFIO, Plane, MandatoryFunctionRequestVarTypeLists, MandatoryPlaneIDs
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
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
def GetUniversalInfoPlane() -> Plane:
    """
        GetUniversalInfoPlane:
        ======================
        Summary:
        --------
        Returns a plane built by Kontrol
        that represents its own Universal
        unique ID.
    """
    Debug.Start("GetUniversalInfoPlane")

    data = [
        696969,                                     # unique device ID
        1,                                              # BFIO version
        1,                                              # Device type
        1,                                              # Device status
        "https://github.com/LyamBRS/BrSpand_GamePad.git",   # Git repository of the device.
        Information.name,
        str(Information.softwareVersion)
    ]
    
    Debug.End()
    return data

#====================================================================#
# Classes
#====================================================================#
# class Example:
    # region   --------------------------- DOCSTRING
    # ''' This class is a reference style class which represents the current state that a device can be in.
        # A device can be GUI or hardware.
        # You don't have to use this class when defining the state of a device, but it is more convenient than
        # memorizing all the numbers associated by heart.
    # '''
    # endregion
    # region   --------------------------- MEMBERS
    # fakeVar : type = "sus"
    # ''' It's ugly docstring which for some annoying reason is below whatever it needs to explain... Which is hideous and hard to follow. No humans read data from bottom to top bruh.'''
    # endregion
    # region   --------------------------- METHODS
    # endregion
    # region   --------------------------- CONSTRUCTOR
    # endregion
    # pass
#====================================================================#
LoadingLog.End("AppLoading.py")