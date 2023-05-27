import serial
import time
from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import BFIO, Debug, NewArrival, Plane, PassengerTypes, Passenger, MandatoryPlaneIDs, MandatoryFunctionRequestVarTypeLists, PrintPlane
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


if(__name__ == "__main__"):
    Debug.enableConsole = True
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
                                PrintPlane(plane)
                                break
                    else:
                        print("new passenger group is null.")
    print("Stopping threads")
    UART.StopDriver()

print("[[[[[[[[[[[[[[[[ - END- ]]]]]]]]]]]]]]]]")
