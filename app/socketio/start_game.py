from flask_socketio import emit
from app.shared import games


def register_handlers(socketio):
    @socketio.on('start_game')
    def start_game(data):
        """Start the game and send the first question."""
        game_code = data['game_code']
        if game_code in games and games[game_code]['questions']:
            question = games[game_code]['questions'][0]
            emit('new_question', {'question': question}, room=game_code)