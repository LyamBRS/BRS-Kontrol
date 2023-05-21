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
def WaitTillConnected(wantedSSID:str, maxConnectionAttempts:int = 10, delayBetweenAttempts:int = 2) -> bool:
    Print(f">>> Waiting until connected to {wantedSSID}. Max tries: {maxConnectionAttempts}")

    for currentAttempt in range(maxConnectionAttempts):
        currentNetwork = GetCurrentSSID()
        if(currentNetwork != wantedSSID):
            Print(f">>>>>> [{currentAttempt}/{maxConnectionAttempts}] - Current network is {currentNetwork} instead of {wantedSSID}")
        else:
            timeTaken = currentAttempt * delayBetweenAttempts
            Print(f">>>>>> After {currentAttempt} over a period of {timeTaken} seconds, {wantedSSID} is seen as connected.")
            return True
        time.sleep(delayBetweenAttempts)

    timeTaken = currentAttempt * delayBetweenAttempts
    print(f">>>>>> {wantedSSID} is not the current network after {maxConnectionAttempts} tries over a period of {timeTaken}")
    return False
# ======================================================================
def ConnectToIt(ssid, password, maxConnectionAttempts:int = 10, delayBetweenAttempts:int = 2):
    # print(f">>> Creating config lines with {ssid} and {password}... Hoping nothing fucks up.")
    config_lines = [
        'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
        'update_config=1',
        '\n',
        'network={',
        '\tssid="{}"'.format(ssid),
        '\tpsk="{}"'.format(password),
        '}'
        ]
    config = '\n'.join(config_lines)

    #give access and writing. may have to do this manually beforehand
    # print(f">>> Changing permissions of wpa_supplicant.conf")
    os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")

    # Print(f">>> Turning off WiFi")
    os.popen("sudo ifconfig wlan0 down")

    #writing to file
    # print(f">>> Writing new things in wpa_supplicant.conf")
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi:
        wifi.write(config)
        print("Success!")
        wifi.close()

    # print(f">>> Changing permissions of wpa_supplicant.conf")
    os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")

    # print(">>> Wifi config added. Refreshing configs...")
    ## refresh configs
    os.popen("sudo wpa_cli -i wlan0 reconfigure")

    # Print(f">>> Turning on WiFi")
    os.popen("sudo ifconfig wlan0 up")

    result = WaitTillConnected(ssid, maxConnectionAttempts=maxConnectionAttempts, delayBetweenAttempts=delayBetweenAttempts)
    return result
# ======================================================================
def EnableWiFi() -> bool:
    try:
        # Run the ping command
        subprocess.check_output(['sudo', 'nmcli', 'radio', 'wifi', 'on'])
        return True
    except subprocess.CalledProcessError:
        return False
# ======================================================================

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
connected = ConnectToIt('Batiscan', 'BATISCAN', maxConnectionAttempts=20)
###################################################################################################
Print("Testing the internet connection of that WiFi...")
maybeConnected = "connected" if GetInternetConnection() == True else "not connected"
Print(f">>> You are {maybeConnected} to the internet.")
###################################################################################################
thisNetwork = GetCurrentSSID()
Print(f"Your network is now {thisNetwork}")
time.sleep(1)
print("\n")
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
password = "pianoarmoirefeuillewhisky5G"
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
