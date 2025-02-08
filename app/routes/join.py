from flask import Blueprint, render_template

join_bp = Blueprint('join', __name__)

@join_bp.route('/join')
def join():
    return render_template('game_join.html')  # Player login page