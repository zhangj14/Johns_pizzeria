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
from kivy.uix.button import Button
from kivy.uix.label import Label
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

class MenuWidget(BoxLayout):
    pass

class MenuScreen(Screen):
    pass

class CheckoutScreen(Screen):
    order_info = ObjectProperty(None)
    pass

class CheckoutLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(
            text_size=self.size, 
            font_size=16, 
            size_hint_x=0.9,
            **kwargs)
    pass

class LastScreen(Screen):
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
        total = 0
        for name, quantity in self.order.items():
            price = round(int(quantity) * self.menu[name][0], 2)
            total += price
            line = BoxLayout(
                orientation='horizontal',
                size_hint_y=0.1
            )
            item = CheckoutLabel(
                text=f'{name} x{quantity}',
                halign='left',
            )
            price_l = CheckoutLabel(
                text=f'${price}',
                halign='right',
            )
            line.add_widget(item)
            line.add_widget(price_l)
            self.children[0].ids.order_info.add_widget(line)
        def mode_price(self):
            if self.mode == 'Delivery':
                return 3.00
            else:
                return 0.00
        line = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.1
        )
        item = CheckoutLabel(
            text=f'{self.mode}',
            halign='left',
        )
        price_l = CheckoutLabel(
            text=f'${mode_price(self)}',
            halign='right',
        )
        line.add_widget(item)
        line.add_widget(price_l)
        self.children[0].ids.order_info.add_widget(line)
        line = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.1
        )
        item = CheckoutLabel(
            text='Total:',
            halign='left',
        )
        price_l = CheckoutLabel(
            text=f'${total}',
            halign='right',
        )
        line.add_widget(item)
        line.add_widget(price_l)
        self.children[0].ids.order_info.add_widget(line)
    pass
    def checkout_to_last(self):
        self.current = 'lastscreen'

class OrderApp(App):
    root_widget = Builder.load_file('order.kv')
    def build(self):
        Window.clearcolor = (0.98, 0.93, 0.93, 1)
        return self.root_widget

if __name__ == '__main__':
    OrderApp().run()