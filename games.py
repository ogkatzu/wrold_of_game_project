import random
from flask import request
import ast
import requests


class Game:
    def __init__(self, name, difficulty=None):
        self.name = name
        self.difficulty = difficulty

    def set_difficulty(self):
        self.difficulty = int(request.form['difficulty'])

    def play(self):
        pass


class GuessGame(Game):
    def __init__(self):
        super().__init__("Number Guess Game")

    def play(self) -> str:
        secret = str(random.randint(1, self.difficulty))
        guess = request.form['guess']
        if secret == guess:
            return f"You guessed the same as the PC ({secret})"
        result = f"You guessed wrong, the number was {secret}"
        return result


class MemoryGame(Game):
    def __init__(self):
        super().__init__("Memory Game")

    def play(self):
        difficulty = self.difficulty
        user_input = []
        # getting the user inputs per each number in the generated sequence
        for i in range(1, difficulty+1):
            user_input.append(int(request.form[f'user_input_{i}']))
        gen_seq = request.form['sequence']
        # Turning the generated sequence to a real list and not a string
        parsed_seq = ast.literal_eval(gen_seq)
        sequence = [int(item) for item in parsed_seq if isinstance(item, int)]
        return sequence == user_input, sequence


class CurrGame(Game):
    def __init__(self):
        super().__init__("Currency Game")

    def get_money_interval(self, amount_usd):
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        exchange_rates = response.json()["rates"]
        rate_to_ils = exchange_rates["ILS"]  # 3.61
        lower_bound = amount_usd - (5 - self.difficulty)
        upper_bound = amount_usd + (5 - self.difficulty)
        lower_bound_ils = round(lower_bound * rate_to_ils)
        upper_bound_ils = round(upper_bound * rate_to_ils)
        exact_answer = amount_usd * rate_to_ils

        return lower_bound_ils, upper_bound_ils, exact_answer

    def play(self):
        difficulty = self.difficulty
        amount_usd = float(request.form["amount_usd"])
        lower_interval, upper_interval, exact_answer = self.get_money_interval(amount_usd=amount_usd)
        guess = float(request.form['guess'])
        exact_answer = round(exact_answer, 2)
        if lower_interval <= guess <= upper_interval:
            return True, exact_answer
        else:
            return False, exact_answer
