from flask import jsonify, Blueprint
import sqlite3

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages')
def messages():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM messages')
        messages = [{'id': row[0], 'text': row[1]} for row in cursor.fetchall()]
    return jsonify(messages)