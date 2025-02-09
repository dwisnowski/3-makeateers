from flask_socketio import emit
from app.shared import games, question_bank


def register_handlers(socketio):
    @socketio.on('start_game')
    def start_game(data):
        """Start the game and send the first question."""
        game_code = data['game_code']
        print(f"Starting game: {game_code}")
        if game_code in games and question_bank:
            question = question_bank[0]
            print(f"Sending question: {question}")
            emit('new_question', question, room=game_code)