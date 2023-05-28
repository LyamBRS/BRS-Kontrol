#====================================================================#
# File Information
#====================================================================#
"""
    BFIO.py
    =============
    Summary
    -------
    This file contains a class that handles a thread meant to
    constantly talk with the UART handled by BrSpand addons.
    It is meant to constantly send hardware requests to GamePad
    and read its hardware planes that are sent back as fast as
    possible. It also contains the getter functions for binders.
"""

#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Hardware.UART.receiver import UART
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
from Libraries.BRS_Python_Libraries.BRS.Debug.LoadingLog import LoadingLog
from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import BFIO, Passenger, Plane
LoadingLog.Start("BFIODriver.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import time
import threading
import serial

#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution, VarTypes
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
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
hardwareRequest = Plane(20, [], [])
                    # LX,         LY            LB             RX            RY            RB             S1             S2             S3             S4             S5
hardwareVarTypes = [VarTypes.Int, VarTypes.Int, VarTypes.Bool, VarTypes.Int, VarTypes.Int, VarTypes.Bool, VarTypes.Bool, VarTypes.Bool, VarTypes.Bool, VarTypes.Bool, VarTypes.Bool]
#====================================================================#
# Classes
#====================================================================#
class BFIODriver:
    """
        BFIODriver:
        ===========
        Summary:
        --------
        Backend driver that reads at fasts intervals the
        UART threads handled by BrSpand ports drivers.
        Its goal is to send planes to Gamepad as fast
        as possible.
    """
    thread = None
    stopEvent = threading.Event()
    isStarted: bool = False
    errorMessage:str = ""

    _realLeftJoystickX = 0
    _realLeftJoystickY = 0
    _realRightJoystickX = 0
    _realRightJoystickY = 0
    _realLeftJoystickButton = False
    _realRightJoystickButton = False

    _realSwitch1 = False
    _realSwitch2 = False
    _realSwitch3 = False
    _realSwitch4 = False
    _realSwitch5 = False


    leftJoystickPositiveX:float = 0
    """ The saved left joystick value for its X axis in the positive. (0-1) """
    leftJoystickNegativeX:float = 0
    """ The saved left joystick value for its X axis in the negative. (0-1) """
    leftJoystickPositiveY:float = 0
    """ The saved left joystick value for its Y axis in the positive. (0-1) """
    leftJoystickNegativeY:float = 0
    """ The saved left joystick value for its Y axis in the negative. (0-1) """

    rightJoystickPositiveX:float = 0
    """ The saved right joystick value for its X axis in the positive. (0-1) """
    rightJoystickNegativeX:float = 0
    """ The saved right joystick value for its X axis in the negative. (0-1) """
    rightJoystickPositiveY:float = 0
    """ The saved right joystick value for its Y axis in the positive. (0-1) """
    rightJoystickNegativeY:float = 0
    """ The saved right joystick value for its Y axis in the negative. (0-1) """

    rightJoystickButton:bool = False
    """ The saved button value for the right joystick. """
    leftJoystickButton:bool = False
    """ The saved button value for the left joystick. """

    switch1:bool = False
    """ The saved state of Gamepad's switch1. """
    switch2:bool = False
    """ The saved state of Gamepad's switch2. """
    switch3:bool = False
    """ The saved state of Gamepad's switch3. """
    switch4:bool = False
    """ The saved state of Gamepad's switch4. """
    switch5:bool = False
    """ The saved state of Gamepad's switch5. """

    _lock = threading.Lock()

    @staticmethod
    def _handlingThread(uartClass, UART:UART):
        from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import BFIO, NewArrival, PassengerTypes, MandatoryPlaneIDs
        ################################################
        receivedAPlane:bool = False
        uartError:bool = False

        while True:

            if uartClass.stopEvent.is_set():
                break

            hardwareRequest = Plane(20, [], [])
            UART.QueuePlaneOnTaxiway(hardwareRequest)
            ###########################################
            time.sleep(0.040) # Gamepad sends 37 bytes at 9600 bauds meaning 31ms of TX time
            ###########################################
            receivedPlane:Passenger = UART.GetOldestReceivedGroupOfPassengers()
            if(receivedPlane != None):
                if(receivedPlane != Execution.Failed):
                    if(receivedPlane[0].value_8bits[1] == 20):
                        # This is an hardware readout! Youpii
                        receivedAPlane = True
                        receivedPlane = NewArrival(receivedPlane, hardwareVarTypes)
                else:
                    uartError = True
            ###########################################

            with uartClass._lock:

                if(uartError == True):
                    uartClass.isStarted = False
                    uartClass.errorMessage = "UART class is not started."

                if(receivedAPlane):
                    receivedAPlane = False

                    uartClass._realLeftJoystickX        = receivedPlane.GetParameter(0)
                    uartClass._realLeftJoystickY        = receivedPlane.GetParameter(1)
                    uartClass._realLeftJoystickButton   = receivedPlane.GetParameter(2)

                    uartClass._realRightJoystickX       = receivedPlane.GetParameter(3)
                    uartClass._realRightJoystickY       = receivedPlane.GetParameter(4)
                    uartClass._realRightJoystickButton  = receivedPlane.GetParameter(5)

                    uartClass._realSwitch1 = receivedPlane.GetParameter(6)
                    uartClass._realSwitch2 = receivedPlane.GetParameter(7)
                    uartClass._realSwitch3 = receivedPlane.GetParameter(8)
                    uartClass._realSwitch4 = receivedPlane.GetParameter(9)
                    uartClass._realSwitch5 = receivedPlane.GetParameter(10)
                pass
        ################################################
        uartClass.isStarted = False

    @staticmethod
    def StartDriver():
        """
            StartDriver:
            ============
            Summary:
            --------
            Starts a thread that reads
            all the informations of BFIODriver
            pins at intervals of 3 seconds

            Returns:
            --------
        """
        Debug.Start("BFIODriver -> StartDriver")

        if(Information.platform != "Linux"):
            Debug.Error(f"You cannot use this driver on your platform: {Information.platform}")
            Debug.End()
            return Execution.Incompatibility

        if BFIODriver.isStarted == False:
            BFIODriver.errorMessage = ""
            if not BFIODriver.thread or not BFIODriver.thread.is_alive():
                BFIODriver.stopEvent.clear()
                BFIODriver.thread = threading.Thread(target=BFIODriver._handlingThread, args=(BFIODriver,UART,))
                BFIODriver.thread.daemon = True
                BFIODriver.thread.start()
                BFIODriver.isStarted = True
                Debug.End()
                return Execution.Passed
        else:
            Debug.Error("Threads are already started. You cannot start more than 2.")
            Debug.End()
            return Execution.Unecessary
        Debug.Log("BFIODriver is now started")
        Debug.End()
        return Execution.Passed

    @staticmethod
    def StopDriver():
        """
            StopDriver:
            ============
            Summary:
            --------
            Stops the thread that handles
            the BFIO of GamePad.
        """
        Debug.Start("BFIODriver -> StopDriver")
        BFIODriver.stopEvent.set()

        if BFIODriver.thread and BFIODriver.thread.is_alive():
            BFIODriver.thread.join()

        BFIODriver.isStarted = False
        Debug.Log("thread is stopped.")
        Debug.End()
        return Execution.Passed

    #region ----------------------------------- Getter - Left Joystick Axis
    def Get_LeftJoystickXPositive() -> float:
        """
            Get_LeftJoystickXPositive:
            ==========================
            Summary:
            --------
            Returns the left joystick's
            X axis in the positive. (0-1)
        """
        if(BFIODriver.isStarted):
            leftJoystickX = (BFIODriver._realLeftJoystickX / 2048)
            if(leftJoystickX > 0):
                BFIODriver.leftJoystickPositiveX = leftJoystickX
                return leftJoystickX
            else:
                BFIODriver.leftJoystickPositiveX = 0
                return 0
        else:
            return 0

    def Get_LeftJoystickXNegative() -> float:
        """
            Get_LeftJoystickXNegative:
            ==========================
            Summary:
            --------
            Returns the left joystick's
            X axis in the negative. (0-1)
        """
        if(BFIODriver.isStarted):
            leftJoystickX = (BFIODriver._realLeftJoystickX / 2048)
            if(leftJoystickX < 0):
                BFIODriver.leftJoystickNegativeX = leftJoystickX * -1
                return BFIODriver.leftJoystickNegativeX
            else:
                BFIODriver.leftJoystickNegativeX = 0
                return 0
        else:
            return 0

    def Get_LeftJoystickYPositive() -> float:
        """
            Get_LeftJoystickYPositive:
            ==========================
            Summary:
            --------
            Returns the left joystick's
            Y axis in the positive. (0-1)
        """
        if(BFIODriver.isStarted):
            leftJoystickY = (BFIODriver._realLeftJoystickY / 2048)
            if(leftJoystickY > 0):
                BFIODriver.leftJoystickPositiveY = leftJoystickY
                return leftJoystickY
            else:
                BFIODriver.leftJoystickPositiveY = 0
                return 0
        else:
            return 0

    def Get_LeftJoystickYNegative() -> float:
        """
            Get_LeftJoystickYNegative:
            ==========================
            Summary:
            --------
            Returns the left joystick's
            Y axis in the negative. (0-1)
        """
        if(BFIODriver.isStarted):
            leftJoystickY = (BFIODriver._realLeftJoystickY / 2048)
            if(leftJoystickY < 0):
                BFIODriver.leftJoystickNegativeY = leftJoystickY * -1
                return BFIODriver.leftJoystickNegativeY
            else:
                BFIODriver.leftJoystickNegativeY = 0
                return 0
        else:
            return 0
    #endregion

    #region ----------------------------------- Getter - Right Joystick Axis
    def Get_RightJoystickXPositive() -> float:
        """
            Get_RightJoystickXPositive:
            ==========================
            Summary:
            --------
            Returns the right joystick's
            X axis in the positive. (0-1)
        """
        if(BFIODriver.isStarted):
            rightJoystickX = (BFIODriver._realRightJoystickX / 2048)
            if(rightJoystickX > 0):
                BFIODriver.rightJoystickPositiveX = rightJoystickX
                return rightJoystickX
            else:
                BFIODriver.rightJoystickPositiveX = 0
                return 0
        else:
            return 0

    def Get_RightJoystickXNegative() -> float:
        """
            Get_RightJoystickXNegative:
            ==========================
            Summary:
            --------
            Returns the right joystick's
            X axis in the negative. (0-1)
        """
        if(BFIODriver.isStarted):
            rightJoystickX = (BFIODriver._realRightJoystickX / 2048)
            if(rightJoystickX < 0):
                BFIODriver.rightJoystickNegativeX = rightJoystickX * -1
                return BFIODriver.rightJoystickNegativeX
            else:
                BFIODriver.rightJoystickNegativeX = 0
                return 0
        else:
            return 0

    def Get_RightJoystickYPositive() -> float:
        """
            Get_RightJoystickYPositive:
            ==========================
            Summary:
            --------
            Returns the right joystick's
            Y axis in the positive. (0-1)
        """
        if(BFIODriver.isStarted):
            rightJoystickY = (BFIODriver._realRightJoystickY / 2048)
            if(rightJoystickY > 0):
                BFIODriver.rightJoystickPositiveY = rightJoystickY
                return rightJoystickY
            else:
                BFIODriver.rightJoystickPositiveY = 0
                return 0
        else:
            return 0

    def Get_RightJoystickYNegative() -> float:
        """
            Get_RightJoystickYNegative:
            ==========================
            Summary:
            --------
            Returns the right joystick's
            Y axis in the negative. (0-1)
        """
        if(BFIODriver.isStarted):
            rightJoystickY = (BFIODriver._realRightJoystickY / 2048)
            if(rightJoystickY < 0):
                BFIODriver.rightJoystickNegativeY = rightJoystickY * -1
                return BFIODriver.rightJoystickNegativeY
            else:
                BFIODriver.rightJoystickNegativeY = 0
                return 0
        else:
            return 0
    #endregion

    #region ----------------------------------- Getter - Buttons
    def Get_LeftJoystickButton() -> bool:
        """
            Get_LeftJoystickButton:
            ==========================
            Summary:
            --------
            Returns the left joystick's
            button as a boolean. Will
            always return False if this
            class is not started.
        """
        if(BFIODriver.isStarted):
            button = BFIODriver._realLeftJoystickButton
            BFIODriver.leftJoystickButton = button
        else:
            return False

    def Get_RightJoystickButton() -> bool:
        """
            Get_RightJoystickButton:
            ==========================
            Summary:
            --------
            Returns the right joystick's
            button as a boolean. Will
            always return False if this
            class is not started.
        """
        if(BFIODriver.isStarted):
            button = BFIODriver._realRightJoystickButton
            BFIODriver.rightJoystickButton = button
        else:
            return False

    def Get_Switch1() -> bool:
        """
            Get_Switch1:
            ============
            Summary:
            --------
            Returns switch 1's value
            as a boolean. Will
            always return False if this
            class is not started.
        """
        if(BFIODriver.isStarted):
            button = BFIODriver._realSwitch1
            BFIODriver.switch1 = button
        else:
            return False

    def Get_Switch2() -> bool:
        """
            Get_Switch2:
            ============
            Summary:
            --------
            Returns switch 2's value
            as a boolean. Will
            always return False if this
            class is not started.
        """
        if(BFIODriver.isStarted):
            button = BFIODriver._realSwitch2
            BFIODriver.switch2 = button
        else:
            return False

    def Get_Switch3() -> bool:
        """
            Get_Switch3:
            ============
            Summary:
            --------
            Returns switch 3's value
            as a boolean. Will
            always return False if this
            class is not started.
        """
        if(BFIODriver.isStarted):
            button = BFIODriver._realSwitch3
            BFIODriver.switch3 = button
        else:
            return False

    def Get_Switch4() -> bool:
        """
            Get_Switch4:
            ============
            Summary:
            --------
            Returns switch 4's value
            as a boolean. Will
            always return False if this
            class is not started.
        """
        if(BFIODriver.isStarted):
            button = BFIODriver._realSwitch4
            BFIODriver.switch4 = button
        else:
            return False

    def Get_Switch5() -> bool:
        """
            Get_Switch5:
            ============
            Summary:
            --------
            Returns switch 5's value
            as a boolean. Will
            always return False if this
            class is not started.
        """
        if(BFIODriver.isStarted):
            button = BFIODriver._realSwitch5
            BFIODriver.switch5 = button
        else:
            return False
    #endregion
#====================================================================#
LoadingLog.End("driver.py")