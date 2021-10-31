from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.properties import (
    NumericProperty, 
    ReferenceListProperty, 
    ObjectProperty
)
from kivy.core.window import Window

import re

class Parent(BoxLayout):
    pass

class ImageButton(ButtonBehavior, Image):
    pass

class HomeScreen(Screen):
    pass

class MenuDropDown(DropDown):
    pass


class MenuWidget(BoxLayout):
    pass

class MenuScreen(Screen):
    pass

class CheckoutScreen(Screen):
    order_info = ObjectProperty(None)
    # for item, info in app.root.
    pass

class CheckoutLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(text_size=self.size, font_size=16, **kwargs)
    pass

class AccountScreen(Screen):
    pass


class MyScreenManager(ScreenManager):
    mode = ''
    order = {}
    menu = {
        "Vegetarian": (5.0, 7.0), "Supreme": (7.0, 10.0), 
        "Pepperoni": (7.0, 10.0), "Beef and Tomato": (7.0, 10.0), 
        "Simply Cheese": (6.0, 9.0), "Hawaiian": (7.0, 10.0), 
        "Cheesy Garlic": (6.0, 9.0), "Mushroom": (5.0, 7.0)
        }
    def home_to_menu(self, mode):
        self.current = 'menuscreen'
        self.mode = mode
        print(self.mode)
    def add_item(self, name, quantity):
        self.order[name] = quantity
    def menu_to_checkout(self):
        print(self.order)
        self.current = 'checkoutscreen'
        for name, quantity in self.order.items():
            line = BoxLayout(
                orientation='horizontal'
            )
            item = CheckoutLabel(
                text=f'{name} x{quantity}',
                halign='left',
            )
            price = CheckoutLabel(
                text=f'${round(int(quantity) * self.menu[name][0], 2)}',
                halign='right',
            )
            line.add_widget(item)
            line.add_widget(price)
            self.children[0].ids.order_info.add_widget(line)
    pass

class OrderApp(App):
    root_widget = Builder.load_file('order.kv')
    def build(self):
        return self.root_widget

if __name__ == '__main__':
    OrderApp().run()