import os
import time
import subprocess
import socket
import inspect
import binascii
import wifi

def Print(message):
    frame = inspect.currentframe().f_back
    line = frame.f_lineno
    print(f"[{line}]\t{message}")

# ======================================================================
# ======================================================================
# ======================================================================
#region ---------------------------------------------------------------- WiFi
def Search():
    wifilist = []

    cells = wifi.Cell.all('wlan0')

    for cell in cells:
        wifilist.append(cell)
    Print(f">>>>>> WiFi list created.")
    return wifilist

def FindFromSearchList(ssid):
    wifilist = Search()

    for cell in wifilist:
        if cell.ssid == ssid:
            Print(f">>>>>> {ssid} found in search list")
            return cell
    Print(f">>>>>> {ssid} not found in search list: {wifilist}")
    return False

def FindFromSavedList(ssid):
    cell = wifi.Scheme.find('wlan0', ssid)

    if cell:
        Print(">>>>>> WiFi found in saved wifis")
        return cell
    Print(">>>>>> FindFromSavedList failed")
    return False

def Connect(ssid, password=None):
    cell = FindFromSearchList(ssid)

    if cell:
        savedcell = FindFromSavedList(cell.ssid)

        # Already Saved from Setting
        if savedcell:
            savedcell.activate()
            Print(f">>>>>> WiFi cell activated")
            return cell

        # First time to connect
        else:
            if cell.encrypted:
                if password:
                    scheme = Add(cell, password)

                    try:
                        scheme.activate()
                        Print(f">>>>>> WiFi scheme activated")

                    # Wrong Password
                    except wifi.exceptions.ConnectionError:
                        Print(f">>>>>> Connection error occured. {password} isn't valid for {ssid}?")
                        Delete(ssid)
                        return False

                    return cell
                else:
                    Print(f">>>>>> No password required")
                    return False
            else:
                scheme = Add(cell)

                try:
                    scheme.activate()
                    Print(f">>>>>> WiFi scheme activated")
                except wifi.exceptions.ConnectionError:
                    Print(f">>>>>> Connection error occured")
                    Delete(ssid)
                    return False

                return cell
    Print(f">>>>>> Connect failed")
    return False

def Add(cell, password=None):
    if not cell:
        Print(f">>>>>> Add failed")
        return False

    scheme = wifi.Scheme.for_cell('wlan0', cell.ssid, cell, password)
    scheme.save()
    Print(f">>>>>> scheme returned")
    return scheme

def Delete(ssid):
    if not ssid:
        Print(f">>>>>> {ssid} not deleted")
        return False

    cell = FindFromSavedList(ssid)

    if cell:
        cell.delete()
        Print(f">>>>>> {ssid} deleted")
        return True

    Print(f">>>>>> {ssid} not deleted")
    return False

def ConnectToIt(ssid:str, password:str):
    Print(f">>> Trying to connect to {ssid} using password {password}...")
    result = Connect(ssid, password)
    Print(f">>> Function returned {result}")
#endregion
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
