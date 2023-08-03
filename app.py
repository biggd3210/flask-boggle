from flask import Flask, request, redirect, render_template, flash, jsonify, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)
boggle_game = Boggle()

@app.route("/")
def show_homepage():
    """Displays starting page."""
    return render_template("home.html")

@app.route("/game-start")
def begin_game():
    """initiates session and stores current boggle board."""
    boggle_board = boggle_game.make_board()
    session['boggle-board'] = boggle_board
    return redirect('/game-play')

@app.route('/game-play')
def display_board():
    """displays boggle board and user interaction to allow game play"""
    boggle_board = session['boggle-board']
    
    return render_template('boggle.html', boggle_board=boggle_board)

@app.route('/check-word', methods=["GET", "POST"])
def check_word():
    """checks word from user input against words.py and verifies it is on the board."""

    data = request.get_json()
    boggle_board = session['boggle-board']
    word = data['word']
    
    word_response = boggle_game.check_valid_word(boggle_board, word)

    msg = {
        'result': word_response,
        'word': word
        }
    
    return jsonify(msg)

@app.route("/log-stats", methods=["POST"])
def log_stats():
    """sets cookies for users stats."""
    score = int(request.json['score'])
    highscore = session.get('highscore', 0)
    plays = session.get('plays', 0)

    session['plays'] = plays + 1
    session['highscore'] = max(score, highscore)
    

    return jsonify(brokeRecord=score > highscore)