from Programs.Local.Loading.BrSpand import InstallCardsDrivers, Debug

import time
import socket

from Libraries.BRS_Python_Libraries.BRS.Network.UDP.sender import UDPSender
from Libraries.BRS_Python_Libraries.BRS.Network.UDP.receiver import UDPReader
from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import Plane, Passenger, BFIO, PrintPlane
from Programs.Local.BFIO.kontrolBFIO import GetUniversalInfoPlane

UDPReader.port = 4211
UDPSender.port = 4210
UDPSender.ipAddress = "192.168.4.2"

result = UDPSender.StartDriver()
result = UDPReader.StartDriver()

time.sleep(2.5)
plane:Plane = GetUniversalInfoPlane()
listToSend = []
for passenger in plane.passengers:
    listToSend.append(passenger.value_8bits[0])
    listToSend.append(passenger.value_8bits[1])

UDPSender.SendThing(listToSend)
print("Sent an universal info plane?")
time.sleep(2.5)

readThingy = UDPReader.GetOldestMessage()
print(f"Received message: {readThingy}")
passenengers = BFIO.GetPassengersFromDualBytes(readThingy)
plane = BFIO.ParsePassengersIntoMandatoryPlane(passenengers)

Debug.enableConsole = True
PrintPlane(plane)
Debug.enableConsole = False

time.sleep(2.5)
print("Close UDP")

result = UDPReader.StopDriver()
result = UDPSender.StopDriver()
















# url = "https://github.com/LyamBRS/BrSpand_GamePad.git"
# name = "GamePad"
# 
# print(f"Trying to clone {url}.")
# print(f"Trying to rename it to {name}")
# 
# Debug.enableConsole = True
# InstallCardsDrivers("GamePad", url)













# from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import Plane, VarTypes, Passenger


# data = [
    # 4206969,                                     # unique device ID
    # 1,                                              # BFIO version
    # 0,                                              # Device type
    # 1,                                              # Device status
    # "https://github.com/LyamBRS/BrSpand_GamePad.git",   # Git repository of the device.
    # "GamePad",
    # "Rev A"
# ]

# vartypes = [VarTypes.Unsigned.LongLong, VarTypes.Unsigned.LongLong, VarTypes.Unsigned.Char, VarTypes.Unsigned.Char, VarTypes.String, VarTypes.String, VarTypes.String]

# universalInfo = Plane(7, data, vartypes)

# for passenger in universalInfo.passengers:
    # print(passenger.value_8bits[0])
    # print(",")
    # print(passenger.value_8bits[1])
    # print(",")








# import time
# from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
# from Libraries.BRS_Python_Libraries.BRS.Hardware.GPIO.driver import GPIO
# from Local.Hardware.LeftBrSpand.driver import LeftBrSpand
# from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
# Debug.enableConsole = True
# 
# 
# Debug.Start("Testing")
# 
# Debug.Log("Staring GPIO")
# result = GPIO.StartDriver()
# if(result != Execution.Passed):
    # Debug.Error("FAILED TO START THE DRIVER")
# else:
    # result = LeftBrSpand.Launch()
    # if(result != Execution.Passed):
        # Debug.Error("FAILED TO START THE DRIVER")
    # else:
        # for i in range(30):
            # try:
                # listOfGPIOs = GPIO.GetList()
            # except:
                # Debug.Error("Fuck up!")
            # Debug.Log(i)
            # LeftBrSpand.PeriodicCallback()
            # time.sleep(1)
# 
# LeftBrSpand.Stop()
# GPIO.StopDriver()
# Debug.End()














# from Libraries.BRS_Python_Libraries.BRS.Utilities.bfio import Plane, PrintPlane, NewArrival
# from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
# from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import VarTypes
# Debug.enableConsole = True
# 
# classes = [
    # VarTypes.Bool,
    # VarTypes.String,
    # VarTypes.Float,
    # VarTypes.Int
# ]
# 
# variables = [
    # True,
    # "Among us",
    # 0.123456789,
    # 4096
# ]
# 
# plane = Plane(128, variables=variables, wantedClasses=classes)
# 
# PrintPlane(plane)
# 
# print("\n\n\n")
# 
# arrivedPlane = NewArrival(plane.passengers, classes)
# PrintPlane(arrivedPlane)

