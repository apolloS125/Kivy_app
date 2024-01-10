from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from itertools import permutations, product

class StartMenu(Screen):
    def __init__(self, **kwargs):
        super(StartMenu, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical')
        
        start_button = Button(text='Start Math24 Solver', on_press=self.go_to_game)
        start_button2 = Button(text='Start Puzzle Game', on_press=self.go_to_game2)
        
        layout.add_widget(start_button)
        layout.add_widget(start_button2)
        
        names_input = TextInput(hint_text="Enter your Name", multiline=False)
        self.name_input = names_input
        layout.add_widget(names_input)

        self.button3 = Button(text="Summit")
        layout.add_widget(self.button3)
        
        self.add_widget(layout)

    def go_to_game(self, instance):
        self.manager.current = 'math24_solver'

    def go_to_game2(self, instance):
        self.manager.current = 'puzzle_game'

class Math24Solver(Screen):
    def __init__(self, **kwargs):
        super(Math24Solver, self).__init__(**kwargs)

        self.numbers_input = []
        self.solution_label = Label(text="Enter 4 numbers")      
        layout = GridLayout(cols=3)
        layout.add_widget(self.solution_label)

        for i in range(4):
            number_input = TextInput(hint_text='Number')
            self.numbers_input.append(number_input)
            layout.add_widget(number_input)

        solve_button = Button(text='Solve', on_press=self.solve)
        layout.add_widget(solve_button)
        exit_button = Button(text='Exit a game', on_press=self.exit)
        layout.add_widget(exit_button)

        self.add_widget(layout)

    def exit(self, instance):
        StartMenu().run

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

class PuzzleGame(Screen):
    def __init__(self, **kwargs):
        super(PuzzleGame, self).__init__(**kwargs)
        

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartMenu(name='start_menu'))
        sm.add_widget(Math24Solver(name='math24_solver'))
        sm.add_widget(PuzzleGame(name='puzzle_game'))
        return sm

if __name__ == '__main__':
    MyApp().run()
