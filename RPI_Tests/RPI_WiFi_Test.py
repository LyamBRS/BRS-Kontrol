import os
import time
import subprocess
import socket
import inspect

def Print(message):
    frame = inspect.currentframe().f_back
    line = frame.f_lineno
    print(f"[{line}]\t{message}")

# ======================================================================
# ======================================================================
# ======================================================================
def ConnectToIt(ssid: str, password: str):
    try:
        # Turn off Wi-Fi
        Print(">>> Turning off WiFi")
        subprocess.check_output(['sudo', 'ifconfig', 'wlan0', 'down'])

        # Wait for Wi-Fi to turn off
        time.sleep(2)

        # Connect to the network
        Print(f">>> Connecting to {ssid} using password {password}")
        subprocess.check_output(['sudo', 'iwconfig', 'wlan0', 'essid', ssid, 'key', password])

        Print(f">>>>>> Successfully connected to {ssid}")
    except subprocess.CalledProcessError as e:
        Print(f">>>> Error occurred: {str(e.output)}")

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
            Print(f">>> Internet connection verified after {ping} pings.")
            return True
        else:
            Print(f">>> [{ping}/10] - Failed to reach google.com")
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
        Print(f">>> {message} was sent to {ip_address} on port {port}")
        return True
    except Exception as e:
        Print(f">>> An error occurred: {str(e)}")
        return False
# ======================================================================
def TurnOnBatiscanLight() -> bool:
    message = "1111111111111"
    ipAddress = "192.168.4.1"
    port = "4210"
    Print(f">>> Sending {message} to {ipAddress} on port {port}...")
    sent = SendUDPMessage(ipAddress, port, message)
    return sent
# ======================================================================
def TurnOffBatiscanLight() -> bool:
    message = "0000000000000"
    ipAddress = "192.168.4.1"
    port = "4210"
    Print(f">>> Sending {message} to {ipAddress} on port {port}...")
    sent = SendUDPMessage(ipAddress, port, message)
    return sent
# ======================================================================
# ======================================================================
# ======================================================================
# ======================================================================

Print("=====================================")
Print("START - START - START - START - START")
Print("=====================================")
###################################################################################################
currentNetwork = GetCurrentSSID()
Print(f"Your network is {currentNetwork}")
time.sleep(1)
###################################################################################################
ssid = "Batiscan"
password = "BATISCAN"
Print(f"Attempting to connect to {ssid} with {password} for its password")
ConnectToIt("Batiscan", "BATISCAN")
###################################################################################################
Print("Testing the internet connection of that WiFi...")
maybeConnected = "connected" if GetInternetConnection() == True else "not connected"
Print(f">>> You are {maybeConnected} to the internet.")
###################################################################################################
thisNetwork = GetCurrentSSID()
Print(f"Your network is now {thisNetwork}")
time.sleep(1)
###################################################################################################
Print(f"Attempting to send some messages to Batiscan...")

wantedLightState:bool = False
for messageNumber in range(20):
    wantedLightState = not wantedLightState
    Print(f"[{messageNumber}/20] - Sending {wantedLightState} to Batiscan.")

    if(wantedLightState == True):
        result = TurnOnBatiscanLight()
        if(not result):
            Print(f"Something failed during ON transmission! Stopping messages.")
            break
    else:
        result = TurnOffBatiscanLight()
        if(not result):
            Print(f"Something failed during OFF transmission! Stopping messages.")
            break
    time.sleep(1)
###################################################################################################
Print("\n\n")
currentNetwork = GetCurrentSSID()
Print(f"Your network is {currentNetwork}")
time.sleep(1)
###################################################################################################
ssid = "Andromeda"
password = "pianofeuillearmoirewhisky5G"
Print(f"Attempting to connect to {ssid} using password {password}")
result = ConnectToIt(ssid, password)
time.sleep(1)
###################################################################################################
currentNetwork = GetCurrentSSID()
Print(f"Your network is now {currentNetwork}")
time.sleep(1)
###################################################################################################
Print("Testing the internet connection of that WiFi...")
maybeConnected = "connected" if GetInternetConnection() == True else "not connected"
Print(f">>> You are {maybeConnected} to the internet.")
###################################################################################################
Print("=======================================")
Print("END - END - END - END - END - END - END")
Print("=======================================")
