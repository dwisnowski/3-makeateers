from flask_socketio import emit
from .. import games

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