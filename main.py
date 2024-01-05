from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from itertools import permutations, product

class Math24Solver(App):
    def build(self):
        self.numbers_input = []
        self.solution_label = Label(text="Enter 4 numbers and press 'Solve' to find a solution for 24.")

        layout = GridLayout(cols=3)
        layout.add_widget(self.solution_label)

        for i in range(4):
            number_input = TextInput(hint_text='Number')
            self.numbers_input.append(number_input)
            layout.add_widget(number_input)

        solve_button = Button(text='Solve')
        layout.add_widget(solve_button)

        return layout

    def evaluate_expression(self, expr):
        try:
            return eval(expr) == 24
        except ZeroDivisionError:
            return False

if __name__ == '__main__':
    Math24Solver().run()
