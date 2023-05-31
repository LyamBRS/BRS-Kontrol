#====================================================================#
# File Information
#====================================================================#
"""
    UDP.py
    ======
    This file contains a thread class much like UDP, LeftBrSpand,
    Accelerometer and so on. This thread class's purpose is to handle
    receptions and transmissions of UDP data to and from Batiscan
    in threads to avoid lag.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import LoadingLog
from Libraries.BRS_Python_Libraries.BRS.Network.UDP.sender import UDPSender
from Libraries.BRS_Python_Libraries.BRS.PnP.controls import Controls
from Local.Drivers.Batiscan.Programs.Communications.planes import ExecuteArrivedPlane
LoadingLog.Start("UDP.py")
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
from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import BFIO
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Network.UDP.receiver import UDPReader
#endregion
#region -------------------------------------------------------- Kivy
# LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ Batiscan
LoadingLog.Import('Batiscan')
from Local.Drivers.Batiscan.Programs.Communications.bfio import PlaneIDs, SendAPlaneOnUDP, getters
from Local.Drivers.Batiscan.Programs.Controls.actions import BatiscanActions
#endregion
#====================================================================#
# Functions
#====================================================================#
def StartUDP() -> Execution:
    """
        StartUDP:
        =========
        Summary:
        --------
        Starts UDP threads. Will return an Execution value to
        indicate how the start went. If UDP can't start, you can't
        communicate with Batiscan.

        This starts UDP reader as well.

        Returns:
        --------
        - `Execution.Passed` = UDP is started and working.
        - `Execution.Failed` = Random failure occured and UDP couldn't start.
        - `Execution.NoConnection` = UDP reader or sender could not start.
    """
    Debug.Start("StartUDP")

    UDPReader.timeoutInSeconds = 0.5
    UDPReader.port = 4211
    UDPSender.port = 4210
    UDPSender.ipAddress = "192.168.4.2"

    result = UDPReader.StartDriver()
    if(result != Execution.Passed):
        Debug.Error("Failed to start UDPReader. We won't be able to receive data from Batiscan.")
        Debug.End()
        return Execution.NoConnection

    result = UDPSender.StartDriver()
    if(result != Execution.Passed):
        Debug.Error("Failed to start UDPSender. We won't be able to send data to Batiscan.")
        Debug.End()
        return Execution.NoConnection
    
    result = BatiscanUDP.StartDriver()
    if(result != Execution.Passed):
        Debug.Error("Failed to start BatiscanUDP. We won't be able to send data to Batiscan.")
        Debug.End()
        return Execution.NoConnection
    
    # from Programs.Communications.bfio import GetUniversalInfoUpdate
    # BatiscanUDP

    Debug.End()
    return Execution.Passed

def StopUDP() -> Execution:
    """
        StopUDP:
        ========
        Summary:
        --------
        Stops all UDP threads running for Batiscan.
        This is called when the Device Driver exits to ensure
        that no stray threads are still running.
    """
    Debug.Start("StopUDP")

    result = BatiscanUDP.StopDriver()
    if(result != Execution.Passed):
        Debug.Error("Failed to stop BatiscanUDP.")
        Debug.End()
        return Execution.NoConnection

    result = UDPReader.StopDriver()
    if(result != Execution.Passed):
        Debug.Error("Failed to stop UDPReader.")
        Debug.End()
        return Execution.NoConnection

    result = UDPSender.StopDriver()
    if(result != Execution.Passed):
        Debug.Error("Failed to stop UDPSender.")
        Debug.End()
        return Execution.NoConnection
    
    Debug.End()
    return Execution.Passed
#====================================================================#
# Classes
#====================================================================#
class BatiscanUDP:
    """
        BatiscanUDP:
        ========
        Summary:
        --------
        Class made to create a thread
        that handles :ref:`UDPReader` and :ref:`UDPSender` for
        Batiscan to use for their things.

        This class will parse incoming planes, generate outgoing
        planes and much more.
    """

    thread = None
    """ private thread object from :ref:`Threading`."""
    stop_event = threading.Event()
    isStarted: bool = False
    lock = threading.Lock()


    @staticmethod
    def _Thread(udpClass, ExecutePlane, Getters, Controls:Controls, StateFlippers:BatiscanActions):

        count = 0
        planeToSend = None
        from Local.Drivers.Batiscan.Programs.Communications.planes import MakeAPlaneOutOfArrivedBytes
        from Libraries.BRS_Python_Libraries.BRS.PnP.controls import SoftwareAxes, SoftwareButtons

        batiscanAxesActions = {
            SoftwareAxes.pitch_up    : 0,
            SoftwareAxes.pitch_down  : 0,
            SoftwareAxes.roll_left   : 0,
            SoftwareAxes.roll_right  : 0,
            SoftwareAxes.yaw_left    : 0,
            SoftwareAxes.yaw_right   : 0,
            SoftwareAxes.up          : 0,
            SoftwareAxes.down        : 0
        }
        """
            A list of all the software axes being used by Batiscan when its
            GUI is loaded and going and their associated descriptions. 
            The names within this list are extracted from :ref:`Controls`. 
            :ref:`SoftwareAxis` and this dictionary is used to keep old
            values to avoid useless updates and planes sent to Batiscan.
        """
        
        batiscanButtonsActions = {
        SoftwareButtons.fill         : False,
        SoftwareButtons.empty        : False,
        SoftwareButtons.reset        : False,
        SoftwareButtons.forward      : False,
        SoftwareButtons.backward     : False,
        SoftwareButtons.up           : False,
        SoftwareButtons.down         : False,
        SoftwareButtons.left         : False,
        SoftwareButtons.right        : False,
        SoftwareButtons.on           : False,
        SoftwareButtons.off          : False,
        SoftwareButtons.custom_1     : False,
        SoftwareButtons.custom_2     : False
        }
        """
            A list of all the software buttons being used by Batiscan when its
            GUI is loaded and going and their associated descriptions. 
            The names within this list are extracted from :ref:`Controls`. 
            :ref:`SoftwareButtons`
        """

        def CurrentButtonValue(name:str) -> bool:
            if(Controls._buttons[name]["binded"]):
                if(Controls._buttons[name]["getter"] != None):
                    newValue = Controls._buttons[name]["getter"]()
                    return newValue
            return False

        def HandleAddons():
            """
                HandleAddons:
                =============
                Summary:
                --------
                Handles the sending of planes
                related to addons getters.
                See Batiscan's controls for
                more informations about this
                one.
            """
            newOnValue = CurrentButtonValue(SoftwareButtons.on)
            if(batiscanButtonsActions[SoftwareButtons.on] != newOnValue):
                batiscanButtonsActions[SoftwareButtons.on] = newOnValue
                if(newOnValue == True):
                    StateFlippers.LightsWantedOn()
                    SendAPlaneOnUDP(PlaneIDs.lightsUpdate, Getters)
                    time.sleep(0.030)

            newOffValue = CurrentButtonValue(SoftwareButtons.off)
            if(batiscanButtonsActions[SoftwareButtons.off] != newOffValue):
                batiscanButtonsActions[SoftwareButtons.off] = newOffValue
                if(newOffValue == True):
                    StateFlippers.LightsWantedOff()
                    SendAPlaneOnUDP(PlaneIDs.lightsUpdate, Getters)
                    time.sleep(0.030)

        while True:
            if udpClass.stop_event.is_set():
                break
            ##################################################
            oldestMessage = UDPReader.GetOldestMessage()
            if(oldestMessage != None):
                for sender,message in oldestMessage.items():
                    Debug.Log(f"New plane from {sender}:")
                    arrival = MakeAPlaneOutOfArrivedBytes(message)
                ##################################################

            HandleAddons()
            if(count == 2):
    
                ###############################################################
                forward = None
                if(Controls._axes[SoftwareAxes.backward]["binded"] == True):
                    pass
                    forward = Controls._axes[SoftwareAxes.backward]["getter"]()
                # else:
                    # forward = None
# 
                backward = None
                if(Controls._axes[SoftwareAxes.forward]["binded"] == True):
                    pass
                    # backward = Controls._axes[SoftwareAxes.forward]["getter"]()
                # else:
                    # backward = None
# 
                # if(forward != None and backward != None):
                    # if(forward > backward):
                        # StateFlippers.SetNewSpeed(forward)
                    # else:
                        # StateFlippers.SetNewSpeed(backward-1)
                ##############################################################
                # if(Controls._axes[SoftwareAxes.yaw_right]["binded"] == True):
                    # yaw_right = Controls._axes[SoftwareAxes.yaw_right]["getter"]()
                # else:
                    # yaw_right = None
# 
                # if(Controls._axes[SoftwareAxes.yaw_left]["binded"] == True):
                    # yaw_left = Controls._axes[SoftwareAxes.yaw_left]["getter"]()
                # else:
                    # yaw_left = None
# 
                # if(yaw_right != None and yaw_left != None):
                    # if(yaw_right > yaw_left):
                        # StateFlippers.SetNewYaw(yaw_right)
                    # else:
                        # StateFlippers.SetNewSpeed(yaw_left - 1)
                ##############################################################
                # if(Controls._axes[SoftwareAxes.roll_right]["binded"] == True):
                    # roll_right = Controls._axes[SoftwareAxes.roll_right]["getter"]()
                # else:
                    # roll_right = None
# 
                # if(Controls._axes[SoftwareAxes.roll_left]["binded"] == True):
                    # roll_left = Controls._axes[SoftwareAxes.roll_left]["getter"]()
                # else:
                    # roll_left = None
# 
                # if(roll_right != None and roll_left != None):
                    # if(roll_right > roll_left):
                        # StateFlippers.SetNewYaw(roll_right)
                    # else:
                        # StateFlippers.SetNewSpeed(-roll_left)
                ##############################################################
                # if(Controls._axes[SoftwareAxes.pitch_up]["binded"] == True):
                    # pitch_up = Controls._axes[SoftwareAxes.pitch_up]["getter"]()
                # else:
                    # pitch_up = None
# 
                # if(Controls._axes[SoftwareAxes.pitch_down]["binded"] == True):
                    # pitch_down = Controls._axes[SoftwareAxes.pitch_down]["getter"]()
                # else:
                    # pitch_down = None
# 
                # if(pitch_up != None and pitch_down != None):
                    # if(pitch_up > pitch_down):
                        # StateFlippers.SetNewYaw(pitch_up)
                    # else:
                        # StateFlippers.SetNewSpeed(-pitch_down)
# 
                SendAPlaneOnUDP(PlaneIDs.navigationUpdate, Getters)
                time.sleep(0.030) 
                count = 0

            if udpClass.stop_event.is_set():
                break

            if(count == 1):
                SendAPlaneOnUDP(PlaneIDs.allSensors, Getters)
                time.sleep(0.030)
                count = 2

            if udpClass.stop_event.is_set():
                break

            if(count == 0):
                SendAPlaneOnUDP(PlaneIDs.allStates, Getters)
                time.sleep(0.030)
                count = 1

            if udpClass.stop_event.is_set():
                break

            if(planeToSend != None):
                SendAPlaneOnUDP(planeToSend, Getters)
                time.sleep(0.030)
                planeToSend = None

            if udpClass.stop_event.is_set():
                break

            try:
                with udpClass.lock:
                    planeToSend = BatiscanUDP._thingToSend
                    BatiscanUDP._thingToSend = None

                    if(arrival != None):
                        ExecutePlane(arrival)
                        arrival = None
                    pass
            except:
                pass
        udpClass.isStarted = False

    @staticmethod
    def StartDriver():
        """
            StartDriver:
            ============
            Summary:
            --------
            Starts the UDP threads
            handled by Batiscan. returns
            Execution.Passed if successful.

            This needs to be done after you
            started :ref:`UDPReader` and :ref:`UDPSender`
        """
        Debug.Start("BatiscanUDP -> StartDriver")
        if (BatiscanUDP.isStarted == False):
            if (not BatiscanUDP.thread or not BatiscanUDP.thread.is_alive()):
                BatiscanUDP.stop_event.clear()
                BatiscanUDP.thread = threading.Thread(target=BatiscanUDP._Thread, args=(BatiscanUDP, ExecuteArrivedPlane, getters, Controls, BatiscanActions, ))
                BatiscanUDP.thread.daemon = True
                BatiscanUDP.thread.start()
                BatiscanUDP.isStarted = True
                Debug.Log("BatiscanUDP is started.")
                Debug.End()
                return Execution.Passed
        else:
            Debug.Error("Thread is already started. You cannot start more than one.")
            Debug.End()
            return Execution.Failed
        Debug.Log("BatiscanUDP is now started")
        Debug.End()
        return Execution.Passed

    @staticmethod
    def StopDriver():
        """
            StopDriver:
            ============
            Summary:
            --------
            Stops the driver from sending anymore
            UDP stuff. DOES NOT CLEAR THE BUFFER
            OF THIS CLASS
        """
        Debug.Start("BatiscanUDP -> StopDriver")
        BatiscanUDP.stop_event.set()
        if BatiscanUDP.thread and BatiscanUDP.thread.is_alive():
            BatiscanUDP.thread.join()
        Debug.Log("Thread is stopped.")
        Debug.End()
        return Execution.Passed

    @staticmethod
    def SendThing(thingToSend) -> Execution:
        """
            SendThing:
            ==========
            Summary:
            --------
            Sets what to send on the UDP.
            It will be set back to `None` once
            its sent.
        """
        Debug.Start("SendThing")

        if(BatiscanUDP.isStarted):
            with BatiscanUDP.lock:
                BatiscanUDP._thingToSend = thingToSend
            Debug.Log("New thing to send has been specified.")
        else:
            Debug.Log("THREAD IS NOT STARTED. NO UDP MESSAGES CAN BE RETURNED")
            Debug.End()
            return Execution.Failed

        Debug.End()
#====================================================================#
LoadingLog.End("driver.py")