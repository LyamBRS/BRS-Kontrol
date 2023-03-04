DefaultIconBannedWords = {
    "abjad",
    "application",
    "access",
    "align",
    "alert",
    "alphabet",
    "archive",
    "arrow",
    "arrange",
    "axis",
    "border",
    "battery",
    "lock",
    "progress",
    "chat",
    "form",
    "crop",
    "cursor",
    "drag",
    "outline",
    "chevron",
    "chart",
    "cancel",
    "calendar",
    "circle",
    "cog",
    "edit",
    "off",
    "remove",
    "settings",
    "plus",
    "minus",
    "book",
    "check",
    "clock",
    "box",
    "search",
    "comment",
    "refresh",
    "decimal",
    "delete",
    "sync",
    "marker",
    "distribute",
    "dock",
    "download",
    "flip",
    "folder",
    "format",
    "gesture",
    "menu",
    "message",
    "strength",
    "order",
    "page",
    "pan",
    "relation",
    "rewind",
    "rotate",
    "selection",
    "signal",
    "sort",
    "select",
    "step",
    "surround",
    "view",
    "source",
    "text",
    "call",
    "unfold",
    "vector",
    "share",
    "filter",
    "block",
}
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.icon_definitions import md_icons
from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem

Debug.enableConsole = True
Debug.Start("Application")
Debug.Log("Builder loading KV lang string")
Builder.load_string(
    '''
#:import images_path kivymd.images_path


<CustomOneLineIconListItem>

    IconLeftWidget:
        icon: root.icon


<PreviousMDIcons>

    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(20)

        MDBoxLayout:
            adaptive_height: True

            MDIconButton:
                icon: 'magnify'

            MDTextField:
                id: search_field
                hint_text: 'Search icon'
                on_text: root.set_list_md_icons(self.text, True)

        RecycleView:
            id: rv
            bar_width: 10
            bar_height: 100
            key_viewclass: 'viewclass'
            key_size: 'height'

            RecycleBoxLayout:
                padding: dp(10)
                default_size: None, dp(48)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
'''
)
Debug.Log("Building done.")

class CustomOneLineIconListItem(OneLineIconListItem):
    Debug.Start("CustomOneLineIconListItem")
    icon = StringProperty()
    Debug.End()

class PreviousMDIcons(Screen):
    Debug.Start("PreviousMDIcons")

    def set_list_md_icons(self, text="", search=False):
        '''Builds a list of icons for the screen MDIcons.'''
        Debug.Start("set_list_md_icons")

        def add_icon_item(name_icon):
            Debug.Start("add_icon_item")
            name_icon_list = name_icon.split("-")

            banned_word_detected = False
            for word in name_icon_list:
                for banned in DefaultIconBannedWords:
                    if word==banned:
                        banned_word_detected = True
                        Debug.Warn("BANNED")
                        break

            self.ids.rv.data.append(
                {
                    "viewclass": "CustomOneLineIconListItem",
                    "icon": name_icon,
                    "text": name_icon,
                    "callback": lambda x: x,
                }
            )
            Debug.End()

        self.ids.rv.data = []
        for name_icon in md_icons.keys():
            if search:
                if text in name_icon:
                    add_icon_item(name_icon)
            else:
                Debug.Log(f"Adding {name_icon}")
                add_icon_item(name_icon)

        Debug.End()
    Debug.End()


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = PreviousMDIcons()

    def build(self):
        return self.screen

    def on_start(self):
        self.screen.set_list_md_icons()


MainApp().run()


# from kivymd.app import MDApp
# from kivy.clock import Clock
# from kivy.metrics import dp
# from kivy.properties import StringProperty
# from kivymd.uix.boxlayout import MDBoxLayout
# from kivy.uix.recycleboxlayout import RecycleBoxLayout
# from kivy.uix.screenmanager import Screen
# from kivy.uix.scrollview import ScrollView

# from kivymd.icon_definitions import md_icons
# from kivymd.uix.button import MDIconButton
# from kivymd.uix.label import MDLabel
# from kivymd.uix.list import OneLineIconListItem
# from kivymd.uix.textfield import MDTextField
# from kivymd.uix.scrollview import MDScrollView
# from kivymd.uix.card import MDCard


# class CustomOneLineIconListItem(OneLineIconListItem):
#     icon = StringProperty()


# class PreviousMDIcons(Screen):
#     def __init__(self, **kwargs):
#         super(PreviousMDIcons, self).__init__(**kwargs)
#         print("__init__")
#          # Create a horizontal box layout offset by half the screen to center the first profile in view.
#         # windowWidth = str(Window.width/2) + "sp"
#         self.Layout = MDBoxLayout(spacing=25, padding=(0,50,0,0), orientation="vertical")

#         self.profileBox = MDBoxLayout(orientation='vertical', spacing="0", padding = (0,"100sp",0,"50sp"), size_hint_y=None)
#         self.profileBox.bind(minimum_height = self.profileBox.setter('height'))

#         # Create the scroll view and add the box layout to it
#         self.scroll = MDScrollView(scroll_type=['bars','content'])
#         self.scroll.smooth_scroll_end = 10

#         self.scroll.add_widget(self.profileBox)
#         self.Layout.add_widget(self.scroll)
#         self.add_widget(self.Layout)

#         import random
#         choices = md_icons.keys()
#         count = 0
#         for key in random.sample(choices,k=50):
#             card = MDIconButton()
#             card.icon = key
#             self.profileBox.add_widget(card)
#             count = count + 1
#             if(count > 100):
#                 break


# class MainApp(MDApp):
#     def build(self):
#         return PreviousMDIcons()


# if __name__ == "__main__":
#     MainApp().run()