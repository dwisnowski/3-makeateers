from flask import jsonify
import sqlite3

def get_messages():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM messages')
        messages = [{'id': row[0], 'text': row[1]} for row in cursor.fetchall()]
    return jsonify(messages)