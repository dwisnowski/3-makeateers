from flask import Flask, request, jsonify, render_template, url_for, redirect, session
from flask_bootstrap import Bootstrap
import sqlite3
from flask_socketio import SocketIO, emit, join_room, leave_room
import random

app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store game sessions
games = {}

app = Flask(__name__)
Bootstrap(app)


# Game state, to keep track of user choices
game_state = {
    'current_scene': 'start',  # Starting point of the game
    'rescued': False  # Did the player rescue Starshine successfully?
}


def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, text TEXT)''')
        conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/game')
def index():
    return render_template('game_host.html')  # Home page for host

@app.route('/game/join')
def join():
    return render_template('game_join.html')  # Player login page

@app.route('/add', methods=['POST'])
def add_message():
    data = request.get_json()
    message = data.get('message')
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (text) VALUES (?)', (message,))
        conn.commit()
    
    return jsonify({'success': True, 'message': 'Message added!'})

@app.route('/messages', methods=['GET'])
def get_messages():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM messages')
        messages = [{'id': row[0], 'text': row[1]} for row in cursor.fetchall()]
    return jsonify(messages)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/horse_game')
def start_game():
    game_state['current_scene'] = 'start'
    return render_template('game_index.html')

@app.route('/horse_game/scene/<scene>', methods=['GET', 'POST'])
def scene(scene):
    game_state['current_scene'] = scene
    
    if scene == 'start':
        return render_template('game_story.html', story="You are standing in front of your house, looking at the neighborhood ranch. Starshine, the horse, is missing. The ranch is owned by a company known for mistreating animals. What will you do?", choices=[
            {'text': 'Visit the Ranch Office', 'route': 'office'},
            {'text': 'Talk to Neighbors', 'route': 'neighbors'},
            {'text': 'Investigate the Stables', 'route': 'stables'}
        ])
    
    elif scene == 'office':
        return render_template('game_story.html', story="You ask about Starshine at the ranch office, but the receptionist is nervous. The manager arrives and warns you to stay out of their business. What will you do?", choices=[
            {'text': 'Ask the Manager Directly', 'route': 'manager_confrontation'},
            {'text': 'Leave and Return Later', 'route': 'start'}
        ])
    
    elif scene == 'neighbors':
        return render_template('game_story.html', story="You ask the neighbors, and one mentions seeing a truck leaving the ranch late at night. It was headed toward the mountains. What will you do?", choices=[
            {'text': 'Follow the Truck\'s Path', 'route': 'mountains'},
            {'text': 'Visit the Local Market', 'route': 'market'}
        ])
    
    elif scene == 'stables':
        return render_template('game_story.html', story="You sneak into the ranch at night and overhear a conversation about selling horses. It looks like something shady is going on. What will you do?", choices=[
            {'text': 'Record the Conversation', 'route': 'record'},
            {'text': 'Confront the Buyers', 'route': 'confront'}
        ])
    
    # Add more scenes as needed, following the same pattern
    
    # For example:
    elif scene == 'manager_confrontation':
        return render_template('game_story.html', story="You confront the manager about Starshine. He gets angry and tells you to leave or face consequences. What will you do?", choices=[
            {'text': 'Leave and Return Later', 'route': 'start'},
            {'text': 'Threaten to Report Them', 'route': 'report'}
        ])
    
    elif scene == 'mountains':
        return render_template('game_story.html', story="You head toward the mountains, following the truck's path. You find a hidden barn. Inside, you spot Starshine. What will you do?", choices=[
            {'text': 'Sneak in at Night', 'route': 'sneak_in'},
            {'text': 'Alert the Authorities', 'route': 'authorities'}
        ])
    
    # Add ending scenarios as well
    elif scene == 'sneak_in':
        game_state['rescued'] = True
        return render_template('game_story.html', story="You successfully sneak in and rescue Starshine. You lead her to safety, and the two of you live happily ever after!", choices=[])

    elif scene == 'authorities':
        return render_template('game_story.html', story="You alert the authorities, who raid the ranch and rescue Starshine. The ranch is shut down, and you live happily with Starshine.", choices=[])

    return redirect(url_for('start_game'))

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
    init_db()
    app.run(host='0.0.0.0', port=5000)
    socketio.run(app, debug=True)
