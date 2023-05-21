from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from Programs.Local.GUI.Navigation import AppNavigationBar
from Libraries.BRS_Python_Libraries.BRS.Network.WiFi.WiFi import WiFiStatusUpdater
from Libraries.BRS_Python_Libraries.BRS.Utilities.pythonKiller import KillPython
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
Debug.enableConsole = True

class MainApp(MDApp):
    def build(self):
        WiFiStatusUpdater.StartUpdating()
        layout = BoxLayout(orientation='vertical')

        # Create the toolbar
        toolbar = AppNavigationBar("Test")

        # Add the toolbar to the layout
        layout.add_widget(toolbar.ToolBar)

        return layout

    def menu_button_pressed(self, instance):
        print("Menu button pressed!")


if __name__ == "__main__":
    MainApp().run()
    WiFiStatusUpdater.StopUpdating()
    KillPython()
KillPython()



























# from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
# Debug.enableConsole = True
# from Libraries.BRS_Python_Libraries.BRS.Network.WiFi.WiFi import Linux_ConnectWiFi, Linux_VerifyInternetConnection
# import time

# Debug.Log("Starting thread... Trying to connect to Batiscan...")
# Linux_ConnectWiFi.StartConnecting("Batiscan", "BATISCAN")

# for currentAttempt in range(60):
#     result = Linux_ConnectWiFi.GetConnectionStatus()
#     connected = result[0]
#     timeTaken = result[2]
#     networkConnected = result[3]
#     # Debug.Log(f"{currentAttempt}: {result}")

#     if(Linux_ConnectWiFi.connected or connected or networkConnected=="Batiscan"):
#         Debug.Log(f"It took {timeTaken} seconds to connect to {networkConnected}")
#         break
#     print(currentAttempt)
#     time.sleep(1)
# Linux_ConnectWiFi.StopConnecting()

# Debug.Log("Starting thread... Trying to connect to the internet.")
# Linux_VerifyInternetConnection.StartPinging()
# for currentAttempt in range(10):
#     result = Linux_VerifyInternetConnection.GetConnectionStatus()
#     connected = result[0]
#     timeTaken = result[2]

#     if(Linux_VerifyInternetConnection.hasInternet or connected):
#         Debug.Log(f"It took {timeTaken} seconds to connect to the internet.")
#         break
#     print(currentAttempt)
#     time.sleep(1)
# Linux_VerifyInternetConnection.StopPinging()

# time.sleep(5)

# Debug.Log("Starting thread... Trying to connect to Andromeda...")
# Linux_ConnectWiFi.StartConnecting("Andromeda", "pianoarmoirefeuillewhisky5G")

# for currentAttempt in range(60):
#     result = Linux_ConnectWiFi.GetConnectionStatus()
#     connected = result[0]
#     timeTaken = result[2]
#     networkConnected = result[3]
#     # Debug.Log(f"{currentAttempt}: {result}")

#     if(Linux_ConnectWiFi.connected or connected or networkConnected=="Andromeda"):
#         Debug.Log(f"It took {timeTaken} seconds to connect to {networkConnected}")
#         break
#     print(currentAttempt)
#     time.sleep(1)
# Linux_ConnectWiFi.StopConnecting()

# Debug.Log("Starting thread... Trying to connect to the internet.")
# Linux_VerifyInternetConnection.StartPinging()
# for currentAttempt in range(10):
#     result = Linux_VerifyInternetConnection.GetConnectionStatus()
#     connected = result[0]
#     timeTaken = result[2]

#     if(Linux_VerifyInternetConnection.hasInternet or connected):
#         Debug.Log(f"It took {timeTaken} seconds to connect to the internet.")
#         break
#     print(currentAttempt)
#     time.sleep(1)
# Linux_VerifyInternetConnection.StopPinging()

# import threading
# import time

# class CounterThread:

#     thread = None
#     stop_event = threading.Event()

#     def _counter_thread():
#         counter = 0
#         while counter <= 25:
#             if CounterThread.stop_event.is_set():
#                 break
#             print("Counter:", counter)
#             counter += 1
#             time.sleep(0.5)

#     def start():
#         if not CounterThread.thread or not CounterThread.thread.is_alive():
#             CounterThread.stop_event.clear()
#             CounterThread.thread = threading.Thread(target=CounterThread._counter_thread)
#             CounterThread.thread.start()

