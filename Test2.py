from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from Libraries.BRS_Python_Libraries.BRS.Debug.consoleLog import Debug

class MainWidget(FloatLayout):

    def create_layouts(self):
        Debug.Start("create_layouts")
        self.create_recycle_view()
        Debug.End()

    def create_recycle_view(self):
        Debug.Start("create_recycle_view")
        recycle_box_layout = RecycleBoxLayout(default_size=(None,
                                              dp(56)),
                                              default_size_hint=(1, None),
                                              size_hint=(1, None),
                                              orientation='vertical')
        recycle_box_layout.bind(minimum_height=recycle_box_layout.setter("height"))
        recycle_view = RecycleView()
        recycle_view.add_widget(recycle_box_layout)
        recycle_view.viewclass = 'Label'
        self.add_widget(recycle_view)
        recycle_view.data = [{'text': str(x)} for x in range(20)]
        Debug.End()


class MainApp(App):
    def build(self):
        Debug.enableConsole = True
        Debug.Start("build")
        Clock.schedule_once(self.add_rv)
        Debug.End()
        return MainWidget()

    def add_rv(self, dt):
        Debug.Start("add_rv")
        self.root.create_layouts()
        Debug.End()


MainApp().run()