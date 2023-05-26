import serial
import time
from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import BFIO, Debug, NewArrival, Plane, PassengerTypes, Passenger, MandatoryPlaneIDs, MandatoryFunctionRequestVarTypeLists, PrintPlane
from Programs.Local.BFIO.kontrolBFIO import GetUniversalInfoPlane

# Define the serial port configurations
TIMEOUT = 0.1
# serial_port = "/dev/ttyAMA0"  # Serial 0 -> A -> TX1_B / RX1_B
serial_port = "/dev/ttyAMA2"  # Serial 2 -> D -> TX2_A
# serial_port = "/dev/ttyAMA3"  # Serial 3 -> C -> TX1_A / RX1_A
# serial_port = "/dev/ttyAMA4"  # Serial 4 -> E -> TX2_B / RX2_B
# serial_port = "/dev/ttyAMA5"  # Serial 5 -> F -> DEBUG / RX2_A


serialObject = serial.Serial(serial_port, baudrate=9600, timeout=TIMEOUT)
################################################
def GetPassengerArrivals() -> list:
    """
        Only reads passengers that arrived.
        returns them in groupes of 2.
    """
    # Clear the buffer of any passengers.
    newArrivals = []
    while serialObject.in_waiting >= 2:
        try:
            data = serialObject.read(2)
            # print(f"{data[0]}, {data[1]}")
            if(data[0] > 3):
                print("Fuck up detected. Offsetting by 1 value.")
                serialObject.read(1)
        except:
            print(f"Timed out when trying to read bytes.")
        passengerList = BFIO.GetPassengersFromDualBytes(data)
        
        for passenger in passengerList:
            if(passenger.passedTSA):
                newArrivals.append(passenger)
            else:
                print(f">>> {passenger.initErrorMessage} ")
    
    return newArrivals
################################################
################################################
class stupidPython:
    receivingPlane:bool = False
    receivedPassengers:list = []

def HandleNewArrivals() -> NewArrival:
    """
        Appends passengers to a list.
        Only starts doing so when it saw
        a pilot in the new arrivals.
        Stops when a co-pilot is seen.
    """
    arrivedPassengers = []
    # Get passengers that arrived.
    newArrivals = GetPassengerArrivals()
    print(f"Concatenating arrivals to a list of {len(stupidPython.receivedPassengers)}")
    for arrival in newArrivals:
        
        if(not stupidPython.receivingPlane):
            if(arrival.type == PassengerTypes.Pilot):
                print("Pilot received.")
                stupidPython.receivingPlane = True
                stupidPython.receivedPassengers.clear()
                stupidPython.receivedPassengers.append(arrival)
        else:
            print(f"Adding passengers to a list of {len(stupidPython.receivedPassengers)}")
            if(arrival.type == PassengerTypes.CoPilot):
                # The rear of a plane was received
                stupidPython.receivingPlane = False
                print("Co-Pilot received")

            stupidPython.receivedPassengers.append(arrival)
            if(stupidPython.receivingPlane == False):
                print("Passengers grouped into plane.")
                arrivedPassengers.append(stupidPython.receivedPassengers.copy())
    return arrivedPassengers
################################################
def BuildPlanesFromPassengers():
    """
        Tests if lists of passengers within
        the returned passenger lists fit in
        specific classes.
    """
    landedPlanes = []

    arrivedGroupsOfPassengers = HandleNewArrivals()
    print(f"{len(arrivedGroupsOfPassengers)} groups of passengers can be parsed into planes.")
    if(len(arrivedGroupsOfPassengers) > 0):
        for group in arrivedGroupsOfPassengers:
            if(group[0].value_8bits[1] == MandatoryPlaneIDs.universalInfo):
                print("UNIVERSAL PLANE LANDED")
                Debug.enableConsole = True
                landedPlane = NewArrival(group, MandatoryFunctionRequestVarTypeLists[MandatoryPlaneIDs.universalInfo])
                Debug.enableConsole = False
                print(f"It is {landedPlane.passedTSA} that this plane passed TSA.")
                landedPlanes.append(landedPlane)
            else:
                print(f"An unknown plane with a callsign of {group[0].value_8bits[1]} landed.")
    return landedPlanes
################################################
def TestBFIOArrivals():
    for timeSlept in range(100):
        pourcentLeft = (timeSlept/100)*100
        print(f"======================================================== [{int(pourcentLeft)}%]")
        maybe = "" if stupidPython.receivingPlane else "not "
        print(f"Currently, we are {maybe}receiving a plane.")
        print(f"Currently, there is {len(stupidPython.receivedPassengers)} passengers received.")
        print(f"\n")
        time.sleep(0.1)

        receivedPlanes = BuildPlanesFromPassengers()
        print(f">>> {len(receivedPlanes)} planes were received.")
        for plane in receivedPlanes:
            if plane.passedTSA == True:
                print("A plane passed TSA! O_O")
                print(f"\n")
                print(f"\n")
                print(f"\n")
                Debug.enableConsole = True
                PrintPlane(plane)
                Debug.enableConsole = False
                return
            else:
                print("A plane failed TSA checks")
        
        print("Sending a plane on taxiway?")
        serialObject.write(GetUniversalInfoPlane())
################################################
TestBFIOArrivals()
serialObject.close()
print("[[[[[[[[[[[[[[[[ - END- ]]]]]]]]]]]]]]]]")
