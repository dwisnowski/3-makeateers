from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
import sqlite3
import os
import importlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
Bootstrap(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize the database
def init_db():
    db_path = 'database.db'
    if os.path.exists(db_path):
        os.remove(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, text TEXT)''')
        conn.commit()

# Import all routes dynamically
def import_routes():
    from app.routes import register_blueprints
    register_blueprints(app)

# Import all socketio handlers dynamically
def import_socketio_handlers():
    socketio_dir = os.path.join(os.path.dirname(__file__), 'socketio')
    for filename in os.listdir(socketio_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f'app.socketio.{filename[:-3]}'
            importlib.import_module(module_name)

init_db()
import_routes()
import_socketio_handlers()