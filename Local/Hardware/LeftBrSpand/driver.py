#====================================================================#
# File Information
#====================================================================#
"""
    driver.py
    =========
    Summary:
    --------
    This file contains the high level classes and functions made to
    interface Kontrol with USB-C BrSpand cards of generation 1.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Libraries.BRS_Python_Libraries.BRS.Hardware.GPIO.driver import GPIO
LoadingLog.Start("driver.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import os
#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.addons import AddonFoundations, AddonInfoHandler, AddonEnum
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
class LeftBrSpand(AddonFoundations):
    #region   --------------------------- DOCSTRING
    """
        LeftBrSpand:
        ==============
        Summary:
        --------
        This class handles the backend of
        whatever BrSpand card has been connected
        to Kontrol on the left port.
    """
    #endregion
    #region   --------------------------- MEMBERS
    addonInformation:AddonInfoHandler = None
    oldConnectionStatus:bool = False
    """
        Used to keep track of when a card
        disconnects / connects
    """
    #endregion
    #region   --------------------------- METHODS
    #region ----------------------- ADDON
    def Launch() -> Execution:
        """
            Launch:
            =======
            Summary:
            --------
            Launches the handler for the
            left BrSpand card port reader.

            Returns:
            --------
            - `Execution.Passed` = Addon was launched.
            - `Execution.Failed` = Error occured
            - `Execution.Incompatibility` = Failed to verify for compatibility.
        """
        Debug.Start("Launch")

        Debug.Log("Creating AddonInfoHandler")
        LeftBrSpand.addonInformation = AddonInfoHandler(
            "LeftBrSpand",
            "ADXL343 on board LeftBrSpand hardware extension.",
            "0.0.1",
            "hardware",
            None,
            False,
            True,
            False,
            False,
            "integrated-circuit-chip",
            LeftBrSpand.Launch,
            LeftBrSpand.Stop,
            LeftBrSpand.Uninstall,
            LeftBrSpand.Update,
            LeftBrSpand.GetState,
            LeftBrSpand.ClearProfile,
            LeftBrSpand.SaveProfile,
            LeftBrSpand.ChangeProfile,
            LeftBrSpand.LoadProfile,
            LeftBrSpand.UnloadProfile,
            LeftBrSpand.GetAllHardwareControls,
            LeftBrSpand.GetAllSoftwareActions,
            LeftBrSpand.ChangeButtonActionBinding,
            LeftBrSpand.ChangeAxisBinding,
            LeftBrSpand.UnbindButtonBinding,
            LeftBrSpand.UnbindAxisBinding,
            LeftBrSpand.ChangeButtonActionBinding,
            LeftBrSpand.ChangeAxisActionBinding
        )

        result = LeftBrSpand.VerifyForExecution()
        if(result != Execution.Passed):
            Debug.Error("The addon cannot run on your device.")
            Debug.Log("Adding addon to application...")
            LeftBrSpand.addonInformation.DockAddonToApplication(False)
            Debug.End()
            return result

        result = ADXL343.StartDriver()
        if(result != Execution.Passed):
            Debug.Error("Failed to start backend driver ADXl343")
            LeftBrSpand.addonInformation.DockAddonToApplication(False)
            Debug.End()
            return Execution.Failed

        Debug.Log("Addon started successfully.")
        Debug.Log("Adding addon to application...")
        LeftBrSpand.addonInformation.DockAddonToApplication(True)
        LeftBrSpand.state = True
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def Stop() -> Execution:
        """
            Stop:
            ==========
            Summary:
            --------
            Stops the addon from running.
            Closes the thread that is running it.
            Gone, reduced to atoms.
            Oh, and it unbinds stuff too.
        """
        Debug.Start("Stop")

        if(LeftBrSpand.state == True):
            Debug.Log("Stopping ADXL343")
            result = ADXL343.StopDriver()
            if(result != Execution.Passed):
                Debug.Error("Error when trying to stop ADXL343")
                Debug.End()
                return Execution.Failed
            Debug.Log("ADXL343 is now OFF")
            LeftBrSpand.profileData.SaveFile()
            Debug.End()
            return Execution.Passed
        else:
            Debug.Log("Unecessary. ADXL343 is not running.")
            Debug.End()
            return Execution.Unecessary
    #endregion
    #region --------------------- PRIVATE
    def _IsCardConnected() -> bool:
        """
            _IsCardConnected:
            =================
            Summary:
            --------
            Identifies if a card is
            connected or not.
        """
        Debug.Start("_IsCardConnected")

        Debug.End()

    def _IsCardUsable() -> bool:
        """
            _IsCardUsable:
            ==============
            Summary:
            --------
            Identifies if a card is usable
            or not by Kontrol.
        """
        Debug.Start("_IsCardUsable")

        Debug.End()

    def _GetCurrentGPIOLevels() -> list:
        """
            _GetCurrentGPIO:
            ================
            Summary:
            --------
            Returns a list of True and
            False that corresponds to
            the levels of the GPIOs used
            by this BrSpand card port.
        """
    # -----------------------------------
    # -----------------------------------
    def VerifyForExecution() -> Execution:
        """
            VerifyForExecution:
            ===================
            Summary:
            --------
            Function that returns Execution.Passed
            if the hardware and software allows
            BrSpand to interface with Kontrol.
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

        if(GPIO.isStarted != True):
            Debug.Error("The GPIO thread is not running.")
            Debug.End()
            return Execution.Failed

        Debug.Log("Seems alright.")
        Debug.End()
        return Execution.Passed
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
LoadingLog.End("ADXL343.py")