from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.uix.list import ThreeLineListItem


class ThreeLineRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super(ThreeLineRecycleView, self).__init__(**kwargs)
        self.viewclass = 'ThreeLineListItem'
        self.data = [
            {
                "text": f"Title {i}",
                "secondary_text": f"Subtitle {i}",
                "tertiary_text": f"Description {i}",
            }
            for i in range(10)
        ]


class CardExample(MDCard):
    def __init__(self, **kwargs):
        super(CardExample, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = "8dp"

        self.rv = ThreeLineRecycleView()
        self.add_widget(self.rv)


class ExampleApp(MDApp):
    def build(self):
        return CardExample()


if __name__ == "__main__":
    ExampleApp().run()