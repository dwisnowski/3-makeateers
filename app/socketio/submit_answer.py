from flask_socketio import emit
from app.shared import games
from app import socketio

@socketio.on('submit_answer')
def submit_answer(data):
    """Handle answer submission and update scores."""
    game_code = data['game_code']
    username = data['username']
    answer = data['answer']

    correct_answer = "A"  # Change to match your question data
    if answer == correct_answer:
        games[game_code]['players'][username]['score'] += 10
    
    leaderboard = {player: info['score'] for player, info in games[game_code]['players'].items()}
    emit('update_leaderboard', leaderboard, room=game_code)