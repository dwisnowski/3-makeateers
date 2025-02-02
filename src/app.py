from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, text TEXT)''')
        conn.commit()

@app.route('/')
def home():
    return "Hello, World! This is your Flask app."

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

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
