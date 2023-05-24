# from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import Plane, NewArrival, VarTypes, Execution, Passenger, PassengerTypes, Debug
# from Libraries.BRS_Python_Libraries.BRS.Utilities.Information import Information
# from Local.Drivers.Batiscan.Programs.Controls.controls import BatiscanControls

# ################################################
# def GetPing() -> list:
#     """
#     """
#     return [True]
# ################################################
# def GetStatus() -> list:
#     """
#     """
#     return [1]
# ################################################
# def GetHandshake() -> list:
#     """
#     """
#     return []
# ################################################
# def GetErrorMessage() -> list:
#     """
#     """
#     return ["no errors"]
# ################################################
# ################################################
# def GetType() -> list:
#     """
#     """
#     return [1]
# ################################################
# def GetID() -> list:
#     """
#         GetIDPlane:
#         =============
#         Summary:
#         --------
#         Gets a plane that requests the other
#         device to send their ID all the while
#         you're sending an ID.

#     """
#     return [1234567890]
# ################################################
# def GetRestartProtocol() -> list:
#     """
#     """
#     return []
# ################################################
# def GetUniversalInfoUpdate() -> list:
#     """
#         GetUniversalInfoUpdate:
#         ======================
#         Summary:
#         --------
#         Gets a plane that requests the other
#         device to send their ID all the while
#         you're sending an ID.
#     """
#     return [
#                     1234567890,                                     # unique device ID
#                     1,                                              # BFIO version
#                     1,                                              # Device type
#                     1,                                              # Device status
#                     "https://github.com/LyamBRS/BRS-Kontrol.git",   # Git repository of the device.
#                     Information.name,                               # name of the device
#                     Information.softwareVersion                     # Software version of the device.
#                 ]
# ################################################
# def GetHandlingError() -> list:
#     """
#         GetHandlingError:
#         ================
#         Summary:
#         --------
#         Gets a plane that is made to
#         specify that there has been
#         an handling error with the methods.
#     """
#     return = []
# ################################################




# ################################################
# def GetUpdateLights() -> list:
#     """
#     """
#     return [BatiscanControls.wantedLeftLight, BatiscanControls.wantedRightLight]
# ################################################
# def GetUpdateServos() -> list:
#     """
#     """
#     return [BatiscanControls.wantedServoA, BatiscanControls.wantedServoB, BatiscanControls.wantedServoC, BatiscanControls.wantedServoD, BatiscanControls.wantedServoE]
# ################################################
# def GetUpdateModes() -> Plane:
#     """
#     """
#     return [BatiscanControls.wantedMode, BatiscanControls.wantedTemperatureUnit]
# ################################################
# def GetUpdateCamera() -> Plane:
#     """
#         GetUpdateCamera:
#         =====================
#         Summary:
#         --------
#     """
#     return [BatiscanControls.wantedCameraStatus, BatiscanControls.wantedCameraAngle]
# ################################################
# def GetAllState() -> Plane:
#     """
#     """
#     return []
# ################################################
# def GetAllSensor() -> Plane:
#     """
#     """
#     return []
# ################################################
# def GetUpdateNavigation() -> Plane:
#     """
#     """
#     return [BatiscanControls.wantedSpeed, BatiscanControls.wantedPitch, BatiscanControls.wantedRoll, BatiscanControls.wantedYaw]
# ################################################
# def GetSetBallast() -> Plane:
#     """
#     """
#     return [BatiscanControls.wantedBallast]
# ################################################
# def GetSurfaceNow() -> Plane:
#     """
#     """
#     return []



# class PlaneIDs:
#     ping:int = 0
#     status:int = 1
#     handshake:int = 2
#     errorMessage:int = 3
#     deviceType:int = 4
#     uniqueID:int = 5
#     restartProtocol:int = 6
#     universalInfo:int = 7
#     communicationError:int = 8

#     lightsUpdate:int = 20
#     servoUpdate:int = 21
#     modeUpdate:int = 22
#     cameraUpdate:int = 23
#     allStates:int = 24
#     allSensors:int = 25
#     navigationUpdate:int = 26
#     ballastUpdate:int = 27
#     surface:int = 28

# sentVarTypes = {
#     PlaneIDs.ping               : [VarTypes.Bool],
#     PlaneIDs.status             : [VarTypes.Unsigned.Char],
#     PlaneIDs.handshake          : [],
#     PlaneIDs.errorMessage       : [VarTypes.String],
#     PlaneIDs.deviceType         : [VarTypes.Unsigned.Char],
#     PlaneIDs.uniqueID           : [VarTypes.Unsigned.LongLong],
#     PlaneIDs.restartProtocol    : [],
#     PlaneIDs.universalInfo      : [VarTypes.Unsigned.LongLong, VarTypes.Unsigned.Long, VarTypes.Unsigned.Char, VarTypes.Unsigned.Char, VarTypes.String, VarTypes.String, VarTypes.String],
#     PlaneIDs.communicationError : [],
#     PlaneIDs.lightsUpdate       : [VarTypes.Bool, VarTypes.Bool],
#     PlaneIDs.servoUpdate        : [VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char],
#     PlaneIDs.modeUpdate         : [VarTypes.Char, VarTypes.Char],
#     PlaneIDs.cameraUpdate       : [VarTypes.Bool, VarTypes.Signed.Char],
#     PlaneIDs.allStates          : [],
#     PlaneIDs.allSensors         : [],
#     PlaneIDs.navigationUpdate   : [VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char],
#     PlaneIDs.ballastUpdate      : [VarTypes.Bool],
#     PlaneIDs.surface            : [],
# }

