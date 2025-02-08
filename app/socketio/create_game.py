from flask_socketio import emit
import random
from app.shared import games

def register_handlers(socketio):
    @socketio.on('create_game')
    def create_game():
        print('Host is trying to create a game')
        """Host creates a new game session."""
        game_code = str(random.randint(1000, 9999))  # Generate a 4-digit game code
        games[game_code] = {'players': {}, 'questions': [], 'current_question': 0}
        print(f'Game {game_code} created')
        emit('game_created', {'game_code': game_code})