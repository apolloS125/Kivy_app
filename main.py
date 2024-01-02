from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import random

class Math24App(App):
    def build(self):
        layout = GridLayout(cols=6, spacing=10)
        
        # Generate 30 buttons
        for i in range(30):
            btn = Button(text=str(i + 1))
            btn.bind(on_press=self.get_random_callback())
            layout.add_widget(btn)
        
        return layout

    def get_random_callback(self):
        callbacks = [self.callback1, self.callback2, self.callback3, self.callback4, 
                     self.callback5, self.callback6, self.callback7, self.callback8, 
                     self.callback9, self.callback10]

        return random.choice(callbacks)

    # Define 10 different callback functions
    def callback1(self, instance):
        pass

    def callback2(self, instance):
        pass
