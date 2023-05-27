import serial
import time
from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import BFIO, Debug, NewArrival, Plane, PassengerTypes, Passenger, MandatoryPlaneIDs, MandatoryFunctionRequestVarTypeLists, PrintPassenger, PrintPlane
from Libraries.BRS_Python_Libraries.BRS.Hardware.UART.receiver import UART, Execution
from Programs.Local.BFIO.kontrolBFIO import GetUniversalInfoPlane

# Define the serial port configurations
TIMEOUT = 0.1
# serial_port = "/dev/ttyAMA0"  # Serial 0 -> A -> TX1_B / RX1_B
serial_port = "/dev/ttyAMA2"  # Serial 2 -> D -> TX2_A
# serial_port = "/dev/ttyAMA3"  # Serial 3 -> C -> TX1_A / RX1_A
# serial_port = "/dev/ttyAMA4"  # Serial 4 -> E -> TX2_B / RX2_B
# serial_port = "/dev/ttyAMA5"  # Serial 5 -> F -> DEBUG / RX2_A


def InitUartClass():
    UART.serialPort = "/dev/ttyAMA2"
    result = UART.StartDriver()
    if(result != Execution.Passed):
        Debug.Error("Failed to start the UART BFIO driver.")
        Debug.End()
        return result
    Debug.Log("UART drivers started.")
    return Execution.Passed

def StopUART():
    return UART.StopDriver()

def TestHandshake():
    success = False

    Debug.enableConsole = False
    result = InitUartClass()
    print(f"InitUartClass returned {result}")
    if(result != Execution.Passed):
        pass
    else:
        print(f"Sending UniversalInfo to BrSpand card...")
        result = UART.QueuePlaneOnTaxiway(GetUniversalInfoPlane())
        print(f"{result}")
        if(result != Execution.Passed):
            print("Failed to queue universal info on taxiway.")
        else:
            print(f"Plane was sent on UART... maybe...")

            for timeSpent in range(5):
                time.sleep(1)
                pourcent = int((timeSpent/5)*100)
                print(f"================================[{pourcent}%]")
                result = UART.QueuePlaneOnTaxiway(GetUniversalInfoPlane())
                if(result != Execution.Passed):
                    print("Failed to queue univrsal info on taxiway.")

                print("Reading received planes:")

                newGroup = UART.GetOldestReceivedGroupOfPassengers()
                if(newGroup == Execution.Failed):
                    print(f"Something failed in GetOldestReceivedGroupOfPassengers: {newGroup}")
                else:
                    if(newGroup != None):
                        planeIsMandatory = BFIO.IsPassengerGroupAMandatoryPlane(newGroup)
                        if(planeIsMandatory):
                            plane = BFIO.ParsePassengersIntoMandatoryPlane(newGroup)
                            if(plane.passedTSA):
                                print("Universal information gathered.")
                                Debug.enableConsole = True
                                PrintPlane(plane)
                                Debug.enableConsole = False
                                return True
                    else:
                        print("new passenger group is null.")
    print("Stopping threads")
    UART.StopDriver()
    return False


from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import VarTypes
def TestValues():
    success = False

    UART.Reset()

    hardwareVarTypes = [VarTypes.Int, VarTypes.Int, VarTypes.Bool, VarTypes.Int, VarTypes.Int, VarTypes.Bool, VarTypes.Bool, VarTypes.Bool, VarTypes.Bool, VarTypes.Bool, VarTypes.Bool]

    hardwareRequest = Plane(20, [], [])

    Debug.enableConsole = False
    # result = InitUartClass()
    # print(f"InitUartClass returned {result}")
    # if(result != Execution.Passed):
        # pass
    # else:
    print(f"Sending hardware request to BrSpand card...")
    result = UART.QueuePlaneOnTaxiway(hardwareRequest)
    print(f"{result}")
    if(result != Execution.Passed):
        print("Failed to queue info on taxiway.")
    else:
        print(f"Plane was sent on UART... maybe...")

        for timeSpent in range(5):
            time.sleep(1)
            pourcent = int((timeSpent/5)*100)
            print(f"================================[{pourcent}%]")
            result = UART.QueuePlaneOnTaxiway(hardwareRequest)
            if(result != Execution.Passed):
                print("Failed to queue hardware request on taxiway")

            print("Reading received planes:")

            # Debug.enableConsole = True
            newGroup = UART.GetOldestReceivedGroupOfPassengers()
            # Debug.enableConsole = False
            if(newGroup == Execution.Failed):
                print(f"Something failed in GetOldestReceivedGroupOfPassengers: {newGroup}")
            else:
                if(newGroup != None):
                    planeIsMandatory = BFIO.IsPassengerGroupAMandatoryPlane(newGroup)
                    print(f"It is {planeIsMandatory} that this plane is mandatory.")

                    for passenger in newGroup:
                        Debug.enableConsole = True
                        PrintPassenger(passenger)
                        Debug.enableConsole = False

                    if(planeIsMandatory):
                        plane = BFIO.ParsePassengersIntoMandatoryPlane(newGroup)
                        if(plane.passedTSA):
                            print("Hardware information gathered.")
                            Debug.enableConsole = True
                            PrintPlane(plane)
                            Debug.enableConsole = False
                            return True
                    else:
                        receivedPlane = NewArrival(receivedPlane, hardwareVarTypes)


                        leftJoystickX = 


                        Debug.enableConsole = True
                        PrintPlane(receivedPlane)
                        Debug.enableConsole = False
                        return True
                else:
                    print("new passenger group is null.")
    print("Stopping threads")
    UART.StopDriver()
    return False

if(__name__ == "__main__"):
    result = TestHandshake()
    if(result == False):
        print("[[[[[[[[[[[[[[[[ - FAIL- ]]]]]]]]]]]]]]]]")

    print("(((((((((((((((( NEXT ))))))))))))))))")
    result = TestValues()
    if(result == False):
        print("[[[[[[[[[[[[[[[[ - FAIL- ]]]]]]]]]]]]]]]]")