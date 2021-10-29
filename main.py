from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown
from kivy.properties import (
    NumericProperty, 
    ReferenceListProperty, 
    ObjectProperty
)
from kivy.core.window import Window


class Parent(BoxLayout):
    pass

class ImageButton(ButtonBehavior, Image):
    pass

class HomeScreen(Screen):
    pass

class MenuDropDown(DropDown):
    pass

class MenuScreen(Screen):
    Vegetarian = ObjectProperty(None)
    Supreme = ObjectProperty(None)
    Pepperoni = ObjectProperty(None)
    Beef_and_tomato = ObjectProperty(None)
    Simply_cheese = ObjectProperty(None)
    Hawiian = ObjectProperty(None)
    Cheesy_garlic = ObjectProperty(None)
    Mushroom = ObjectProperty(None)
    pass

class CheckoutScreen(Screen):
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
        "Cheesy Garlic": (6.0, 9.0), "Mushroom": (5.0, 7.0)}
    def home_to_menu(self, mode):
        self.current = 'menuscreen'
        self.mode = mode
    def menu_to_checkout(self):
        # for item in self.menu.keys():
        #     try:
        #         self.add_item(item)
        #     except TypeError:
        #         pass
        # print(self.order)
        # self.current = 'checkoutscreen'
        return
    def home_to_menu(self, mode):
        self.current = 'menuscreen'
        self.mode = mode
    def home_to_menu(self, mode):
        self.current = 'menuscreen'
        self.mode = mode
        print(self.mode)
    def add_item(self, name):
        self.order[name] = (self.ids[name], self.ids[name] * self.menu[name][0])
    pass

class OrderApp(App):
    root_widget = Builder.load_file('order.kv')
    def build(self):
        return self.root_widget

if __name__ == '__main__':
    OrderApp().run()