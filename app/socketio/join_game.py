from flask_socketio import emit, join_room
from app import games, socketio

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