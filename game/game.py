from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import random

app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store game sessions
games = {}


@socketio.on('create_game')
def create_game():
    """Host creates a new game session."""
    game_code = str(random.randint(1000, 9999))  # Generate a 4-digit game code
    games[game_code] = {'players': {}, 'questions': [], 'current_question': 0}
    emit('game_created', {'game_code': game_code})

@socketio.on('join_game')
def join_game(data):
    """Player joins an existing game."""
    game_code = data['game_code']
    username = data['username']
    
    if game_code in games:
        games[game_code]['players'][username] = {'score': 0}
        join_room(game_code)
        emit('player_joined', {'username': username}, room=game_code)
        emit('join_success', {'game_code': game_code})
    else:
        emit('error', {'message': 'Game not found'})

@socketio.on('start_game')
def start_game(data):
    """Start the game and send the first question."""
    game_code = data['game_code']
    if game_code in games and games[game_code]['questions']:
        question = games[game_code]['questions'][0]
        emit('new_question', {'question': question}, room=game_code)

@socketio.on('submit_answer')
def submit_answer(data):
    """Handle answer submission and update scores."""
    game_code = data['game_code']
    username = data['username']
    answer = data['answer']

    # Dummy answer check (replace with actual logic)
    correct_answer = "A"  # Change to match your question data
    if answer == correct_answer:
        games[game_code]['players'][username]['score'] += 10
    
    # Send updated leaderboard
    leaderboard = {player: info['score'] for player, info in games[game_code]['players'].items()}
    emit('update_leaderboard', leaderboard, room=game_code)

@socketio.on('next_question')
def next_question(data):
    """Send the next question to players."""
    game_code = data['game_code']
    game = games.get(game_code, None)
    
    if game and game['current_question'] + 1 < len(game['questions']):
        game['current_question'] += 1
        question = game['questions'][game['current_question']]
        emit('new_question', {'question': question}, room=game_code)
    else:
        emit('game_over', {}, room=game_code)

if __name__ == '__main__':
    socketio.run(app, debug=True)
