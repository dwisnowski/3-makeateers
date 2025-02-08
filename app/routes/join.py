from flask import Blueprint, render_template

bp = Blueprint('join', __name__)

@bp.route('/game/join')
def join():
    return render_template('game_join.html')  # Player login page