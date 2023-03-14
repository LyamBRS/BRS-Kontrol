from tkinter import Button
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug
from kivy.uix.button import Button

from kivy.app import App
from kivy.uix.recycleview import RecycleView
from kivy.uix.button import Button

class MyRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super(MyRecycleView, self).__init__(**kwargs)
        self.data = [{'text': str(i)} for i in range(10)]
        self.viewclass = 'MyButton'
        self.button_pressed_callback = None

class MyButton(Button):
    def on_press(self):
        if self.parent.parent.button_pressed_callback:
            self.parent.parent.button_pressed_callback(self)

class TestApp(App):
    def build(self):
        def button_pressed(button):
            print("Button", button.text, "pressed")

        rv = MyRecycleView()
        rv.button_pressed_callback = button_pressed
        return rv

if __name__ == '__main__':
    TestApp().run()