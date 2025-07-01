# app.py
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import random
import os
import string

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# In-memory room storage
rooms = {}

# Load prompts

def load_prompts(file):
    with open(file, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

truths = load_prompts('truth.txt')
dares = load_prompts('dare.txt')

# Generate 4-digit room code
def generate_room_code():
    while True:
        code = ''.join(random.choices(string.digits, k=4))
        if code not in rooms:
            return code

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/create-room', methods=['POST'])
def create_room():
    name = request.form.get('name')
    code = generate_room_code()
    rooms[code] = {
        'host': name,
        'players': [name],
        'turn': 0,
        'played_this_round': set()
    }
    session['room_code'] = code
    session['name'] = name
    return redirect(url_for('room', code=code))

@app.route('/join-room', methods=['POST'])
def join_room():
    name = request.form.get('name')
    code = request.form.get('room_code')
    if code not in rooms:
        return f"Room {code} not found.", 404
    if name in rooms[code]['players']:
        return f"Name '{name}' already taken in room {code}.", 400
    rooms[code]['players'].append(name)
    session['room_code'] = code
    session['name'] = name
    return redirect(url_for('room', code=code))

@app.route('/room/<code>')
def room(code):
    if code not in rooms:
        return f"Room {code} does not exist.", 404
    name = session.get('name')
    if not name or name not in rooms[code]['players']:
        return redirect(url_for('home'))
    current_turn = rooms[code]['players'][rooms[code]['turn'] % len(rooms[code]['players'])]
    return render_template('game_room.html', code=code, player=name, current=current_turn)

@app.route('/spin/<code>/<choice>', methods=['POST'])
def spin(code, choice):
    name = session.get('name')
    if not name or code not in rooms or name not in rooms[code]['players']:
        return jsonify({"error": "Unauthorized"}), 403

    room = rooms[code]
    if name != room['players'][room['turn'] % len(room['players'])]:
        return jsonify({"error": "Not your turn"}), 403

    if name in room['played_this_round']:
        return jsonify({"error": "Already played this round"}), 403

    if choice == 'truth':
        prompt = random.choice(truths)
    elif choice == 'dare':
        prompt = random.choice(dares)
    else:
        prompt = random.choice(truths + dares)

    room['played_this_round'].add(name)

    # If all have played, reset and move to next round
    if len(room['played_this_round']) >= len(room['players']):
        room['played_this_round'].clear()
        room['turn'] = (room['turn'] + 1) % len(room['players'])

    return jsonify({"prompt": prompt})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
