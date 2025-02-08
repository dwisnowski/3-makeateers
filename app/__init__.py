from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
Bootstrap(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize the database
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, text TEXT)''')
        conn.commit()

# Import routes
from app.routes import home, game, join, add_message, messages, health_check, scene

# Import socketio handlers
from app.socketio import create_game, join_game, start_game, submit_answer, next_question

init_db()