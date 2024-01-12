from kivy.app import App
import random
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from itertools import permutations, product
from kivy.uix.popup import Popup
from kivy.clock import Clock

class StartMenu(Screen):
    def __init__(self, **kwargs):
        super(StartMenu, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical')
        self.greeting = Label(text='Welcome ')
        self.start_button = Button(text='Start Math24 Solver', on_press=self.go_to_game, font_size=40)
        self.start_button2 = Button(text='Start Puzzle Game', on_press=self.go_to_game2, font_size=40)
        
        self.greeting.pis_hint = {"top": 1}
        layout.add_widget(self.greeting)
        layout.add_widget(self.start_button)
        layout.add_widget(self.start_button2)
        
        names_input = TextInput(hint_text="Enter your Name", multiline=False)
        self.name_input = names_input
        layout.add_widget(self.name_input)

        self.button3 = Button(text="Summit", on_press=self.callback)
        layout.add_widget(self.button3)
        
        self.add_widget(layout)

    def go_to_game(self, instance):
        self.manager.current = 'math24_solver'

    def go_to_game2(self, instance):
        PuzzleGame.is_game_started = True
        self.manager.current = 'difficulty'

    def callback(self, instance):
        self.greeting.text = 'Welcome' + ' ' + self.name_input.text

class Math24Solver(Screen):
    def __init__(self, **kwargs):
        super(Math24Solver, self).__init__(**kwargs)
        self.numbers_input = []
        self.solution_label = Label(text="Enter 4 numbers")      
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.solution_label)

        for _ in range(4):
            number_input = TextInput(hint_text='Number')
            self.numbers_input.append(number_input)
            layout.add_widget(number_input)

        solve_button = Button(text='Solve', on_press=self.solve, size_hint_y=None, height=50)
        layout.add_widget(solve_button)
        exit_button = Button(text='Exit a game', on_press=self.exit, size_hint_y=None, height=50)
        layout.add_widget(exit_button)

        self.add_widget(layout)

    def exit(self, instance):
        self.manager.current = 'start_menu'
    
    #for check ans
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
    is_game_started = False
    difficulty_level = "Easy"
    number_range = (0, 0)
    target_range = (0, 0)

    def __init__(self, **kwargs):
        super(PuzzleGame, self).__init__(**kwargs)
        self.initialize_game()

    def initialize_game(self):
        self.operators = ["+", "-", "*", "/", "(", ")"]
        self.numbers = [0, 0, 0, 0]
        self.target_number = 0
        self.time_left = 30
        self.score = 0
        self.solved_puzzles = 1
        self.unsolved_puzzles = 1360

        self.layout = GridLayout(cols=4)
        self.number_labels = []

        self.generate_random_numbers()

        for number in self.numbers:
            label = Button(text=str(number), font_size=30, on_press=self.handle_number)
            self.layout.add_widget(label)
            self.number_labels.append(label)

        self.target_label = Label(text=f"Target: {self.target_number}", font_size=30)
        self.layout.add_widget(self.target_label)

        self.score_label = Label(text=f"Score: {self.score}", font_size=25)
        self.layout.add_widget(self.score_label)

        self.time_label = Label(text=f"Time: {self.time_left}", font_size=25)
        self.layout.add_widget(self.time_label)

        operators_grid = GridLayout(cols=2)
        for operator in self.operators:
            button = Button(text=operator, font_size=30, on_press=self.handle_operator)
            operators_grid.add_widget(button)
        self.layout.add_widget(operators_grid)

        exit_button = Button(text='Exit a game', on_press=self.exit)
        skip_button = Button(text="START/SKIP", font_size=30, on_press=self.handle_skip)
        done_button = Button(text="DONE", font_size=30, on_press=self.handle_done)
        self.solution_label = Label(text="Calculate here", font_size=20)

        self.layout.add_widget(exit_button)
        self.layout.add_widget(skip_button)
        self.layout.add_widget(done_button)
        self.layout.add_widget(self.solution_label)

        Clock.schedule_interval(self.update_time, 1 if self.is_game_started else 0)

        self.add_widget(self.layout)

    def handle_number(self, button):
        number = button.text
        current_text = self.solution_label.text
        if current_text == "Calculate here":
            current_text = ""
        self.solution_label.text = current_text + number
        button.text = ""
        button.background_color = [0, 1, 0, 1]

    #for call operator
    def handle_operator(self, operator_button):
        operator = operator_button.text
        current_text = self.solution_label.text
        self.solution_label.text = current_text + operator

    def handle_skip(self, skip_button):
        self.is_game_started = True
        self.update_number_labels()
        self.next_puzzle()
        # skip_button.background_color = [1, 1, 1, 1]

    #for gennumber and regennumber
    def generate_random_numbers(self):
        self.numbers = [random.randint(*self.number_range) for _ in range(4)]
        self.update_number_labels()

    def update_number_labels(self):
        for label, number in zip(self.number_labels, self.numbers):
            label.text = str(number)

    def update_target(self):
        self.target_number = random.randint(*self.target_range)
        self.target_label.text = f"Target: {self.target_number}"

    def handle_done(self, done_button):
        if self.check_solution():
            self.score += 10
            self.next_puzzle()
        else:
            self.show_incorrect_popup()

    def show_incorrect_popup(self):
        popup = Popup(title='Incorrect Solution', content=Label(text='Try again!'), size_hint=(None, None), size=(400, 200))
        popup.open()

    #for done button
    def check_solution(self):
        try:
            result = eval(self.solution_label.text)
            return result == self.target_number
        except ZeroDivisionError:
            return False
        except:
            return False

    #for skip and done button
    def next_puzzle(self):
        self.generate_random_numbers()
        self.update_target()
        self.solved_puzzles += 1
        self.unsolved_puzzles -= 1
        self.score_label.text = f"Score: {self.score}"
        self.solution_label.text = ""
        self.time_left = 30

    def update_time(self, dt):
        if self.is_game_started and self.time_left > 0:
            self.time_left -= dt  # Decrement by elapsed time
            self.time_label.text = f"Time: {int(self.time_left)}"  # Display as integer seconds
        elif self.is_game_started:
            self.time_left = 30
            self.is_game_started = False
            self.show_game_over_popup()
    
    #show score when game over
    def show_game_over_popup(self):
        popup = Popup(title='Game Over', content=Label(text=f'Your final score is {self.score}'), size_hint=(None, None), size=(400, 200))
        self.score = 0
        popup.open()

    def exit(self, exit_button):
        self.is_game_started = False
        self.manager.current = 'start_menu'

