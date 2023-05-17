#====================================================================#
# File Information
#====================================================================#
"""
    driver.py
    =========
    Summary:
    --------
    This file contains the high level classes and functions made to
    interface an on board addon card such as an Accelerometer.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
LoadingLog.Start("driver.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
# LoadingLog.Import("Python")
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
# from ...Utilities.Information import Information
# from ...Utilities.FileHandler import JSONdata, CompareKeys, AppendPath
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Hardware.Accelerometer import ADXL343
from Libraries.BRS_Python_Libraries.BRS.Utilities.FileHandler import JSONdata, AppendPath
#endregion
#region -------------------------------------------------------- Kivy
# LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
# LoadingLog.Import('KivyMD')
#endregion
#====================================================================#
# Variables
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class Accelerometer:
    #region   --------------------------- DOCSTRING
    """
        Accelerometer:
        ==============
        Summary:
        --------
        This class handles the backend of trying
        to interface an accelerometer addon card
        with the Raspberry Pi.
    """
    #endregion
    #region   --------------------------- MEMBERS
    isRunning:bool = False

    profileData:JSONdata = None
    #endregion
    #region   --------------------------- METHODS
    def Launch() -> Execution:
        """
            Launch:
            =======
            Summary:
            --------
            Launches the accelerometer addon.
            returns Execution to indicate how
            the launch went.

            Returns:
            --------
            - `Execution.Passed` = Addon was launched.
            - `Execution.Failed` = Error occured
            - `Execution.Incompatibility` = Failed to verify for compatibility.
        """
        Debug.Start("Launch")

        result = Accelerometer.VerifyForExecution()
        if(result != Execution.Passed):
            Debug.Error("The addon cannot run on your device.")
            Debug.End()
            return Execution.Failed

        Debug.Log("Addon started successfully.")
        Accelerometer.isRunning = True
        Debug.End()
        return Execution.Passed

    def StopAddon() -> Execution:
        """
            StopAddon:
            ==========
            Summary:
            --------
            Stops the addon from running.
            Closes the thread that is running it.
            Gone, reduced to atoms.
            Oh, and it unbinds stuff too.
        """
        Debug.Start("StopAddon")

        Debug.End()

    def Set(
            oldProfileName:str = None,
            newProfileName:str = None,
            SoftwareBindX_Positive:str = None,
            SoftwareBindX_Negative:str = None,
            SoftwareBindY_Positive:str = None,
            SoftwareBindY_Negative:str = None,
            ) -> Execution:
        """
            Set:
            ====
            Summary:
            --------
            This method sets parameters
            into a profile such as what
            to bind X and Y axis to.
            You can also rename a profile.

            Arguments:
            ----------
            - `oldProfileName:str` = The old profile that will be replaced with :ref:`newProfileName` Both need to be specified to change em.
            - `newProfileName:str` = The new profile that will replace with :ref:`oldProfileName` Both need to be specified to change em.
            - `SoftwareBindX_Positive:str` = The software axis to bind to the positive value returned from the ADXL343's X axis.
            - `SoftwareBindX_Negative:str` = The software axis to bind to the negative value returned from the ADXL343's X axis.
            - `SoftwareBindY_Positive:str` = The software axis to bind to the positive value returned from the ADXL343's Y axis.
            - `SoftwareBindY_Negative:str` = The software axis to bind to the negative value returned from the ADXL343's Y axis.
        """
        Debug.Start("Set")
        Debug.End()

    def ProfileLoggedIn(ProfileLoggedIn:str) -> Execution:
        """
            ProfileLoggedIn:
            ================
            Summary:
            --------
            Loads settings from a specific
            profile into the class and other
            hardware handling classes.

            If the profile does not exist,
            errors will be returned.
        """
        Debug.Start("ProfileLoggedIn")

        Debug.End()

    def ClearProfileCache(profileThatGotDeleted:str) -> Execution:
        """
            ClearProfileCache:
            ==================
            Summary:
            --------
            Clears a profile from a cache.
        """
        Debug.Start("ClearProfileCache")

        Debug.End()
    
    def VerifyForExecution() -> Execution:
        """
            VerifyForExecution:
            ===================
            Summary:
            --------
            Function that returns Execution.Passed
            if the hardware and software allows
            ADXL343 to interface with Kontrol.
            Otherwise, Execution.Failed is returned.
        """
        Debug.Start("VerifyHardware")

        if(not Information.initialized):
            Debug.Error("Information class is not initialized")
            Debug.End()
            return Execution.Failed
        
        if(Information.platform != "Linux"):
            Debug.Error("This addon only works on Linux.")
            Debug.End()
            return Execution.Incompatibility
        
        Debug.Log("Seems alright.")

        Debug.End()
        return Execution.Passed

    def _CreateOrLoadJSON() -> Execution:
        """
            _CreateOrLoadJSON:
            ==================
            Summary:
            --------
            Handles the creation and
            loading of the addon's JSON
            file. Creates the JSON
            if none exists.
        """
        Debug.Start("_CreateOrLoadJSON")

        import os
        path = os.getcwd()
        path = AppendPath(path, "/Local/Hardware/Accelerometer")
        Accelerometer.profileData = JSONdata("Config", path)

        if(Accelerometer.profileData.jsonData == None):
            Debug.Error("Failed to load Config.json")
            Debug.Log("Creating JSON")

            Accelerometer.profileData.CreateFile({})
            Accelerometer.profileData = JSONdata("Config", path)

            if(Accelerometer.profileData.jsonData == None):
                Debug.Error("Failed to create JSON after second try.")
                Debug.End()
                return Execution.Failed

        Debug.End()
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
LoadingLog.End("ADXL343.py")