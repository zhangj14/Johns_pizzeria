from kivy.app import App
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (
    NumericProperty, 
    ReferenceListProperty, 
    ObjectProperty
)

class Parent(BoxLayout):
    pass

class Header(Widget):
    pass

class HomePage(Widget):
    pass

class OrderApp(App):
    def build(self):
        root = Parent()

        return root


if __name__ == '__main__':
    OrderApp().run()