# from kivy.uix.boxlayout import BoxLayout
# from kivymd.app import MDApp
# from kivymd.uix.toolbar import MDTopAppBar
# from kivymd.uix.button import MDIconButton
# from kivymd.uix.gridlayout import MDGridLayout
# 
# from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
# from kivy.uix.boxlayout import BoxLayout
# from kivymd.app import MDApp
# from kivymd.uix.toolbar import MDTopAppBar
# from kivymd.uix.button import MDIconButton
# from kivymd.uix.label import MDLabel
# from kivy.uix.anchorlayout import AnchorLayout
# from kivymd.uix.card import MDCard
# 
# from Libraries.BRS_Python_Libraries.BRS.GUI.Utilities.references import Shadow, Rounding
# 
# 
# class NavigationButton(MDIconButton):
    # def __init__(self, **kwargs):
        # super(NavigationButton, self).__init__(**kwargs)
        # self.name = "Quit"
        # self.text = "Quit"
        # self.icon = "android"
        # self.valign = "center"
        # self.halign = "center"
        # self.pos_hint = {"center_x":0.5, "center_y":0.5}
        # self.size_hint = (1,1)
        # self.icon_size = self.size[1]
# 
# class BottomButtons(MDCard):
#    def __init__(self, **kwargs):
        # super(BottomButtons, self).__init__(**kwargs)
        # self.shadow_softness = Shadow.Smoothness.default
        # self.elevation = Shadow.Elevation.default
        # self.shadow_radius = Shadow.Radius.default
        # self.radius = Rounding.default
        # self.add_widget(NavigationButton())
        # self.add_widget(NavigationButton())  
        # self.add_widget(NavigationButton())  
        # self.add_widget(NavigationButton())  
        # self.add_widget(NavigationButton())  
# 
# class Test(MDApp):
    # def build(self):
        # layout = BoxLayout(orientation="vertical", padding = 10)
        # layout.size_hint = (1,0.125)
# 
        # top_toolbar = BottomButtons()
# 
        # layout.add_widget(top_toolbar)
        # return layout


# Test().run()








# from kivy.lang import Builder
# 
# from kivymd.app import MDApp
# from kivymd.uix.button import MDFloatingActionButton
# 
# KV = '''
# MDScreen:
    # md_bg_color: "#f7f2fa"
# 
    # MDBoxLayout:
        # id: box
        # spacing: "56dp"
        # adaptive_size: True
        # pos_hint: {"center_x": .5, "center_y": .5}
# '''
# 
# 
# class Example(MDApp):
    # def build(self):
        # self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "Orange"
        # self.theme_cls.material_style = "M3"
        # return Builder.load_string(KV)
# 
    # def on_start(self):
        # data = {
            # "standard": {"md_bg_color": "#fefbff", "text_color": "#6851a5"},
            # "small": {"md_bg_color": "#e9dff7", "text_color": "#211c29"},
            # "large": {"md_bg_color": "#f8d7e3", "text_color": "#311021"},
        # }
        # for type_button in data.keys():
            # self.root.ids.box.add_widget(
                # MDFloatingActionButton(
                    # icon="pencil",
                    # type=type_button,
                    # theme_icon_color="Custom",
                    # md_bg_color=data[type_button]["md_bg_color"],
                    # icon_color=data[type_button]["text_color"],
                # )
            # )
# 
# 
# Example().run()

