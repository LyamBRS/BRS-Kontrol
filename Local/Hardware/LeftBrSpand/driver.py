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
from Programs.Local.Hardware.RGB import KontrolRGB
from Programs.Pages.PopUps import PopUpTypeEnum
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
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
from Libraries.BRS_Python_Libraries.BRS.Utilities.LanguageHandler import _
from Libraries.BRS_Python_Libraries.BRS.Utilities.addons import AddonFoundations, AddonInfoHandler, AddonEnum
#endregion
#region -------------------------------------------------------- Kivy
# LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import('KivyMD')
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton
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
    currentConnectionStatus:bool = False
    gpioLevels:list = []
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
            "BrSpand handler and detector for left USB-C port",
            "0.0.1",
            "hardware",
            None,
            False,
            False,
            False,
            False,
            "expansion-card-variant",
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
            LeftBrSpand.PeriodicCallback,
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
            Debug.End()
            return Execution.Passed
        else:
            Debug.Log("Unecessary. Addon is not running.")
            Debug.End()
            return Execution.Unecessary
    # -----------------------------------
    def PeriodicCallback(*args) -> Execution:
        """
            PeriodicCallback:
            =================
            Summary:
            --------
            Checks if a BrSpand card
            is currently connected to
            Kontrol's Left USB-C port
            periodically. Calls dialogs
            if something happens.
        """
        Debug.Start("PeriodicCallback")

        if(LeftBrSpand.state != True):
            Debug.Error("LeftBrSpand addon is not started")
            Debug.End()
            return Execution.ByPassed

        LeftBrSpand._GetCurrentGPIOLevels()
        connected = LeftBrSpand._IsCardConnected()
        usable = LeftBrSpand._IsCardUsable()

        if(connected):
            KontrolRGB.DisplayUserError()
        else:
            KontrolRGB.DisplayPopUpAnimation(PopUpType=PopUpTypeEnum.Warning)

        if(LeftBrSpand.currentConnectionStatus != LeftBrSpand.oldConnectionStatus):
            LeftBrSpand.oldConnectionStatus = LeftBrSpand.currentConnectionStatus

            if(connected and usable):
                dialog = MDDialog(
                    title=_("BrSpand Detected"),
                    text=_("A BrSpand card was detected. Do you want to start the connection process? This may cause crashes and unknown behaviors if the application is currently executing tasks and processes. Make sure you are in a main menu before connecting a BrSpand card."),
                    buttons=[
                        MDFlatButton(text=_("Cancel"), font_style="H4"),
                        MDFillRoundFlatButton(text=_("Start"), font_style="H4")
                    ]
                )
                dialog.open()
                Debug.End()
                return Execution.Passed

            if(not connected):
                dialog = MDDialog(
                    title=_("BrSpand Lost"),
                    text=_("The BrSpand card connected to the left USB-C port has been disconnected. Ensure you have a solid connection if this is not normal. Avoid bending Kontrol too."),
                    buttons=[
                        MDFillRoundFlatButton(text=_("Ok"), font_style="H4")
                    ]
                )
                dialog.open()
                Debug.End()
                return Execution.Passed

            if(connected and not usable):
                dialog = MDDialog(
                    title=_("BrSpand Error"),
                    text=_("The BrSpand card connected to the left USB-C port cannot be used. This is either an error or because the card does not use their second connector. If your card only has one connector, there might be an issue with it."),
                    buttons=[
                        MDFillRoundFlatButton(text=_("Ok"), font_style="H4")
                    ]
                )
                dialog.open()
                Debug.End()
                return Execution.Passed

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

        connectedAndValid = [True, True, False, False]
        connectedAndInvalid = [False, False, False, False]

        if(LeftBrSpand.gpioLevels == connectedAndInvalid):
            LeftBrSpand.currentConnectionStatus = True
            Debug.End()
            return True

        if(LeftBrSpand.gpioLevels == connectedAndInvalid):
            LeftBrSpand.currentConnectionStatus = True
            Debug.End()
            return True

        LeftBrSpand.currentConnectionStatus = False
        Debug.End()
        return False

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
        connectedAndValid = [True, True, False, False]
        connectedAndInvalid = [False, False, False, False]

        if(LeftBrSpand.gpioLevels == connectedAndInvalid):
            Debug.End()
            return True

        if(LeftBrSpand.gpioLevels == connectedAndInvalid):
            Debug.End()
            return False

        Debug.End()
        return False

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
        Debug.Start("_GetCurrentGPIOLevels")
        gpio12 = GPIO.GetGPIOLevel(12)
        gpio13 = GPIO.GetGPIOLevel(13)
        gpio26 = GPIO.GetGPIOLevel(26)
        gpio27 = GPIO.GetGPIOLevel(27)
        Debug.Log(f"Current GPIO levels are {[gpio12, gpio13, gpio26, gpio27]}")
        LeftBrSpand.gpioLevels = [gpio12, gpio13, gpio26, gpio27]
        Debug.End()
        return [gpio12, gpio13, gpio26, gpio27]
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
LoadingLog.End("driver.py")