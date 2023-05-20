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

def ConnectToIt(ssid, password):
    print(f"Creating config lines with {ssid} and {password}... Hoping nothing fucks up.")
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
    print(f"Changing permissions of wpa_supplicant.conf")
    os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")

    print(f"Turning off WiFi")
    os.popen("sudo ifconfig wlan0 down")

    #writing to file
    print(f"Writing new things in wpa_supplicant.conf")
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi:
        wifi.write(config)
        print("Success!")
        wifi.close()

    print("Wifi config added. Refreshing configs...")
    ## refresh configs
    os.popen("sudo wpa_cli -i wlan0 reconfigure")

    print(f"Turning on WiFi")
    os.popen("sudo ifconfig wlan0 up")

    print(f"Running whatever I found online for raspberry pi 3")
    os.popen("sudo dhclient -r wlan0")
    os.popen("sudo ifdown wlan0")
    os.popen("sudo ifup wlan0")
    os.popen("sudo dhclient -v wlan0")

if __name__ == '__main__':

    print(f"Current network: {GetCurrentSSID()}")
    time.sleep(2)
    # Connect WiFi with password & without password")
    print (f"Connecting to Batiscan...")
    ConnectToIt('Batiscan', 'BATISCAN')
    time.sleep(5)
    print(f"Current network: {GetCurrentSSID()}")
    time.sleep(2)

    print (f"Connecting to Andromeda...")
    ConnectToIt('Andromeda', 'pianofeuillearmoirewhisky5G')
    time.sleep(5)
    print(f"Current network: {GetCurrentSSID()}")