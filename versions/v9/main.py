from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty


import re


class ImageButton(ButtonBehavior, Image):
    '''
    Homepage.
    Images that act as buttons.
    '''
    pass


class Header(Label):
    '''
    Header containing the name of the restaurant.
    '''
    pass


class Footer(BoxLayout):
    '''
    Footer containing a button for
    cancelling the order, and a button for proceding.
    '''
    destination = StringProperty('')
    pass


class ModeSelection(BoxLayout):
    '''
    Homepage.
    The modeselection area of homepage.
    '''
    mode = StringProperty('')
    source = StringProperty('')
    pass


class MenuInput(TextInput):
    '''
    Menupage.
    Input field for quantity of item.
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
    '''
    Menupage.
    Containing item name, image and a menuinput.
    '''
    itemname = StringProperty('')
    itemsource = StringProperty('')
    pass


class CheckoutLabel(Label):
    '''
    Checkout and Confirm page.
    Left-align text.
    '''
    pass


class InfoInput(TextInput):
    '''
    Checkoutpage.
    Input field for personal info.
    '''
    filter = StringProperty(None)
    if filter == 'str':
        special = '!@#$%^&*()_+}{|":?><~`=[];\',./\\'
    else:
        special = '!@#$%^&*()_+}{|:?><~`=[];/'

    def _on_focus(self, instance, value, *largs):
        '''
        Overwrite the on_focus method.
        Automatically clear the input fields
        when they are focused.
        '''
        if any((self.text == 'A valid phone number is required.',
                self.text == 'This field is compulsory.',
                self.text == 'A valid address is required.')):
            self.text = ''
        return super()._on_focus(instance, value, *largs)

    def insert_text(self, substring, from_undo=False):
        '''
        Overwrite the insert_text method.
        '''
        # Dealing with special character.
        if substring in self.special:
            return
        # Dealing with spaces and newline character.
        if (((len(self.text) == 0
                or self.text[-1] == ' '
                or self.text[-1] == '\n')
                and substring == ' ')
            or
            ((len(self.text) == 0
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
                    return super().insert_text(substring.capitalize(),
                                               from_undo=from_undo)
                else:
                    return super().insert_text(substring, from_undo=from_undo)
        # Phone number field.
        elif self.filter == 'int':
            # Less than 13 digits.
            if len(self.text) > 13:
                return
            # Integer only.
            try:
                return super().insert_text(str(int(substring)),
                                           from_undo=from_undo)
            except ValueError:
                return
        # Address and notes.
        elif self.filter is None:
            # Less than 150 characters.
            if len(self.text) > 100:
                return
            else:
                return super().insert_text(substring, from_undo=from_undo)


class InfoBox(BoxLayout):
    '''
    Checkoutpage.
    Containing InfoInput and a prompt.
    '''
    pass


class InfoBoxes(StackLayout):
    '''
    Checkoutpage.
    Containing four InfoBoxes.
    '''
    pass


class HomeScreen(Screen):
    '''
    First page of the program.
    Containing header, banner image and mode selection.
    '''
    pass


class MenuScreen(Screen):
    '''
    Second page of the program.
    Containing header, images and names, input fields and footer.
    '''
    pass


class CheckoutScreen(Screen):
    '''
    Third page of the program.
    Containing header, personal info input , order info and footer.
    '''
    order_info = ObjectProperty(None)
    pass


class ConfirmScreen(Screen):
    '''
    Fourth page of the program.
    Containing header, personal info
    and order info display and footer.
    '''
    order_info = ObjectProperty(None)


class LastScreen(Screen):
    '''
    Last page of the program.
    Containing thank you and redirect to homepage automatically.
    '''
    pass


class MyScreenManager(ScreenManager):
    '''
    ScreenManager object.
    Root widget of the whole program.
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
        Homepage to Menupage.
        Record the user's prefered delivery method.
        '''
        self.transition.direction = 'left'
        self.current = 'menuscreen'
        self.mode = mode

    def get_order(self, destination):
        '''
        Used in Checkout and Confirm.
        Create order info based on the input fields in Menupage.
        '''
        menu = self.ids.menuscreen

        def mode_price(self):
            '''
            To return a price based on delivery preference.
            '''
            if self.mode == 'Delivery':
                return 3.00
            else:
                return 0.00

        if destination == self.ids.checkoutscreen:
            input = destination.ids.infobox.ids.address.ids.input
            # Disabled the address field if the mode is Pickup.
            if self.mode == 'Pickup':
                input.disabled = True
                input.text = 'N/A'
            else:
                input.disabled = False

        total = 0
        # Loop through the input fields in Menupage.
        for id, value in menu.ids.items():
            # Get the actual text input.
            text = value.ids['quantity'].text
            # Check for the value type again.
            try:
                int(text)
            except:
                continue
            # If no text, pass.
            if text == '':
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
                destination.ids.order_info.add_widget(line)
        # If nothing is selected, return.
        if total == 0:
            text = 'Please select at least one item.'
            menu.ids.pepperoni.ids.quantity.text = text
            return False

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
        destination.ids.order_info.add_widget(line)

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
        destination.ids.order_info.add_widget(line)
        return True

    def menu_to_checkout(self):
        '''
        Menupage to Checkoutpage,
        calculate the total price including delivery fee,
        displays the price of individual items.
        '''
        if not self.get_order(self.ids.checkoutscreen):
            return
        # Change the screen.
        self.transition.direction = 'left'
        self.current = 'checkoutscreen'

    def checkout_to_confirm(self):
        '''
        Take the information from the checkout input fields
        and display them. Let the user confirm them.
        '''
        # Access the input fields.
        infobox = self.ids.checkoutscreen.ids.infobox
        name = infobox.ids.name.ids.input
        number = infobox.ids.number.ids.input
        address = infobox.ids.address.ids.input
        note = infobox.ids.note.ids.input
        order = self.ids.checkoutscreen.ids.order_info
        # Name, phone number and address are compulsory.
        if any((name.text == '',
                name.text == 'This field is compulsory.')):
            name.text = 'This field is compulsory.'
            return
        if number.text == '':
            number.text = 'This field is compulsory.'
            return
        # Phone numbers have to be more than 7 digits.
        if len(number.text) < 7:
            number.text = 'A valid phone number is required.'
            return
        if self.mode == 'Delivery':
            if any((address.text == '',
                    address.text == 'This field is compulsory.',
                    address.text == 'A valid address is required.')):
                address.text = 'This field is compulsory.'
                return
            pat = '[A-Za-z][A-Za-z][A-Za-z]'
            # Manully check if it might be a word.
            if not all((re.search(pat, address.text),
                        re.search('[aeiou]', address.text))):
                address.text = 'A valid address is required.'
                return
        else:
            try:
                int(number.text)
                pass
            except:
                number.text = 'This field is compulsory.'
                return
        # Add info to the confirm page.
        confirm = self.ids.confirmscreen
        confirm.order_info = order
        infobox = self.ids.confirmscreen.ids.infobox
        # Create the info labels based on the value
        # in the respective input fields.
        name_l = CheckoutLabel(
            text=f'Order Name: {name.text}',
            halign='left'
        )
        number_l = CheckoutLabel(
            text=f'Phone Number: {number.text}',
            halign='left'
        )
        address_l = CheckoutLabel(
            text=f'Delivery Address: {address.text}',
            halign='left'
        )
        note_l = CheckoutLabel(
            text=f'Note: {note.text}',
            halign='left'
        )
        # Add the information labels in.
        infobox.add_widget(name_l)
        infobox.add_widget(number_l)
        infobox.add_widget(address_l)
        infobox.add_widget(note_l)
        self.get_order(self.ids.confirmscreen)
        # Change the screen.
        self.transition.direction = 'left'
        self.current = 'confirmscreen'

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
        confirm = self.ids.confirmscreen
        for widget in menu.ids.values():
            widget.ids.quantity.text = ''
        checkout.ids.order_info.clear_widgets()
        for widget in checkout.ids.infobox.ids.values():
            widget.ids.input.text = ''
        for widget in confirm.ids.values():
            widget.clear_widgets()


class OrderApp(App):
    '''
    App object.
    Entry point for this program
    '''
    root_widget = Builder.load_file('versions/v9/order.kv')

    def build(self):
        # Set the minumum size.
        Window.minimum_width, Window.minimum_height = Window.size
        # Set the background colour.
        Window.clearcolor = (0.98, 0.93, 0.93, 1)
        return self.root_widget

if __name__ == '__main__':
    OrderApp().run()
