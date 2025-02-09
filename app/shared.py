import os
import importlib

games = {}

# Function to dynamically load question modules
def load_questions():
    question_bank = {
        "general": [],
        "parks": {}
    }

    # Load general questions
    general_module = importlib.import_module('app.shared.general')
    question_bank["general"] = general_module.general_questions

    # Load park-specific questions
    parks_dir = os.path.join(os.path.dirname(__file__), 'shared')
    for park_name in os.listdir(parks_dir):
        park_path = os.path.join(parks_dir, park_name)
        if os.path.isdir(park_path) and park_name != '__pycache__':
            question_bank["parks"][park_name] = {"rides": {}}
            rides_dir = os.path.join(park_path, 'rides')
            if os.path.exists(rides_dir):
                for ride_name in os.listdir(rides_dir):
                    if ride_name.endswith('.py') and ride_name != '__init__.py':
                        ride_module_name = f'app.shared.{park_name}.rides.{ride_name[:-3]}'
                        ride_module = importlib.import_module(ride_module_name)
                        question_bank["parks"][park_name]["rides"][ride_name[:-3]] = ride_module.questions

    return question_bank

question_bank = load_questions()




