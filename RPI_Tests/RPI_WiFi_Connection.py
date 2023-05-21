# -*- coding: utf-8 -*-

import subprocess
import time
import os

def GetCurrentSSID() -> str:
    try:
        # Run the iwgetid command and capture the output
        output = subprocess.check_output(['iwgetid', '-r']).decode('utf-8').strip()
        return output
    except subprocess.CalledProcessError:
        return None

def WaitTillConnected(wantedSSID:str, maxConnectionAttempts:int = 10, delayBetweenAttemps:int = 2) -> bool:
    print(f"Waiting until connected to {wantedSSID}. Max tries: {maxConnectionAttempts}")

    for currentAttempt in range(maxConnectionAttempts):
        time.sleep(delayBetweenAttemps)
        currentNetwork = GetCurrentSSID()
        if(currentNetwork != wantedSSID):
            print(f"[{currentAttempt/maxConnectionAttempts}] - Current network is {currentNetwork} instead of {wantedSSID}...")
        else:
            timeTaken = currentAttempt * delayBetweenAttemps
            print(f"after {currentAttempt} over a period of {timeTaken} seconds, {wantedSSID} is seen as connected.")

    timeTaken = currentAttempt * delayBetweenAttemps
    print(f"{wantedSSID} is not the current network after {maxConnectionAttempts} tries over a period of {timeTaken}")

def ConnectToIt(ssid, password):
    print(f">>> Creating config lines with {ssid} and {password}... Hoping nothing fucks up.")
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
    print(f">>> Changing permissions of wpa_supplicant.conf")
    os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")

    print(f">>> Turning off WiFi")
    os.popen("sudo ifconfig wlan0 down")

    #writing to file
    print(f">>> Writing new things in wpa_supplicant.conf")
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi:
        wifi.write(config)
        print("Success!")
        wifi.close()

    print(">>> Wifi config added. Refreshing configs...")
    ## refresh configs
    os.popen("sudo wpa_cli -i wlan0 reconfigure")

    print(f">>> Turning on WiFi")
    os.popen("sudo ifconfig wlan0 up")

if __name__ == '__main__':

    print(f"Current network: {GetCurrentSSID()}")
    time.sleep(5)
    # Connect WiFi with password & without password")
    print (f"Connecting to Batiscan...")
    ConnectToIt('Batiscan', 'BATISCAN')
    time.sleep(1)

    print("\n")
    result = WaitTillConnected("Batiscan", 10, 2)
    time.sleep(5)
    print(f"Current network: {GetCurrentSSID()}")
    time.sleep(5)

    print (f"Connecting to Andromeda...")
    ConnectToIt('Andromeda', 'pianoarmoirefeuillewhisky5G')
    time.sleep(5)
    
    print("\n")
    result = WaitTillConnected("Batiscan", 10, 2)
    time.sleep(5)
    print(f"Current network: {GetCurrentSSID()}")
    time.sleep(5)