import os
import time
import subprocess
import socket
# ======================================================================
# ======================================================================
# ======================================================================
def ConnectToIt(ssid:str, password:str):
    result = os.system('iwconfig ' + "wlan0" + ' essid ' + ssid + ' key ' + password)
    print(f">>> command ran with return code {result}")
# ======================================================================
def GetCurrentSSID() -> str:
    try:
        # Run the iwgetid command and capture the output
        output = subprocess.check_output(['iwgetid', '-r']).decode('utf-8').strip()
        return output
    except subprocess.CalledProcessError:
        return None
# ======================================================================
def TestInternetConnection() -> bool:
    try:
        # Run the ping command
        subprocess.check_output(['ping', '-c', '1', 'google.com'])
        return True
    except subprocess.CalledProcessError:
        return False
# ======================================================================
def GetInternetConnection() -> bool:
    for ping in range(10):
        time.sleep(1)
        connected = TestInternetConnection()
        if(connected):
            print(f">>> Internet connection verified after {ping} pings.")
            return True
        else:
            print(f">>> [{ping}/10] - Failed to reach google.com")
    return False
# ======================================================================
def SendUDPMessage(ip_address, port, message:str):
    try:
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Send the message
        sock.sendto(message.encode('utf-8'), (ip_address, port))

        # Close the socket
        sock.close()
        print(f">>> {message} was sent to {ip_address} on port {port}")
        return True
    except Exception as e:
        print(">>> Error occurred:", str(e))
        return False
# ======================================================================
def TurnOnBatiscanLight() -> bool:
    message = "1111111111111"
    ipAddress = "192.168.4.1"
    port = "4210"
    print(f">>> Sending {message} to {ipAddress} on port {port}...")
    sent = SendUDPMessage(ipAddress, port, message)
    return sent
# ======================================================================
def TurnOffBatiscanLight() -> bool:
    message = "0000000000000"
    ipAddress = "192.168.4.1"
    port = "4210"
    print(f">>> Sending {message} to {ipAddress} on port {port}...")
    sent = SendUDPMessage(ipAddress, port, message)
    return sent
# ======================================================================
# ======================================================================
# ======================================================================
# ======================================================================

print("=====================================")
print("START - START - START - START - START")
print("=====================================")
###################################################################################################
currentNetwork = GetCurrentSSID()
print(f"Your network is {currentNetwork}")
time.sleep(1)
###################################################################################################
ssid = "Batiscan"
password = "BATISCAN"
print(f"Attempting to connect to {ssid} with {password} for its password")
ConnectToIt("Batiscan", "BATISCAN")
###################################################################################################
print("Testing the internet connection of that WiFi...")
maybeConnected = "connected" if GetInternetConnection() == True else "not connected"
print(f">>> You are {maybeConnected} to the internet.")
###################################################################################################
thisNetwork = GetCurrentSSID()
print(f"Your network is now {thisNetwork}")
time.sleep(1)
###################################################################################################
print(f"Attempting to send some messages to Batiscan...")

wantedLightState:bool = False
for messageNumber in range(20):
    wantedLightState = not wantedLightState
    print(f"[{messageNumber}/20] - Sending {wantedLightState} to Batiscan.")

    if(wantedLightState == True):
        result = TurnOnBatiscanLight()
        if(not result):
            print(f"Something failed during ON transmission! Stopping messages.")
            break
    else:
        result = TurnOffBatiscanLight()
        if(not result):
            print(f"Something failed during OFF transmission! Stopping messages.")
            break
    time.sleep(1)
###################################################################################################
print("\n\n")
currentNetwork = GetCurrentSSID()
print(f"Your network is {currentNetwork}")
time.sleep(1)
###################################################################################################
ssid = "Andromeda"
password = "pianofeuillearmoirewhisky5G"
print(f"Attempting to connect to {ssid} using password {password}")
result = ConnectToIt(ssid, password)
time.sleep(1)
###################################################################################################
currentNetwork = GetCurrentSSID()
print(f"Your network is now {currentNetwork}")
time.sleep(1)
###################################################################################################
print("Testing the internet connection of that WiFi...")
maybeConnected = "connected" if GetInternetConnection() == True else "not connected"
print(f">>> You are {maybeConnected} to the internet.")
###################################################################################################
print("=======================================")
print("END - END - END - END - END - END - END")
print("=======================================")
