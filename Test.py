from kivymd.icon_definitions import md_icons
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

class MyApp(MDApp):
    def build(self):
        self.icon = md_icons['account-plus-outline']
        self.icon2 = md_icons['account-outline']

        return MDLabel(text=self.icon2, font_style='Icon')

if __name__ == '__main__':
    MyApp().run()