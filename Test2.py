from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Canvas, Color, Rectangle, PushMatrix, PopMatrix, Rotate

kv = '''
<MyWidget>:
    orientation: 'vertical'
    Label:
        id: my_label
        text: 'Hello, World!'
        size_hint_y: None
        height: self.texture_size[1]
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1 # set the background color to white
            Rectangle:
                pos: self.pos
                size: self.size
    Button:
        text: 'Rotate'
        on_press: root.rotate()
'''

class MyWidget(BoxLayout):
    def rotate(self):
        canvas = self.ids.my_label.canvas
        with canvas:
            PushMatrix()
            Rotate(angle=45, origin=self.ids.my_label.center)
            PopMatrix()

class TestApp(App):
    def build(self):
        return MyWidget()

if __name__ == '__main__':
    TestApp().run()