import threading
import asyncio
from Libraries.BRS_Python_Libraries.BRS.Utilities.Enums import Execution
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Network.WiFi.WiFi import CanDeviceUseWiFi, GetWiFiNetworks

        # result = CanDeviceUseWiFi()

        # result = True
        # networks = [
            # {
                # "ssid" : "wifi_name",
                # "strength" : 50,
                # "bssid" : "c0:3c:04:2a:62:ec",
                # "mode" : None,
            # },
            # {
                # "ssid" : "Batiscan",
                # "strength" : 100,
                # "bssid" : "aa:bb:cc:dd:ee:ff",
                # "mode" : None,
            # }
        # ]

        # if(result != True):
            # Debug.Log("WiFi networks cannot be accessed.")
            # anim = Animation(pos_hint = {"center_x":0.5, "center_y":0.45}, t="in_out_back")
            # anim.start(self.NoWiFiCard)
            # KontrolRGB.DisplayMinorProblem()
        # else:
            # Debug.Log("Wifi can be accessed")
            # Debug.Log("Getting WiFi networks")
            # networks = GetWiFiNetworks()

            # Debug.Log("Configurating WiFiLogin Screens.")
            # WiFiLogin_Screens.SetBadExiter(NetworkMenu_Screens, "NetworkMenu")
            # WiFiLogin_Screens.SetGoodExiter(NetworkMenu_Screens, "NetworkMenu")
# 
            # if(networks == Execution.Failed):
                # Debug.Error("Fatal error when getting available networks.")
                # Debug.Log("WiFi networks cannot be accessed.")
                # anim = Animation(pos_hint = {"center_x":0.5, "center_y":0.45}, t="in_out_back")
                # anim.start(self.NoWiFiCard)
                # KontrolRGB.DisplayUserError()
                # Debug.End()
                # return

            # if(networks == Execution.Crashed):
                # Debug.Error("Fatal error when getting available networks.")
                # Debug.Log("WiFi networks cannot be accessed.")
                # anim = Animation(pos_hint = {"center_x":0.5, "center_y":0.45}, t="in_out_back")
                # anim.start(self.NoWiFiCard)
                # KontrolRGB.DisplayUserError()
                # Debug.End()
                # return

            # if(networks == Execution.Incompatibility):
                # Debug.Error("Fatal error when getting available networks.")
                # Debug.Log("WiFi networks cannot be accessed.")
                # anim = Animation(pos_hint = {"center_x":0.5, "center_y":0.45}, t="in_out_back")
                # anim.start(self.NoWiFiCard)
                # KontrolRGB.DisplayUserError()
                # Debug.End()
                # return

            # Debug.Log("Creating WiFi network cards.")
            # for network in networks:
                # WiFiCard = WiFiSelectionCard(network)
                # WiFiCard.PressedEnd = self.GoToWiFiConnectionScreen
                # self.cardBox.add_widget(WiFiCard)


import time
print("\n\n\n\n")
print(">>> START")
AsyncGetNearbyNetworks(WiFiProgress)
print(">>> END")
time.sleep(5)
print(f"Result = {WiFiProgress.status}")
print("\n\n\n\n")



# from kivy.lang import Builder

# from kivymd.app import MDApp
# from kivymd.uix.behaviors import TouchBehavior
# from kivymd.uix.button import MDRaisedButton

# KV = '''
# Screen:

#     MyButton:
#         text: "PRESS ME"
#         pos_hint: {"center_x": .5, "center_y": .5}
# '''

# class MyButton(MDRaisedButton, TouchBehavior):
#     def on_long_touch(self, *args):
#         print("<on_long_touch> event")

#     def on_double_tap(self, *args):
#         print("<on_double_tap> event")

#     def on_triple_tap(self, *args):
#         print("<on_triple_tap> event")

#     def on_release(self, *args):
#         print("<on_release> event")

#     def on_release(self, *args):
#         print("<on_release> event")

#     def on_press(self, *args):
#         print("<on_press> event")
#         from Local.Drivers.Batiscan.Programs.Communications.UDP import BatiscanUDP
#         BatiscanUDP._NoConnection()

# class MainApp(MDApp):
#     def build(self):
#         return Builder.load_string(KV)


# MainApp().run()