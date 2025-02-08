from flask import request, jsonify
import sqlite3

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