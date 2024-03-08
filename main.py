from flask import Flask, render_template, request
import games
import random
import sqlite3
USERNAME = games.USERNAME


def connect_to_db() -> None:
    """
    Connects to the database and creates a scores table if it does not exist.
    """
    conn = sqlite3.connect('score.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def get_user_score(username: str) -> list:
    """
    Function to retrieve the user's score from the 'score.db' database.
    Takes a username as input and returns the user's score as a list.
    """
    conn = sqlite3.connect('score.db')
    cursor = conn.cursor()
    cursor.execute('SELECT score FROM scores WHERE user = ?', (username,))  # (USERNAME)
    scores = cursor.fetchall()
    # Create a new row for the user if it doesn't exist and set the score to 0
    if not scores:
        conn.close()
        conn = sqlite3.connect('score.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO scores (user, score) VALUES (?, ?)', (username, 0))
        conn.commit()
        cursor.execute('SELECT score FROM scores WHERE user = ?', (username,))  # (USERNAME)
        scores = cursor.fetchall()
        # return scores[0][0]
    return scores[0][0]


app = Flask(__name__)

connect_to_db()


def generate_sequence(difficulty) -> list:
    sequence = [random.randint(1, 101) for _ in range(difficulty)]
    return sequence


@app.route("/", methods=["GET"])
def index():
    score = get_user_score(username=USERNAME)
    return render_template("index.html", score=score)


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