class select_Difficulty(Screen):
    def __init__(self, **kwargs):
        super(select_Difficulty, self).__init__(**kwargs)

        layout = GridLayout(cols=1)

        label = Label(text="Select Difficulty", font_size=30)
        
        easy_button = Button(text="Easy", on_press=self.set_difficulty_easy)
        medium_button = Button(text="Medium", on_press=self.set_difficulty_normal)
        hard_button = Button(text="Hard", on_press=self.set_difficulty_hard)
        exit_button = Button(text='Back to menu', on_press=self.exit)

        layout.add_widget(label)
        layout.add_widget(easy_button)
        layout.add_widget(medium_button)
        layout.add_widget(hard_button)
        layout.add_widget(exit_button)

        self.add_widget(layout)
    
    def set_difficulty_easy(self, instance):
        # Set the range of numbers between 1 - 10 and the range of the target to be 1 - 10
        PuzzleGame.number_range = (1, 11)
        PuzzleGame.target_range = (1, 31)
        
        PuzzleGame.is_game_started = True
        PuzzleGame.difficulty_level = "Easy"
        self.manager.current = 'puzzle_game'

    def set_difficulty_normal(self, instance):
        # Set the range of numbers between 1 - 50 and the range of the target to be 1 - 50
        PuzzleGame.number_range = (1, 21)
        PuzzleGame.target_range = (1, 51)
        
        PuzzleGame.is_game_started = True
        PuzzleGame.difficulty_level = "Medium"
        self.manager.current = 'puzzle_game'

    def set_difficulty_hard(self, instance):
        # Set the range of numbers between 1 - 100 and the range of the target to be 1 - 100
        PuzzleGame.number_range = (1, 51)
        PuzzleGame.target_range = (1, 100)
        
        PuzzleGame.is_game_started = True
        PuzzleGame.difficulty_level = "Hard"
        self.manager.current = 'puzzle_game'

    def exit(self, exit_button):
        self.manager.current = 'start_menu'

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartMenu(name='start_menu'))
        sm.add_widget(select_Difficulty(name='difficulty'))
        sm.add_widget(Math24Solver(name='math24_solver'))
        sm.add_widget(PuzzleGame(name='puzzle_game'))
        return sm

if __name__ == '__main__':
    MyApp().run()
