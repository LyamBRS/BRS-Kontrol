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
from Libraries.BRS_Python_Libraries.BRS.Hardware.UART.receiver import UART
from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import BFIO, NewArrival, Plane
from Programs.Local.BFIO.kontrolBFIO import GetUniversalInfoPlane
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

    cardJustConnected:bool = False
    universalInfoSent:bool = False

    class ConnectedCard:
        """
            ConnectedCard:
            ==============
            Summary:
            --------
            Keeps information about the
            BrSpand card connected to this
            BrSpand UART port.
        """
        universalInformationPlane:NewArrival = None
        gitRepository:str = None
        name:str = None
        revision:str = None
        type:int = None
        ID:int = None
        BFIO:int = 0


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
            LeftBrSpand.state = False
            UART.StopDriver()
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

        if(LeftBrSpand.cardJustConnected and LeftBrSpand.universalInfoSent):
            result = LeftBrSpand._CheckUARTForUniversalInfo()
            if(result != Execution.Passed):
                Debug.Error("Check UART failed.")
                LeftBrSpand.cardJustConnected = False
                LeftBrSpand.universalInfoSent = False
                Debug.End()
                return Execution.Failed

            result = LeftBrSpand._StoreUniversalInformations()
            if(result != Execution.Passed):
                Debug.Error("Failed to store universal informations")
                LeftBrSpand.cardJustConnected = False
                LeftBrSpand.universalInfoSent = False
                Debug.End()
                return Execution.Failed

            LeftBrSpand._DisplayConnectionSuccessful()
            LeftBrSpand.cardJustConnected = False
            LeftBrSpand.universalInfoSent = False

        if(LeftBrSpand.cardJustConnected and not LeftBrSpand.universalInfoSent):
            Debug.Log("Starting handshake proceedure")
            LeftBrSpand._StartHandshake()
            LeftBrSpand.universalInfoSent = True

        if(LeftBrSpand.currentConnectionStatus != LeftBrSpand.oldConnectionStatus):
            LeftBrSpand.oldConnectionStatus = LeftBrSpand.currentConnectionStatus

            if(connected):
                # dialog = MDDialog(
                    # title=_("BrSpand Detected"),
                    # text=_("A BrSpand card was detected. Do you want to start the connection process? This may cause crashes and unknown behaviors if the application is currently executing tasks and processes. Make sure you are in a main menu before connecting a BrSpand card."),
                    # buttons=[
                        # MDFlatButton(text=_("Cancel"), font_style="H6"),
                        # MDFillRoundFlatButton(text=_("Start"), font_style="H6")
                    # ]
                # )
                KontrolRGB.StartOfHandshake()
                LeftBrSpand.cardJustConnected = True
                LeftBrSpand.universalInfoSent = False
                Debug.End()
                return Execution.Passed

            if(not connected):
                LeftBrSpand.dialog = MDDialog(
                    title=_("BrSpand Lost"),
                    text=_("The BrSpand card connected to the left USB-C port has been disconnected. Ensure you have a solid connection if this is not normal. Avoid bending Kontrol too."),
                    buttons=[
                        MDFillRoundFlatButton(text=_("Ok"), font_style="H6", on_press = LeftBrSpand.CloseDialog)
                    ]
                )
                LeftBrSpand.cardJustConnected = False
                LeftBrSpand.universalInfoSent = False
                LeftBrSpand.dialog.open()
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

        if(LeftBrSpand.gpioLevels == connectedAndValid):
            LeftBrSpand.currentConnectionStatus = True
            Debug.End()
            return True

        if(LeftBrSpand.gpioLevels == connectedAndInvalid):
            LeftBrSpand.currentConnectionStatus = True
            Debug.End()
            return True

        LeftBrSpand.currentConnectionStatus = False
        Debug.Log("Card is NOT connected")
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

        if(LeftBrSpand.gpioLevels == connectedAndValid):
            Debug.End()
            return True

        if(LeftBrSpand.gpioLevels == connectedAndInvalid):
            Debug.End()
            return False

        Debug.End()
        return False

    def _StartHandshake() -> Execution:
        """
            _StartHandshake:
            ================
            Summary:
            --------
            This function starts an UART class
            and tries to send an universal plane.
            on the Left master runway.
        """
        Debug.Start("LeftBrSpand -> _StartHandshake")
        UART.serialPort = "/dev/ttyAMA2"
        result = UART.StartDriver()

        if(result == Execution.Incompatibility):
            LeftBrSpand.dialog = MDDialog(
                title=_("BrSpand Failure"),
                text=_("The left BrSpand port failed to start the UART driver and thus cannot communicate with the card you plugged in. Make sure you're running on a compatible Kontrol version."),
                buttons=[
                    MDFlatButton(text=_("Ok"), font_style="H6", on_press = LeftBrSpand.CloseDialog),
                ]
            )
            LeftBrSpand.dialog.open()
            KontrolRGB.DisplayUserError()
            Debug.Error("LeftBrSpand failed to start UART BFIO threads.")
            Debug.End()
            return Execution.Failed

        Debug.Log("Building and sending Universal Info")
        kontrolUniversalInfo = GetUniversalInfoPlane()
        result = UART.QueuePlaneOnTaxiway(kontrolUniversalInfo)
        if(result != Execution.Passed):
            LeftBrSpand.dialog = MDDialog(
                title=_("BrSpand Failure"),
                text=_("The left BrSpand port failed to output its Universal Informations to the BrSpand card you just plugged in. Unplug it, wait for the pop up message then try to reconnect it."),
                buttons=[
                    MDFlatButton(text=_("Damn"), font_style="H6", on_press = LeftBrSpand.CloseDialog),
                ]
            )
            LeftBrSpand.dialog.open()
            KontrolRGB.DisplayUserError()
            Debug.Error("LeftBrSpand failed to queue plane on taxiway of BFIO threads.")
            Debug.End()
            return Execution.Failed

        KontrolRGB.Handshaking()
        Debug.End()
        return Execution.Passed

    def _StoreUniversalInformations() -> Execution:
        """
            __StoreUniversalInformations:
            =============================
            Summary:
            --------
            Handles the storing of the
            universal information stored
            within the landed plane obtained
            from the handshake with the
            currently plugged in BrSpand
            card.
        """
        Debug.Start("__StoreUniversalInformations")

        data = [
            4206969,                                     # unique device ID 0
            1,                                              # BFIO version 1
            0,                                              # Device type 2
            1,                                              # Device status 3
            "https://github.com/LyamBRS/BrSpand_GamePad.git",   # Git repository of the device. 4
            "GamePad", # 5
            "Rev A" # 6
        ]

        LeftBrSpand.ConnectedCard.ID = LeftBrSpand.ConnectedCard.universalInformationPlane.GetParameter(0)
        LeftBrSpand.ConnectedCard.BFIO = LeftBrSpand.ConnectedCard.universalInformationPlane.GetParameter(1)
        LeftBrSpand.ConnectedCard.type = LeftBrSpand.ConnectedCard.universalInformationPlane.GetParameter(2)
        LeftBrSpand.ConnectedCard.gitRepository = LeftBrSpand.ConnectedCard.universalInformationPlane.GetParameter(4)
        LeftBrSpand.ConnectedCard.name = LeftBrSpand.ConnectedCard.universalInformationPlane.GetParameter(5)
        LeftBrSpand.ConnectedCard.revision = LeftBrSpand.ConnectedCard.universalInformationPlane.GetParameter(6)

        Debug.End()
        return Execution.Passed

    def _DisplayConnectionSuccessful() -> Execution:
        """
            _DisplayConnectionSuccessful:
            =============================
            Summary:
            --------
            This function's purpose is to
            display a dialog to the user
            informing him about the card
            he just plugged into their
            Kontrol device.
        """
        Debug.Start("LeftBrSpand -> _DisplayConnectionSuccessful")

        planeID = LeftBrSpand.ConnectedCard.universalInformationPlane.planeID
        passengerCount = len(LeftBrSpand.ConnectedCard.universalInformationPlane.passengers)
        passedTSA = LeftBrSpand.ConnectedCard.universalInformationPlane.passedTSA
        amountOfClasses = LeftBrSpand.ConnectedCard.universalInformationPlane.amountOfClasses

        LeftBrSpand.dialog = MDDialog(
            title= str(LeftBrSpand.ConnectedCard.name) + _(" is now connected!"),
            #text=_("You plugged in a BrSpand compatible extension card into Kontrol.") + _("This card's revision is") + ": " + str(LeftBrSpand.ConnectedCard.revision) + ". " + _("The drivers can be downloaded from") + ": " + str(LeftBrSpand.ConnectedCard.gitRepository),
            text=f"This plane's callsign is {planeID}. It carries {passengerCount} passengers divided into {amountOfClasses} classes, it is {passedTSA} that it passed TSA.",

            buttons=[
                MDFlatButton(text=_("Cancel"), font_style="H6", on_press = LeftBrSpand.CloseDialog),
                MDFillRoundFlatButton(text=_("Launch"), font_style="H6", on_press = LeftBrSpand.CloseDialog)
            ]
            )
        KontrolRGB.ApploadingAnimation()
        LeftBrSpand.dialog.open()
        Debug.End()
        return Execution.Passed
    # -----------------------------------
    def CloseDialog(*args):
        """
            CloseDialog:
            ============
            Summary:
            --------
            Closes the currently opened
            BrSpand dialog and returns
            the RGB lights to normal.
        """
        Debug.Start("CloseDialog")
        LeftBrSpand.dialog.dismiss()
        KontrolRGB.DisplayDefaultColor()
        Debug.End()
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
    # -----------------------------------
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
    def _CheckUARTForUniversalInfo() -> Execution:
        """
            _CheckUARTForUniversalInfo:
            ===========================
            Summary:
            --------
            Checks the UART to see if the card
            answered with its universal informations
            properly.
        """
        Debug.Start("LeftBrSpand -> _CheckUARTForUniversalInfo")

        newGroup = UART.GetOldestReceivedGroupOfPassengers()
        if(newGroup == Execution.Failed):
            Debug.Error(f"BFIO failure. Failed to obtain oldest plane received.")
            LeftBrSpand.dialog = MDDialog(
                title=_("Handshake Failure"),
                text=_("416: BrSpand drivers failed to obtain Universal Information from their own drivers. Handshake could not be resolved."),
                buttons=[
                    MDFillRoundFlatButton(text=_("Damn"), font_style="H6", on_press = LeftBrSpand.CloseDialog)
                ]
            )
            KontrolRGB.DisplayUserError()
            LeftBrSpand.dialog.open()
            LeftBrSpand.cardJustConnected = False
            LeftBrSpand.universalInfoSent = False
            Debug.End()
            return Execution.Failed

        else:
            if(newGroup != None):
                planeIsMandatory = BFIO.IsPassengerGroupAMandatoryPlane(newGroup)
                if(planeIsMandatory):
                    plane = BFIO.ParsePassengersIntoMandatoryPlane(newGroup)
                    if(plane.passedTSA):
                        Debug.Log("HOLY SHIT I THINK WE GOT IT ?!?")
                        LeftBrSpand.ConnectedCard.universalInformationPlane = plane
                        Debug.End()
                        return Execution.Passed
                    else:
                        Debug.Error(f"BFIO failure. Universal Information plane seems to be corrupted.")
                        LeftBrSpand.dialog = MDDialog(
                            title=_("Handshake Failure"),
                            text=_("437: The received BFIO data from the BrSpand card appears to be corrupted. Please unplug the card, wait for the connection lost pop up messgage and try to connect it again."),
                            buttons=[
                                MDFillRoundFlatButton(text=_("Sure"), font_style="H6", on_press = LeftBrSpand.CloseDialog)
                            ]
                        )
                        KontrolRGB.DisplayUserError()
                        LeftBrSpand.dialog.open()
                        LeftBrSpand.cardJustConnected = False
                        LeftBrSpand.universalInfoSent = False
                        Debug.End()
                        return Execution.Failed
                else:
                    Debug.Error(f"BFIO failure. BrSpand card keeps sending useless informations")
                    LeftBrSpand.dialog = MDDialog(
                        title=_("Handshake Failure"),
                        text=_("450: The connected card is sending unsupported BFIO answers/requests before their handshakes were successful. Unplug the card, wait for the connection lost pop up then try to connect it again."),
                        buttons=[
                            MDFillRoundFlatButton(text=_("Huh"), font_style="H6", on_press = LeftBrSpand.CloseDialog)
                        ]
                    )
                    KontrolRGB.DisplayUserError()
                    LeftBrSpand.cardJustConnected = False
                    LeftBrSpand.universalInfoSent = False
                    LeftBrSpand.dialog.open()
                    Debug.End()
                    return Execution.Failed
            else:
                Debug.Error(f"BFIO failure. Failed to obtain oldest plane received.")
                LeftBrSpand.dialog = MDDialog(
                    title=_("Handshake Failure"),
                    text=_("463: BrSpand drivers did not receive anything back from the BrSpand card. Handshake could not be resolved. Try to unplug, then replug your BrSpand card only once the Connection Lost message appears."),
                    buttons=[
                        MDFillRoundFlatButton(text=_("Damn"), font_style="H6", on_press = LeftBrSpand.CloseDialog)
                    ]
                )
                KontrolRGB.DisplayUserError()
                LeftBrSpand.cardJustConnected = False
                LeftBrSpand.universalInfoSent = False
                LeftBrSpand.dialog.open()
                Debug.End()
                return Execution.Failed
    #endregion
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
LoadingLog.End("driver.py")