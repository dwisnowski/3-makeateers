from flask import Blueprint
import os
import importlib

routes_bp = Blueprint('routes', __name__)

def register_blueprints(app):
    routes_dir = os.path.dirname(__file__)
    for filename in os.listdir(routes_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f'app.routes.{filename[:-3]}'
            module = importlib.import_module(module_name)
            if hasattr(module, 'bp'):
                app.register_blueprint(module.bp)