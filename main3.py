from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import (
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
    '''
    Footer in all pages.
    '''
    next = ObjectProperty()
    destination = StringProperty('')


class HomeScreen(Screen):
    pass


class MenuInput(TextInput):
    '''
    Customise the input fields in the menu page.
    '''
    def insert_text(self, substring, from_undo=False):
        '''
        Overwrite the insert_text method.
        '''
        try:
            # If it's an integer.
            int(substring)
            # 0 is not allowed.
            if self.text == '' and substring != '0':
                return super().insert_text(substring, 
                                           from_undo=from_undo)
            # Between 1 and 10 only.
            elif int(self.text) > 1 or int(substring) > 0:
                self.text = "Enter a number between 1 ~ 10."
            else:
                return super().insert_text(substring, 
                                           from_undo=from_undo)
        except ValueError:
            pass
    
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        '''
        Overwrite the keyboard_on_key_down method. 
        Remove all text when the user press 'backspace'.
        '''
        if keycode[0] == 8:
            self.text = ''
            return
        return super().keyboard_on_key_down(window, keycode, 
                                            text, modifiers)
    
    def _on_focus(self, instance, value, *largs):
        '''
        Overwrite the on_focus method.
        Remove all text when the user focus / unfocus the input fields.
        '''
        try:
            int(self.text)
        except ValueError:
            self.text = ''
        return super()._on_focus(instance, value, *largs)


class MenuWidget(BoxLayout):
    pass


class MenuScreen(Screen):
    pass


class InfoInput(TextInput):
    '''
    Customise the input fields in the checkout page.
    '''
    # def __init__(self, filter=None, **kwargs):
    #     self.filter = filter
    #     self.id = 'input'
    #     super().__init__(**kwargs)

    def insert_text(self, substring, from_undo=False):
        '''
        Overwrite the insert_text method.
        '''
        # Dealing with spaces and newline character.
        if (
            ((len(self.text) == 0 
            or self.text[-1] == ' '
            or self.text[-1] == '\n')
            and substring == ' ')
            or ((len(self.text) == 0 
            or self.text[-1] == '\n')
            and substring == '\n')):
            return
        # Name field.
        if self.filter == 'str':
            try:
                # Cannot be integer.
                int(substring)
                return
            except ValueError:
                # Less than 50 characters.
                if len(self.text) > 50:
                    return
                # Capitalisation.
                elif len(self.text) == 0 or self.text[-1] == ' ':
                    return super().insert_text(substring.capitalize(), from_undo=from_undo)
                else:
                    return super().insert_text(substring, from_undo=from_undo)
        # Phone number field.
        elif self.filter == 'int':
            # Less than 13 digits.
            if len(self.text) > 13:
                return
            # Integer only.
            try:
                return super().insert_text(str(int(substring)), from_undo=from_undo)
            except ValueError:
                return
        # Address and notes.
        elif self.filter == None:
            # Less than 150 characters. 
            if len(self.text) > 100:
                return
            else:
                return super().insert_text(substring, from_undo=from_undo)

    def _on_focus(self, instance, value, *largs):
        '''
        Overwrite the _on_focus method.
        Automaticallt remove the text when it's focused.
        '''
        if (self.text == 'This field is compulsory.'
        or self.text == 'A valid phone number is required.'):
            self.text = ''
        else:
            pass
        return super()._on_focus(instance, value, *largs)


class InfoBox(BoxLayout):
    '''
    Checkout page.
    Containging a prompt and a text box.
    '''
    input = ObjectProperty(None)
    filter = StringProperty(None)
    prompt = StringProperty('')
    # def __init__(self, prompt=str(prompt),filter=str(filter), **kwargs):
    #     super().__init__(**kwargs)
    #     self.add_widget(Label(text=prompt))
    #     self.add_widget(InfoInput(filter=filter))
    pass


class CheckoutScreen(Screen):
    order_info = ObjectProperty(None)
    pass


class CheckoutLabel(Label):
    '''
    Text that is left-aligned.
    '''
    def __init__(self, **kwargs):
        super().__init__(
            text_size=self.size,
            font_size=16,
            size_hint_x=0.9,
            **kwargs)
    pass


class ConfirmScreen(Screen):
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

    def menu_to_checkout(self):
        '''
        Going from the menu to the checkout,
        calculate the total price including delivery fee,
        displays the price of individual items.
        '''
        menu = self.ids.menuscreen
        checkout = self.ids.checkoutscreen
        def mode_price(self):
            '''To return a price based on delivery preference.'''
            if self.mode == 'Delivery':
                return 3.00
            else:
                return 0.00

        if self.mode == 'Pickup':
            input = checkout.ids.infobox
            input.disabled = True
            input.text = 'N/A'

        total = 0
        for id, value in menu.ids.items():
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
                checkout.ids.order_info.add_widget(line)
        if total == 0:
            text = 'Please select at least one item.'
            menu.ids.pepperoni.ids.quantity.text = text
            return

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
        checkout.ids.order_info.add_widget(line)

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
            text=f'${total + mode_price(self)}',
            halign='right',
        )
        line.add_widget(item)
        line.add_widget(price_l)
        checkout.ids.order_info.add_widget(line)
        self.transition.direction = 'left'
        self.current = 'checkoutscreen'

    def checkout_to_confirm(self):
        '''
        Take the informationi from the checkout input fields
        and display them. Let the user confirm them.
        '''
        # Access the input fields.
        infobox = self.ids.checkoutscreen.ids.infobox
        name_field = infobox.ids.name.ids.input
        number_field = infobox.ids.number.ids.input
        address_field = infobox.ids.address.ids.input
        note_field = infobox.ids.note.ids.input
        # Name, phone number and address are compulsory.
        if name_field.text == '':
            name_field.text = 'This field is compulsory.'
            return
        if number_field.text == '':
            number_field.text = 'This field is compulsory.'
            return
        if len(number_field.text) < 7:
            number_field.text = 'A valid phone number is required.'
            return
        if address_field.text == '' and self.mode == 'Delivery':
            address_field.text = 'This field is compulsory.'
            return
        else:
            try:
                int(number_field.text)
                pass
            except:
                number_field.text = 'This field is compulsory.'
                return
        # Clear the left side of the page.
        infobox.clear_widgets()
        name = Label(
            text=f'Order Name: {name_field.text}',
            size_hint_y=0.2,
            halign='left'
        )
        number = Label(
            text=f'Phone Number: {number_field.text}',
            size_hint_y=0.2,
            halign='left'
        )
        address = Label(
            text=f'Delivery Address: {address_field.text}',
            size_hint_y=0.2,
            halign='left'
        )
        note = Label(
            text=f'Note: {note_field.text}',
            size_hint_y=0.2,
            halign='left'
        )
        # Add the information labels in.
        infobox.add_widget(name)
        infobox.add_widget(number)
        infobox.add_widget(address)
        infobox.add_widget(note)
        self.ids.checkoutscreen.ids.footer.destination = 'Confirm'

    def confirm(self):
        '''
        Let the user confirm their information.
        Once confirmed, they will be directed to a thankyou page, 
        and then directed back to the homepage in 5 seconds.
        '''
        self.transition.direction = 'left'
        self.current = 'lastscreen'
        Clock.schedule_once(self.last_to_home, 5)

    def last_to_home(self, dt):
        '''
        Go from the thank you screen to homepage.
        Dt parameter for 5 seconds delay.
        '''
        self.cancel()

    def cancel(self):
        '''
        To cancel the order and reset variables.
        '''
        self.transition.direction = 'right'
        self.current = 'homescreen'
        self.mode = ''
        self.order = {}
        # Clear the widgets.
        checkout = self.ids.checkoutscreen
        menu = self.ids.menuscreen
        checkout.ids.infobox.clear_widgets()
        for widget in menu.ids.values():
            widget.ids.quantity.text = ''
        checkout.ids.order_info.clear_widgets()
        # checkout.ids.order_info.add_widget(
        #     InfoBox(id='name',
        #     prompt='Please enter your name',
        #     multiline=False,
        #     filter='str'))
        # checkout.ids.order_info.add_widget(
        #     InfoBox(id='number',
        #     prompt='Please enter your phone nmuber',
        #     multiline=False,
        #     filter='int'))
        # checkout.ids.order_info.add_widget(
        #     InfoBox(id='address',
        #     prompt='Please enter your address',
        #     multiline=True,
        #     filter=None))
        # checkout.ids.order_info.add_widget(
        #     InfoBox(id='note',
        #     prompt='Anything else we need to know',
        #     multiline=True,
        #     filter=None))
        for widget in checkout.ids.values():
            try:
                widget.input.text = ''
            except AttributeError:
                continue


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
