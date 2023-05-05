from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from Libraries.BRS_Python_Libraries.BRS.GUI.Status.WiFi import WiFiSelectionCard


wifiDictionary = {
    "ssid" : "wifi_name",
    "strength" : 50,
    "bssid" : "c0:3c:04:2a:62:ec",
    "mode" : None,
}



class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"

        screen = MDScreen()
        layout = MDBoxLayout(padding = 50, spacing=50)
        wifi = WiFiSelectionCard(wifiDictionary)
        wifi2 = WiFiSelectionCard(wifiDictionary)
        layout.orientation = "vertical"
        layout.add_widget(wifi)
        layout.add_widget(wifi2)
        screen.add_widget(layout)

        return screen


Example().run()