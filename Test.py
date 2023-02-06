from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import ScrollView,MDScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

class ExampleApp(MDApp):
    def build(self):
        # Create a horizontal box layout
        box = BoxLayout(orientation='horizontal', spacing=10, padding = 50, size_hint_x=None)
        box.bind(minimum_width = box.setter('width'))


        # Create 10 MDCards and add them to the box layout
        for i in range(50):
            card = MDCard(size=(400, 500), size_hint_x=None)
            card.md_bg_color = (1,0,1,1)
            box.add_widget(card)

        # Create the scroll view and add the box layout to it
        scroll = MDScrollView(scroll_type=['bars','content'])
        scroll.smooth_scroll_end = 10
        scroll.add_widget(box)

        return scroll

ExampleApp().run()