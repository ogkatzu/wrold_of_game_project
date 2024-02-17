from flask import Flask, render_template, request
import games
import random

app = Flask(__name__)


def generate_sequence(difficulty):
    sequence = [random.randint(1, 101) for _ in range(difficulty)]
    return sequence


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/play-guess-game', methods=['GET'])
def page_guess_game():
    difficulty = request.args.get('difficulty')
    return render_template('guess-game.html', difficulty=difficulty)


@app.route("/guess-game", methods=['POST'])
def play_guess_game():
    guess_game = games.GuessGame()
    guess_game.set_difficulty()
    result = guess_game.play()
    difficulty = request.form['difficulty']
    return render_template('guess-game.html', result=result, difficulty=difficulty)


@app.route("/play-memory-game", methods=["get"])
def page_memory_game():
    difficulty = int(request.args.get('difficulty'))
    seq = generate_sequence(int(difficulty))
    return render_template("memory-game.html", difficulty=difficulty, sequence=seq)


@app.route("/memory-game", methods=["POST"])
def play_memory_game():
    memory_game = games.MemoryGame()
    memory_game.set_difficulty()
    result = memory_game.play()
    difficulty = int(request.form['difficulty'])
    return render_template("memory-game-result.html", result=result, difficulty=difficulty)


@app.route("/play-curr-game", methods=["GET"])
def page_curr_game():
    difficulty = request.args.get("difficulty")
    amount_usd = random.randint(1, 100)  # Random amount in USD
    return render_template('currency-game.html', difficulty=difficulty, amount_usd=amount_usd)


@app.route("/currency-game", methods=["GET", "POST"])
def play_curr_game():
    game = games.CurrGame()
    game.set_difficulty()
    amount = request.form['amount_usd']
    result = game.play()
    return render_template("currency-game-result.html", result=result, amount_usd=amount)


if __name__ == "__main__":
    app.run(debug=True)
