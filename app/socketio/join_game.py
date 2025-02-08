from flask_socketio import emit, join_room
from app.shared import games
from app import socketio

@socketio.on('join_game')
def join_game(data):
    """Player joins an existing game session."""
    game_code = data['game_code']
    username = data['username']
    
    if game_code in games:
        games[game_code]['players'][username] = {'score': 0}
        join_room(game_code)
        emit('player_joined', {'username': username}, room=game_code)
        emit('join_success', {'game_code': game_code})
    else:
        emit('error', {'message': 'Game not found'})