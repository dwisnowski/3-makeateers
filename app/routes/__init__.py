from flask import Blueprint

routes_bp = Blueprint('routes', __name__)

from . import add_message, game, health_check, home, join, messages, scene