#     def stop():
#         CounterThread.stop_event.set()
#         if CounterThread.thread and CounterThread.thread.is_alive():
#             CounterThread.thread.join()

# Example usage:
# CounterThread.start()
# print("Application can still execute stuff!")
# Main application continues executing while the counter thread runs

# Perform other tasks in the main application
# time.sleep(1)
# print("Yup this works")
# time.sleep(2)

# Stop the counter thread
# CounterThread.stop()

# Continue with other tasks in the main application
# time.sleep(1)
# print("Application continues executing.")



























# import module
# import os
# 
# name = ""
# 
# function to establish a new connection
# def createNewConnection(name, SSID, password):
    # config = f"""<?xml version=\"1.0\"?>
# <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    # <name>{name}</name>
    # <SSIDConfig>
        # <SSID>
            # <name>{SSID}</name>
        # </SSID>
    # </SSIDConfig>
    # <connectionType>ESS</connectionType>
    # <connectionMode>auto</connectionMode>
    # <MSM>
        # <security>
            # <authEncryption>
                # <authentication>WPA2PSK</authentication>
                # <encryption>AES</encryption>
                # <useOneX>false</useOneX>
            # </authEncryption>
            # <sharedKey>
                # <keyType>passPhrase</keyType>
                # <protected>false</protected>
                # <keyMaterial>{password}</keyMaterial>
            # </sharedKey>
        # </security>
    # </MSM>
# </WLANProfile>"""
# 
    # print(">>> >>> Config: ")
    # print(f">>> >>> {config}")
    # print(">>> >>>  Command: ")
    # command = f"netsh wlan add profile filename=\""+name+".xml\""+" interface=\"Wi-Fi\""
    # print(command)
    # with open(name+".xml", 'w') as file:
        # print(">>> >>> WRITING CONFIG IN XML")
        # file.write(config)
    # os.system(command)
# 
# function to connect to a network
# def connect(name, SSID):
    # print(">>> >>> Command:")
    # command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\""
    # print(f">>> >>> {command}")
    # os.system(command)
# 
# function to display avavilabe Wifi networks
# def displayAvailableNetworks():
    # print(">>> >>> displayAvailableNetworks: Command: ")
    # command = "netsh wlan show networks interface=\"Wi-Fi\""
    # print(f">>> >>> {command}")
    # os.system(command)
# 
# 
# display available netwroks
# print(">>> DISPLAYING AVAILABLE NETWORKS")
# displayAvailableNetworks()
# print(">>> DISPLAY FINISHED.")
# 
# input wifi name and password
# name = "Batiscan"
# password = "BATISCAN"
# 
# establish new connection
# print(">>> CREATING NEW CONNECTION...")
# createNewConnection(name, name, password)
# print(">>> CONNECTION CREATED")
# 
# connect to the wifi network
# print(">>> CONNECTING?")
# connect(name, name)
# print(">>> If you aren't connected to this network, try connecting with the correct password!")


























# from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
# from Libraries.BRS_Python_Libraries.BRS.Utilities import Information
# Debug.enableConsole = True
# from kivymd.app import MDApp
# from kivymd.uix.button import MDIconButton
# from kivymd.uix.screen import MDScreen
# from kivymd.uix.boxlayout import MDBoxLayout
# from Libraries.BRS_Python_Libraries.BRS.Network.WiFi.WiFi import GetNetworkInterfaces
# from Libraries.BRS_Python_Libraries.BRS.GUI.Status.WiFi import WiFiSelectionCard
# from Programs.Pages.NetworkMenu import NetworkMenu, NetworkMenu_Screens

# resultedList = []
# wifiDictionary = {
    # "ssid" : "wifi_name",
    # "strength" : 50,
    # "bssid" : "c0:3c:04:2a:62:ec",
    # "mode" : None,
# }

# resultedList.append(wifiDictionary)
# print(str(resultedList))

# wifiDictionary = {}

# wifiDictionary = {
    # "ssid" : "wifi_name",
    # "strength" : 50,
    # "bssid" : "c0:3c:04:2a:62:ec",
    # "mode" : None,
# }
# resultedList.append(wifiDictionary)
# print(str(resultedList))

# interfaces = GetNetworkInterfaces()

# Debug.Log(interfaces)

# class Example(MDApp):
    # def build(self):
        # self.theme_cls.theme_style = "Light"
        # self.theme_cls.primary_palette = "Orange"

        # screen = NetworkMenu_Screens.Call()

        # return screen


# Example().run()