# receivedVarTypes = {
#     PlaneIDs.ping               : [VarTypes.Bool],
#     PlaneIDs.status             : [VarTypes.Unsigned.Char],
#     PlaneIDs.handshake          : [],
#     PlaneIDs.errorMessage       : [VarTypes.String],
#     PlaneIDs.deviceType         : [VarTypes.Unsigned.Char],
#     PlaneIDs.uniqueID           : [VarTypes.Unsigned.LongLong],
#     PlaneIDs.restartProtocol    : [],
#     PlaneIDs.universalInfo      : [VarTypes.Unsigned.LongLong, VarTypes.Unsigned.Long, VarTypes.Unsigned.Char, VarTypes.Unsigned.Char, VarTypes.String, VarTypes.String, VarTypes.String],
#     PlaneIDs.communicationError : [],
#     PlaneIDs.lightsUpdate       : [VarTypes.Bool, VarTypes.Bool],
#     PlaneIDs.servoUpdate        : [VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char],
#     PlaneIDs.modeUpdate         : [VarTypes.Char, VarTypes.Char],
#     PlaneIDs.cameraUpdate       : [VarTypes.Bool, VarTypes.Signed.Char],
#     PlaneIDs.allStates          : [VarTypes.Bool, VarTypes.Bool, VarTypes.Bool, VarTypes.Bool, VarTypes.Bool,VarTypes.Bool, VarTypes.Bool, VarTypes.Bool],
#     PlaneIDs.allSensors         : [VarTypes.Int, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Unsigned.Char],
#     PlaneIDs.navigationUpdate   : [VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char, VarTypes.Signed.Char],
#     PlaneIDs.ballastUpdate      : [VarTypes.Bool],
#     PlaneIDs.surface            : [VarTypes.Bool],
# }

# getters = {
#     PlaneIDs.ping               : GetPing,
#     PlaneIDs.status             : GetStatus,
#     PlaneIDs.handshake          : GetHandshake,
#     PlaneIDs.errorMessage       : GetErrorMessage,
#     PlaneIDs.deviceType         : GetType,
#     PlaneIDs.uniqueID           : GetID,
#     PlaneIDs.restartProtocol    : GetRestartProtocol,
#     PlaneIDs.universalInfo      : GetUniversalInfoUpdate,
#     PlaneIDs.communicationError : GetHandlingError,
#     PlaneIDs.lightsUpdate       : GetUpdateLights,
#     PlaneIDs.servoUpdate        : GetUpdateServos,
#     PlaneIDs.modeUpdate         : GetUpdateModes,
#     PlaneIDs.cameraUpdate       : GetUpdateCamera,
#     PlaneIDs.allStates          : GetAllState,
#     PlaneIDs.allSensors         : GetAllSensor,
#     PlaneIDs.navigationUpdate   : GetUpdateNavigation,
#     PlaneIDs.ballastUpdate      : GetSetBallast,
#     PlaneIDs.surface            : GetSurfaceNow,
# }


# def SendUDPMessage(ip_address, port, message:str):
#     try:
#         import socket
#         # Create a UDP socket
#         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#         # Send the message
#         sock.sendto(message.encode('utf-8'), (ip_address, port))

#         # Close the socket
#         sock.close()
#         return True
#     except Exception as e:
#         Debug.Error("FAILED TO SEND SOCKET")
#         return False

# def MakeAPlaneOutOfArrivedPassengers(passengers:list) -> NewArrival:
#     """
#         MakeAPlaneOutOfArrivedPassengers:
#         =================================
#         Summary:
#         --------
#         Creates a plane out of a list of arrived
#         passengers depending on the pilot's ID.

#         Arguments:
#         ----------
#         - `passengers:list` a list of passenger objects.
#     """

#     pilot:Passenger = passengers[0]
#     if(pilot.type != PassengerTypes.Pilot):
#         Debug.Error("Err first passenger isnt a pilot mate...")
#         return Execution.Failed
    
#     planeID = pilot.value_8bits[1]
#     try:
#         newArrival = NewArrival(passengers, receivedVarTypes[planeID])
#         return newArrival
#     except:
#         Debug.Error("PLANE DOES NOT EXIST / ISNT SUPPORTED")

# def SendAPlaneOnUDP(functionID:int) -> Execution:
#     """
#         SendAPlaneOnUDP:
#         ================
#         Summary:
#         --------
#         Sends a plane on the UDP made of given parameters
#     """
#     ipAddress = "192.168.4.1"
#     port = 4210

#     try:
#         planeToSend = Plane(functionID, getters[functionID](), sentVarTypes[functionID])
#     except:
#         Debug.Error("FAILED TO CREATE PLANE BRUH")
    
#     try:
#         import socket
#         # Create a UDP socket
#         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#         for passenger in planeToSend.passengers:
#             # Send the message
#             sock.sendto(passenger.value_8bits[0].encode('utf-8'), (ipAddress, port))
#             sock.sendto(passenger.value_8bits[1].encode('utf-8'), (ipAddress, port))

#         # Close the socket
#         sock.close()
#         return True
#     except Exception as e:
#         Debug.Error("FAILED TO SEND SOCKET")
#         return False