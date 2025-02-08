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
    try:
        if os.path.exists(db_path):
            os.remove(db_path)
    except PermissionError:
        print(f"Warning: Could not remove {db_path} because it is being used by another process.")
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, text TEXT)''')
        conn.commit()

# Import all routes dynamically
def import_routes():
    routes_dir = os.path.join(os.path.dirname(__file__), 'routes')
    for filename in os.listdir(routes_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f'app.routes.{filename[:-3]}'
            module = importlib.import_module(module_name)
            if hasattr(module, 'bp'):
                app.register_blueprint(module.bp)

# Import all socketio handlers dynamically
def import_socketio_handlers(socketio):
    socketio_dir = os.path.join(os.path.dirname(__file__), 'socketio')
    for filename in os.listdir(socketio_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f'app.socketio.{filename[:-3]}'
            module = importlib.import_module(module_name)
            if hasattr(module, 'register_handlers'):
                module.register_handlers(socketio)

init_db()
import_routes()
import_socketio_handlers(socketio)