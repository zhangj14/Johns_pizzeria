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
from kivy.clock import Clock
from kivy.properties import (
    NumericProperty,
    ReferenceListProperty,
    ObjectProperty,
    StringProperty
)
from kivy.core.window import Window


class ImageButton(ButtonBehavior, Image):
    '''
    To use an image as a button.
    '''
    pass


class FooterButton(BoxLayout):

    next = ObjectProperty()
    destination = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(
            size_hint_y=1,
            orientation='horizontal',
            **kwargs,
        )


class HomeScreen(Screen):
    pass


class MenuDropDown(DropDown):
    pass


class MenuInput(TextInput):

    def insert_text(self, substring, from_undo=False):
        try:
            int(substring)
            if self.text == '':
                return super().insert_text(substring, from_undo=from_undo)
            elif int(self.text) > 1 or int(substring) > 0:
                self.text = "Enter a number between 1 ~ 10."
            else:
                return super().insert_text(substring, from_undo=from_undo)
        except ValueError:
            pass


class MenuWidget(BoxLayout):
    pass


class MenuScreen(Screen):
    pass


class InfoInput(TextInput):

    def insert_text(self, substring, from_undo=False):
        if self.filter == 'str':
            try:
                int(substring)
            except ValueError:
                return super().insert_text(substring, from_undo=from_undo)
            else:
                return
        elif self.filter == 'int':
            try:
                return super().insert_text(str(int(substring)), from_undo=from_undo)
            except ValueError:
                return
        elif self.filter == None:
            return super().insert_text(substring, from_undo=from_undo)


class InfoBox(BoxLayout):
    input = ObjectProperty(None)
    filter = StringProperty(None)
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
    '''
    Root object of the program. Contains 4 different screens.
    '''
    # Initialise variables.
    mode = ''
    order = {}
    menu = {
        "vegetarian": (5.0, 7.0), "supreme": (7.0, 10.0),
        "pepperoni": (7.0, 10.0), "beeftomato": (7.0, 10.0),
        "simplycheese": (6.0, 9.0), "hawaiian": (7.0, 10.0),
        "cheesygarlic": (6.0, 9.0), "mushroom": (5.0, 7.0)
        }

    def home_to_menu(self, mode):
        '''
        Going from homepage to the menu,
        record the user's prefered delivery method.
        '''
        self.transition.direction = 'left'
        self.current = 'menuscreen'
        self.mode = mode
        print(self.mode)

    def menu_to_checkout(self):
        '''
        Going from the menu to the checkout,
        calculate the total price including delivery fee,
        displays the price of individual items.
        '''
        self.transition.direction = 'left'
        self.current = 'checkoutscreen'
        total = 0
        for id, value in self.ids.menuscreen.ids.items():
            # Get the actual text input.
            text = value.ids['quantity'].text
            # Check for the value type again.
            try:
                int(text)
            except:
                continue
            # If no text, pass.
            if text  == '':
                continue
            else:
                # Round it to 2 d.p. following convention.
                price = round(int(text) * self.menu[id][0], 2)
                # Add price to total.
                total += price
                line = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=0.1
                )
                item = CheckoutLabel(
                    text=f'{value.itemname} x{text}',
                    halign='left',
                )
                price_l = CheckoutLabel(
                    text=f'${price}',
                    halign='right',
                )
                # Add the line to the screen.
                line.add_widget(item)
                line.add_widget(price_l)
                self.children[0].ids.order_info.add_widget(line)

        def mode_price(self):
            '''To return a price based on delivery preference.'''
            if self.mode == 'Delivery':
                return 3.00
            else:
                return 0.00

        # Line for delivery / pickup.
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

        # Line for total.
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

    def last_to_home(self, dt):
        '''
        Go from the thank you screen to homepage.
        Dt parameter for 5 seconds delay.
        '''
        self.transition.direction = 'right'
        self.current = 'homescreen'

    def checkout_to_last(self):
        '''
        Go from the checkout page to the thank you page.
        Then called the function 
        to go from the last page to the first.
        '''
        name_field = self.ids.checkoutscreen.ids.name.ids.input
        number_field = self.ids.checkoutscreen.ids.number.ids.input
        if name_field.text == '':
            name_field.text = 'This field is compulsory.'
            return
        if number_field.text == '':
            number_field.text = 'This field is compulsory.'
            return
        else:
            try:
                int(number_field.text)
                pass
            except:
                number_field.text = 'This field is compulsory.'
                return
        self.transition.direction = 'left'
        self.current = 'lastscreen'
        Clock.schedule_once(self.last_to_home, 5)

    def cancel(self):
        '''To cancel the order and reset variables.'''
        self.transition.direction = 'right'
        self.current = 'homescreen'
        self.mode = ''
        self.order = {}
        self.ids.checkoutscreen.ids.order_info.clear_widgets()


class OrderApp(App):
    '''
    App object, starting point for the whole program.
    '''
    # Load the data from the kv file for widgets.
    root_widget = Builder.load_file('order.kv')

    def build(self):
        # Set the window background colour to light red.
        Window.clearcolor = (0.98, 0.93, 0.93, 1)
        return self.root_widget

if __name__ == '__main__':
    OrderApp().run()
