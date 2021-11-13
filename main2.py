from kivy.app import App
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Line


class Label(Label):
    '''
    Style the default label widgets.
    '''
    def __init__(self, **kwargs):
        super().__init__(
            color='#cc3d0b', 
            font_name='Comfortaa-VariableFont_wght', 
            font_size=16,
            **kwargs)


class TextInput(TextInput):
    '''
    Style the default text input.
    '''
    def __init__(self, **kwargs):
        super().__init__(
            background_color='#fcf0f0',
            foreground_color='#000000',
            font_name='Consola',
            font_size='16'
            **kwargs)


class Button(Button):
    '''
    Style the default buttons.
    '''
    def __init__(self, **kwargs):
        super().__init__(
            size_hint_y=1,
            font_size=18,
            background_normal='',
            background_down='',
            background_color='#fbb448',
            font_name='Consola',
            **kwargs)
        with self.canvas:
            Color(243/255, 103/255, 13/255, 1)
            Line(
                width=10, 
                Rectangal=(self.x, self.y, self.width, self.height))


class ImageButton(ButtonBehavior, Image):
    '''
    Images that act as buttons.
    Used in homepage.
    '''
    def __init__(self, **kwargs):
        super().__init__(
            allow_stetch=True,
            keep_ratio=True,
            **kwargs)


class Header(Label):
    '''
    Header containing the name of the restaurant.
    '''
    def __init__(self, **kwargs):
        super().__init__(
            text_size=self.size,
            text="John's Pizzeria",
            font_size=30,
            halign='left',
            **kwargs)


class Footer(BoxLayout):
    '''
    Footer containing a button for 
    cancelling the order, and a button for proceding.
    '''
    def __init__(self, **kwargs):
        super().__init__(
            orientation='horizontal',
            size_hint_y=1,
            **kwargs)
        # Button for cancelling the order.
        self.add_widget(Button(
            text='<<<Cancel<<<',
            on_release=''
        ))

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
    pass


class ConfirmScreen(Screen):
    '''
    Fourth page of the program.
    Containing header, personal info and order info display and footer.
    '''
    pass


class ThankyouScreen(Screen):
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
    pass


class OrderAApp(App):
    '''
    App object.
    Entry point for this program
    '''
    def build(self):
        return Button(text="I am a button.")

if __name__ == '__main__':
    OrderAApp().run()