from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = "secret123"

wordList = {
    "easy": ["detox", "dough", "humor","mercy", "query"],
    "medium": ["storm", "yacht","suede", "visor","snoop", "swath"],
    "hard": ["cavalry", "parer","tares", "asterisk","defibrillator", "brewery"]
}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/start", methods=["GET", "POST"])
def start_game():
    if request.method == "POST":
        difficulty = request.form.get("difficulty", "easy")
        session["difficulty"] = difficulty
    else:
        difficulty = session.get("difficulty", "easy")

    word = random.choice(wordList[difficulty])
    session["word"] = word
    session["guessedWord"] = ["_"] * len(word)
    session["attempts"] = 10
    session["message"] = ""
    return redirect("/game")

@app.route("/game", methods=["GET", "POST"])
def game():
    if "word" not in session:
        return redirect("/")

    word = session["word"]
    guessedWord = session["guessedWord"]
    attempts = session["attempts"]
    message = session.get("message", "")

    if request.method == "POST":
        guess = request.form["guess"].lower()
        if guess in word:
            for i, letter in enumerate(word):
                if letter == guess:
                    guessedWord[i] = guess
            message = "Great guess!"
        else:
            attempts -= 1
            message = f"Wrong guess! Attempts left: {attempts}"

        session["guessedWord"] = guessedWord
        session["attempts"] = attempts
        session["message"] = message

        if "_" not in guessedWord:
            return redirect("/result/win")
        elif attempts == 0:
            return redirect("/result/lose")

    return render_template("game.html", guessedWord=' '.join(guessedWord),
                           attempts=attempts, message=message)

@app.route("/result/<result>")
def result(result):
    word = session.get("word", "")
    return render_template("result.html", result=result, word=word)

if __name__ == "__main__":
    app.run(debug=True)
