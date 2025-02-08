from flask import render_template, Blueprint

bp = Blueprint('game_participant', __name__)

@bp.route('/game/participant')
def game():
    return render_template('game_participant.html')  # Home page for host