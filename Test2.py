from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Hardware.Neopixel.driver import RGBModes
from Libraries.BRS_Python_Libraries.BRS.Hardware.Neopixel.rgbDriverHandler import RGB

import time
Debug.enableConsole = False
RGB.StartDriver()

Debug.Log("Test2.py -> Waiting 1 seconds...")
time.sleep(1)

print("\n######################################################")
print("TESTING: 10s: Static, B=(255,0,0), R=(0,255,0), S=(0,0,255)")
print("######################################################")
RGB.SetAttributes(colors=[[255,0,0], [0,255,0], [0,0,255]], rgbMode = RGBModes.static)
time.sleep(10)

print("\n######################################################")
print("TESTING: 3s: Static, colors = (255,255,255)")
print("######################################################")
RGB.SetAttributes(colors=[255,255,255], rgbMode = RGBModes.static)
time.sleep(3)

print("\n######################################################")
print("TESTING: 3s: Pulse, B=(50,50,50), R=(0,0,0), S=(0,0,0)")
print("######################################################")
RGB.SetAttributes(colors=[[50,50,50], [0,0,0], [0,0,0]], rgbMode = RGBModes.pulse)
time.sleep(3)

print("\n######################################################")
print("TESTING: 3s: Pulse, B=(50,50,50), R=(50,50,50), S=(0,0,0)")
print("######################################################")
RGB.SetAttributes(colors=[[50,50,50], [50,50,50], [0,0,0]])
time.sleep(3)

print("\n######################################################")
print("TESTING: 6s: Pulse, B=(50,50,50), R=(50,50,50), S=(50,50,50)")
print("######################################################")
RGB.SetAttributes(colors=[[50,50,50], [50,50,50], [50,50,50]])
time.sleep(6)

print("\n######################################################")
print("TESTING: 5s: Cycling, colors = (255,255,255)")
print("######################################################")
RGB.SetAttributes(colors=[255,255,255], rgbMode = RGBModes.cycling)
time.sleep(5)

print("\n######################################################")
print("TESTING: 5s: Cycling, B=(50,0,0), R=(0,50,0), S=(0,0,50)")
print("######################################################")
RGB.SetAttributes(colors=[[50,0,0], [0,50,0], [0,0,50]], rgbMode = RGBModes.cycling)
time.sleep(5)

print("\n######################################################")
print("TESTING: 5s: Loading, B=(50,0,50), R=(50,50,0), S=(0,50,50)")
print("######################################################")
RGB.SetAttributes(colors=[[50,0,50], [50,50,0], [0,50,50]], rgbMode= RGBModes.loading)
time.sleep(5)

print("\n######################################################")
print("TESTING: ENDING")
print("######################################################")
RGB.StopDriver()
time.sleep(2)
print("\n######################################################")
print("TESTING: ENDED")
print("######################################################")




# import os
# import ast

# directory = os.getcwd()
# used_libraries = set()

# def check_file_for_libraries(file_path):
#     with open(file_path, "r") as file:
#         tree = ast.parse(file.read())

#     for node in ast.walk(tree):
#         if isinstance(node, ast.Import):
#             for name in node.names:
#                 if name.name == "git":
#                     used_libraries.add("gitpython")
#                 if name.name == "github":
#                     used_libraries.add("PyGitHub")

# # Recursive iteration through files in the directory
# for root, _, files in os.walk(directory):
#     for file_name in files:
#         print(f"CHECKING >>> {file_name}")
#         if file_name.endswith(".py"):  # Process only Python files
#             file_path = os.path.join(root, file_name)
#             check_file_for_libraries(file_path)

# print("\n")
# print(used_libraries)













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
