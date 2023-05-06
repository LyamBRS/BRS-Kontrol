from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from Libraries.BRS_Python_Libraries.BRS.Utilities import Information
Debug.enableConsole = True
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from Libraries.BRS_Python_Libraries.BRS.Network.WiFi.WiFi import GetNetworkInterfaces
from Libraries.BRS_Python_Libraries.BRS.GUI.Status.WiFi import WiFiSelectionCard
from Programs.Pages.NetworkMenu import NetworkMenu, NetworkMenu_Screens


wifiDictionary = {
    "ssid" : "wifi_name",
    "strength" : 50,
    "bssid" : "c0:3c:04:2a:62:ec",
    "mode" : None,
}

interfaces = GetNetworkInterfaces()

Debug.Log(interfaces)

class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"

        screen = NetworkMenu_Screens.Call()

        return screen


Example().run()