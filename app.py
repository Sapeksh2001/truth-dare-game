# app.py
from flask import Flask, render_template, request, redirect, session, url_for
import random
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with secure key in production

# Load prompts
def load_prompts(file):
    with open(file, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

truths = load_prompts('truth.txt')
dares = load_prompts('dare.txt')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        players = request.form.getlist('players')
        session['players'] = players
        session['turn'] = 0
        return redirect(url_for('game'))
    return render_template('index.html')

@app.route('/game')
def game():
    players = session.get('players', [])
    if not players:
        return redirect(url_for('index'))
    turn = session.get('turn', 0)
    current = players[turn % len(players)]
    return render_template('game.html', player=current)

@app.route('/spin/<choice>')
def spin(choice):
    if choice == 'truth':
        prompt = random.choice(truths)
    elif choice == 'dare':
        prompt = random.choice(dares)
    else:
        prompt = random.choice(truths + dares)
    session['turn'] += 1
    return {'prompt': prompt}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
