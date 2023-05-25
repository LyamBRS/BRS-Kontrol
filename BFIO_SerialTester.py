import serial
import time
from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import BFIO, NewArrival, Plane, PassengerTypes, Passenger, MandatoryPlaneIDs, MandatoryFunctionRequestVarTypeLists, PrintPlane

# Define the serial port configurations
TIMEOUT = 0.1
serial_port = "/dev/ttyAMA0"  # Serial 0 -> A -> TX1_B / RX1_B
# serial_port = "/dev/ttyAMA2"  # Serial 2 -> D -> TX2_A
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
        except:
            print(f"Timed out when trying to read bytes.")
        passenger = BFIO.GetPassengersFromDualBytes([data[0], data[1]])
        newArrivals.append(passenger)
    
    return newArrivals
################################################
################################################
receivedPassengers:list = []
receivingPlane:bool = False
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

    for arrival in newArrivals:
        
        if(not receivingPlane):
            if(arrival.type == PassengerTypes.Pilot):
                receivingPlane = True
                receivedPassengers.clear()
                receivedPassengers.append(arrival)
        else:
            if(arrival.type == PassengerTypes.CoPilot):
                # The rear of a plane was received
                receivingPlane = False

            receivedPassengers.append(arrival)
            if(receivingPlane == False):
                arrivedPassengers.append(receivedPassengers.copy())
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
    if(len(arrivedGroupsOfPassengers) > 0):
        for group in arrivedGroupsOfPassengers:
            if(group[0].value_8bits[1] == MandatoryPlaneIDs.universalInfo):
                print("UNIVERSAL PLANE LANDED")
                landedPlane = NewArrival(group, MandatoryFunctionRequestVarTypeLists[MandatoryPlaneIDs.universalInfo])
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
        maybe = "" if receivingPlane else "not"
        print(f"Currently, we are {maybe} receiving a plane.")
        print(f"Currently, there is {len(receivedPassengers)} passengers received.")
        print(f"\n")
        time.sleep(0.01)

        receivedPlanes = BuildPlanesFromPassengers()
        if(len(receivedPlanes) > 0):
            print("PLANE WAS RECEIVED!")
            print("\n\n\n\n")
            PrintPlane(receivedPlanes[0])
            break
################################################
TestBFIOArrivals()
serialObject.close()
print("[[[[[[[[[[[[[[[[ - END- ]]]]]]]]]]]]]]]]")
