#====================================================================#
# File Information
#====================================================================#
"""
    driver.py
    =========
    Summary:
    --------
    This file contains the Addon class necessary for Kontrol to know
    it has access to GPIOs
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
class GPIOReader(AddonFoundations):
    #region   --------------------------- DOCSTRING
    """
        GPIOReader:
        ==============
        Summary:
        --------
        This class handles the backend of
        whatever GPIO reading there is to do
        from a Linux terminal
    """
    #endregion
    #region   --------------------------- MEMBERS
    addonInformation:AddonInfoHandler = None
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
            slow GPIO updater that other
            addons may be using.

            Returns:
            --------
            - `Execution.Passed` = Addon was launched.
            - `Execution.Failed` = Error occured
            - `Execution.Incompatibility` = Failed to verify for compatibility.
        """
        Debug.Start("Launch")

        Debug.Log("Creating AddonInfoHandler")
        GPIOReader.addonInformation = AddonInfoHandler(
            "GPIOReader",
            "GPIOReader. Reads GPIO each couple seconds",
            "0.0.1",
            "hardware",
            None,
            False,
            True,
            False,
            False,
            "raspberry-pi",
            GPIOReader.Launch,
            GPIOReader.Stop,
            GPIOReader.Uninstall,
            GPIOReader.Update,
            GPIOReader.GetState,
            GPIOReader.ClearProfile,
            GPIOReader.SaveProfile,
            GPIOReader.ChangeProfile,
            GPIOReader.LoadProfile,
            GPIOReader.UnloadProfile,
            GPIOReader.GetAllHardwareControls,
            GPIOReader.GetAllSoftwareActions,
            GPIOReader.ChangeButtonActionBinding,
            GPIOReader.ChangeAxisBinding,
            GPIOReader.UnbindButtonBinding,
            GPIOReader.UnbindAxisBinding,
            GPIOReader.ChangeButtonActionBinding,
            GPIOReader.ChangeAxisActionBinding
        )

        result = GPIOReader.VerifyForExecution()
        if(result != Execution.Passed):
            Debug.Error("The addon cannot run on your device.")
            Debug.Log("Adding addon to application...")
            GPIOReader.addonInformation.DockAddonToApplication(False)
            Debug.End()
            return result

        result = GPIO.StartDriver()
        if(result != Execution.Passed):
            Debug.Error("Failed to start backend driver GPIOReader")
            GPIOReader.addonInformation.DockAddonToApplication(False)
            Debug.End()
            return Execution.Failed

        Debug.Log("Addon started successfully.")
        Debug.Log("Adding addon to application...")
        GPIOReader.addonInformation.DockAddonToApplication(True)
        GPIOReader.state = True
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

        if(GPIOReader.state == True):
            Debug.Log("Stopping GPIOReader")
            result = GPIO.StopDriver()
            if(result != Execution.Passed):
                Debug.Error("Error when trying to stop GPIO backend driver")
                Debug.End()
                return Execution.Failed
            Debug.Log("GPIOReader is now OFF")
            Debug.End()
            return Execution.Passed
        else:
            Debug.Log("Unecessary. GPIOReader is not running.")
            Debug.End()
            return Execution.Unecessary
    #endregion
    #region --------------------- PRIVATE

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

        Debug.Log("Seems alright.")
        Debug.End()
        return Execution.Passed
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
LoadingLog.End("GPIOReader.py")