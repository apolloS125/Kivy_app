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

        solve_button = Button(text='Solve', on_press=self.solve)
        layout.add_widget(solve_button)

        return layout

    def evaluate_expression(self, expr):
        try:
            return eval(expr) == 24
        except ZeroDivisionError:
            return False

    def find_24_solutions(self, numbers):
        operators = ['+', '-', '*', '/']
        for perm in permutations(numbers):
            for ops in product(operators, repeat=3):
                expr = f"(({perm[0]}{ops[0]}{perm[1]}){ops[1]}{perm[2]}){ops[2]}{perm[3]}"
                if self.evaluate_expression(expr):
                    return expr
        return None

    def solve(self, instance):
        user_numbers = [int(num_input.text) for num_input in self.numbers_input if num_input.text.isdigit()]
        if len(user_numbers) == 4:
            solution = self.find_24_solutions(user_numbers)
            if solution:
                self.solution_label.text = f"A solution to reach 24: {solution} = 24"
            else:
                self.solution_label.text = "No solution found for 24."
        else:
            self.solution_label.text = "Please enter 4 valid numbers."

if __name__ == '__main__':
    Math24Solver().run()
