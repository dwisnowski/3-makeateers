from flask import request, jsonify, Blueprint
import sqlite3

add_message_bp = Blueprint('add_message', __name__)

@add_message_bp.route('/add_message')
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