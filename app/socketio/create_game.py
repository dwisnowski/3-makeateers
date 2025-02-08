from flask_socketio import emit
import random
from app.shared import games
from app import socketio

@socketio.on('create_game')
def create_game():
    """Host creates a new game session."""
    game_code = str(random.randint(1000, 9999))  # Generate a 4-digit game code
    games[game_code] = {'players': {}, 'questions': [], 'current_question': 0}
    emit('game_created', {'game_code': game_code})