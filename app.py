from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
import sqlite3

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


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
