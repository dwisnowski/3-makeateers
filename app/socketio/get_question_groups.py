import importlib
import os
from flask_socketio import emit

# Base directory for shared parks
BASE_DIR = 'app/shared/parks'

def get_question_banks():
    question_groups = {}
    for park in os.listdir(BASE_DIR):
        park_path = os.path.join(BASE_DIR, park)
        if os.path.isdir(park_path):
            question_groups[park] = {}
            rides_path = os.path.join(park_path, 'rides')
            if os.path.isdir(rides_path):
                for ride in os.listdir(rides_path):
                    if ride.endswith('.py') and ride != '__init__.py':
                        ride_name = ride[:-3]
                        module_path = f'app.shared.parks.{park}.rides.{ride_name}'
                        module = importlib.import_module(module_path)
                        if hasattr(module, 'questions'):
                            question_groups[park][ride_name] = getattr(module, 'questions')
    return question_groups

def register_handlers(socketio):
    @socketio.on('get_question_groups')
    def get_question_groups():
        """Send the list of question groups to the client."""
        question_groups = get_question_banks()
        groups = []
        for park, rides in question_groups.items():
            for ride in rides:
                groups.append({"park": park, "ride": ride})
        emit('question_groups', groups)
