from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from itertools import permutations, product

class StartMenu(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')  # Vertical BoxLayout
        
        start_button = Button(text='Start Math24 Solver', on_press=self.go_to_game)
        start_button2 = Button(text='Start Puzzle Game', on_press=self.go_to_game2)
        
        layout.add_widget(start_button)
        layout.add_widget(start_button2)
        
        names_input = TextInput(hint_text="Enter your Name",multiline=False)
        self.name_input = names_input
        layout.add_widget(names_input)

        self.button3 = Button(text="Summit")
        layout.add_widget(self.button3)
        return layout
    
    def go_to_game(self, instance):
        Math24Solver().run()

    def go_to_game2(self, instance):
        PuzzleGameApp().run()
    
class Math24Solver(App):
    def build(self):
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

        return layout

    def exit(self, instance):
        App.get_running_app().stop()

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

class NumberPuzzleGame(FloatLayout):
    numbers = [11, 4, 6, 5]
    operators = ["+", "-"]
    target_number = 24
    time_left = 30
    score = 30
    solved_puzzles = 1
    unsolved_puzzles = 1360

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        grid_layout = GridLayout(cols=2, spacing=10)
        self.add_widget(grid_layout)

        for number in self.numbers:
            label = Label(text=str(number), font_size=40)
            grid_layout.add_widget(label)

        # Box Layout for game info (target, score, time)
        info_layout = GridLayout(cols=1, spacing=10, size_hint=(None, None), size=(150, 200))
        info_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.add_widget(info_layout)

        self.target_label = Label(text="Target: " + str(self.target_number), font_size=30)
        info_layout.add_widget(self.target_label)

        self.score_label = Label(text="Score: " + str(self.score), font_size=25)
        info_layout.add_widget(self.score_label)

        self.time_label = Label(text="Time: " + str(self.time_left), font_size=25)
        info_layout.add_widget(self.time_label)

        # Box Layout for operator buttons
        button_box = GridLayout(cols=2, spacing=10, size_hint=(None, None), size=(200, 50))
        button_box.pos_hint = {'center_x': 0.5, 'bottom': 0}
        self.add_widget(button_box)

        for operator in self.operators:
            button = Button(text=operator, font_size=30)
            button.bind(on_press=self.handle_operator)
            button_box.add_widget(button)

        # Start the game clock
        Clock.schedule_interval(self.update_time, 1)

    def handle_operator(self, button):
        pass

    def update_time(self, dt):
        self.time_left -= 1
        self.time_label.text = "Time: " + str(self.time_left)
        if self.time_left <= 0:
            # Handle game over
            pass

class PuzzleGameApp(App):
    def build(self):
        return NumberPuzzleGame()  

if __name__ == '__main__':
    StartMenu().run()