#fakeNetwork = """
#Interface name : Wi-Fi
#There are 5 networks currently visible.
#
#SSID 1 : BELL310
#    Network type            : Infrastructure
#    Authentication          : WPA2-Personal
#    Encryption              : CCMP
#    BSSID 1                 : 0c:ac:8a:00:d6:0d
#         Signal             : 33%
#         Radio type         : 802.11ax
#         Channel            : 6
#         Basic rates (Mbps) : 1 2 5.5 11
#         Other rates (Mbps) : 6 9 12 18 24 36 48 54
#
#SSID 2 :
#    Network type            : Infrastructure
#    Authentication          : WPA2-Enterprise
#    Encryption              : CCMP
#    BSSID 1                 : 10:33:bf:ba:8f:da
#         Signal             : 40%
#         Radio type         : 802.11ac
#         Channel            : 157
#         Basic rates (Mbps) : 6
#         Other rates (Mbps) : 9 12 18 24 36 48 54
#    BSSID 2                 : 94:6a:77:e6:74:19
#         Signal             : 40%
#         Radio type         : 802.11n
#         Channel            : 6
#         Basic rates (Mbps) : 6
#         Other rates (Mbps) : 9 12 18 24 36 48 54
#    BSSID 3                 : 10:33:bf:9f:94:4d
#         Signal             : 85%
#         Radio type         : 802.11n
#         Channel            : 6
#         Basic rates (Mbps) : 6
#         Other rates (Mbps) : 9 12 18 24 36 48 54
#    BSSID 4                 : 10:33:bf:9f:94:57
#         Signal             : 80%
#         Radio type         : 802.11ac
#         Channel            : 157
#         Basic rates (Mbps) : 6
#         Other rates (Mbps) : 9 12 18 24 36 48 54
#
#SSID 3 : BELL653
#    Network type            : Infrastructure
#    Authentication          : WPA2-Personal
#    Encryption              : CCMP
#    BSSID 1                 : c0:3c:04:2a:62:ec
#         Signal             : 78%
#         Radio type         : 802.11ax
#         Channel            : 6
#         Basic rates (Mbps) : 1 2 5.5 11
#         Other rates (Mbps) : 6 9 12 18 24 36 48 54
#"""
#import re
#Debug.enableConsole = True
#text = fakeNetwork # Replace with your text
#networks = []
#current_network = {}
#
#for line in text.split("\n"):
#    line = line.strip()
#    if line.startswith("SSID"):
#        current_network = {}
#        current_network["ssid"] = line.split(":")[1].strip()
#        var = current_network["ssid"]
#        Debug.Log(f"SSID = {var}")
#
#    elif line.startswith("Authentication"):
#        current_network["authentication"] = line.split(":")[1].strip()
#        var = current_network["authentication"]
#        Debug.Log(f"authentication = {var}")
#
#    elif line.startswith("Encryption"):
#        current_network["encryption"] = line.split(":")[1].strip()
#        var = current_network["authentication"]
#        Debug.Log(f"encryption = {var}")
#
#    elif line.startswith("Signal"):
#        signal = line.split(":")[1].strip()
#        current_network["signal"] = signal
#        Debug.Log(f"signal = {signal}")
#
#    elif line.startswith("BSSID"):
#        bssid = line.split(":")[1].strip()
#
#        dataList:list = line.split(" ")
#        cleanedList = [x for x in dataList if (x and len(x)>5)]
#        Debug.Log(f"BSSID: {cleanedList}")
#
#    elif line.startswith("Channel"):
#        current_network["channel"] = line.split(":")[1].strip()
#        networks.append(current_network)
#
#print(networks)
#
#
## def Netsh_GetWiFiNetworks() -> list:
#    # """
#        # Netsh_GetWiFiNetworks:
#        # ======================
#        # Summary:
#        # --------
#        # Allows you to get a cleaned list of netsh wlan networks output.
#        # This function allows you to see all the networks that are
#        # available wirelessly.
#
#        # This is especially useful if you want to check which WiFi
#        # your WINDOWS device can access
#
#        # `Attention`:
#        # ------------
#        # Netsh commands only works on WINDOWS DEVICES. They
#        # do not work on Linux nor MacOS devices.
#
#        # Returns:
#        # ----------
#        # - `Execution.Incompatibility`: The function cannot be used due to your device's operating system.
#        # - `Execution.Failed`: Failed to run the command. wlan is not accessible.
#
#        # Examples of returned lists:
#        # -----------------------------
#    # """
#    # Debug.Start("Netsh_GetWiFiNetworks")
#
#    # if(Information.initialized):
#        # if(Information.platform != "Windows"):
#            # Debug.Error(f"Attempting to call a netsh function on a non windows based OS: {Information.OS}")
#            # Debug.End()
#            # return Execution.Incompatibility
#        # else:
#            # Debug.Log("Windows platform detected.")
#    # else:
#        # Debug.Warn("Warning, BRS's Information class is not initialized. This function cannot execute safety measures.")
#
#    # try:
#        # networks = subprocess.check_output(["netsh", "wlan", "show", "networks", "mode=bssid"])
#        # decodedNetworks = networks.decode("ascii")
#        # Debug.Log("Subprocess success")
#    # except:
#        # Debug.Error("Fatal error while running subprocess. You're either not using Windows or don't have any WiFi drivers.")
#        # Debug.End()
#        # return Execution.Crashed
#    
#
#
## if __name__ == "__main__":
##     Debug.enableConsole = True
##     print(Netsh_GetWiFiNetworks())
#
