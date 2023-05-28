from Libraries.BRS_Python_Libraries.BRS.Network.UDP.receiver import UDPReader, Debug, Execution, time
from Local.Drivers.Batiscan.Programs.Communications.bfio import PlaneIDs, SendAPlaneOnUDP, MakeAPlaneOutOfArrivedBytes
Debug.enableConsole = True

# DONT FORGET TO SOMEHOW FIND WAY TO CHECK WTF IS BEING SENT

Debug.Start("=====================================")
Debug.Log("Starting driver...")
UDPReader.timeoutInSeconds = 5
UDPReader.port = 4211
UDPReader.StartDriver()
Debug.Log("Driver started!")

for reading in range(30):
    time.sleep(1)
    pourcent = int((reading/30)*100)
    print(f"--------------------- [{pourcent}%]")
    SendAPlaneOnUDP(PlaneIDs.universalInfo)
    while True:
        receivedMessage = UDPReader.GetOldestMessage()
        if(receivedMessage == None):
            break
        for sender,message in receivedMessage.items():
            Debug.Log(f"New plane from {sender}:")
            arrival = MakeAPlaneOutOfArrivedBytes(message)

            if(arrival == Execution.Failed):
                print("Failed to generate a plane.")

            if(arrival == Execution.Crashed):
                print("Crashed when making the plane?")

            if (arrival.passedTSA):
                Debug.Log(">>> Plane passed TSA")

UDPReader.StopDriver()
Debug.End()