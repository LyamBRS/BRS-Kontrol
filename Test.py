# from kivy.lang import Builder
# from kivy.properties import StringProperty
# from kivy.uix.screenmanager import Screen

# from kivymd.icon_definitions import md_icons
# from kivymd.app import MDApp
# from kivymd.uix.list import OneLineIconListItem


# Builder.load_string(
#     '''
# #:import images_path kivymd.images_path


# <CustomOneLineIconListItem>

#     IconLeftWidget:
#         icon: root.icon


# <PreviousMDIcons>

#     MDBoxLayout:
#         orientation: 'vertical'
#         spacing: dp(10)
#         padding: dp(20)

#         MDBoxLayout:
#             adaptive_height: True

#             MDIconButton:
#                 icon: 'magnify'

#             MDTextField:
#                 id: search_field
#                 hint_text: 'Search icon'
#                 on_text: root.set_list_md_icons(self.text, True)

#         RecycleView:
#             id: rv
#             key_viewclass: 'viewclass'
#             key_size: 'height'

#             RecycleBoxLayout:
#                 padding: dp(10)
#                 default_size: None, dp(48)
#                 default_size_hint: 1, None
#                 size_hint_y: None
#                 height: self.minimum_height
#                 orientation: 'vertical'
# '''
# )


# class CustomOneLineIconListItem(OneLineIconListItem):
#     icon = StringProperty()


# class PreviousMDIcons(Screen):

#     def set_list_md_icons(self, text="", search=False):
#         '''Builds a list of icons for the screen MDIcons.'''

#         def add_icon_item(name_icon):
#             self.ids.rv.data.append(
#                 {
#                     "viewclass": "CustomOneLineIconListItem",
#                     "icon": name_icon,
#                     "text": name_icon,
#                     "callback": lambda x: x,
#                 }
#             )

#         self.ids.rv.data = []
#         for name_icon in md_icons.keys():
#             if search:
#                 if text in name_icon:
#                     add_icon_item(name_icon)
#             else:
#                 add_icon_item(name_icon)


# class MainApp(MDApp):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.screen = PreviousMDIcons()

#     def build(self):
#         return self.screen

#     def on_start(self):
#         self.screen.set_list_md_icons()


# MainApp().run()


# from kivymd.app import MDApp
# from kivymd.uix.button import MDIconButton
# from kivymd.uix.screen import MDScreen
# from kivymd.uix.boxlayout import MDBoxLayout
# from kivymd.uix.floatlayout import MDFloatLayout


# class Example(MDApp):
#     def build(self):
#         self.theme_cls.theme_style = "Dark"
#         self.theme_cls.primary_palette = "Orange"

#         return (
#             MDScreen(
#                 MDFloatLayout(
#                     MDIconButton(
#                         icon="language-python",
#                         pos_hint={"center_x": 0.5, "center_y": 0.5},
#                     )
#                 )
#             )
#         )


# Example().run()




from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty

from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

KV = '''
MDScreen

    MDDropDownItem:
        id: drop_item
        pos_hint: {'center_x': .5, 'center_y': .5}
        text: 'Item 0'
        on_release: app.menu.open()
'''


class IconListItem(OneLineIconListItem):
    icon = StringProperty()
    def __init__(self, **kwargs):
        super(IconListItem, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.add_widget(IconLeftWidget())

class Test(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "git",
                "text": f"Item {i}",
                "height": dp(56),
                "on_release": lambda x=f"Item {i}": self.set_item(x),
            } for i in range(5)
        ]
        print("Menu items created")
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.drop_item,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        print("Menu created")
        self.menu.bind()

    def set_item(self, text_item):
        print("Set items")
        self.screen.ids.drop_item.set_item(text_item)
        self.menu.dismiss()

    def build(self):
        return self.screen


Test().run()