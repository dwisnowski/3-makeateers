from flask import render_template, Blueprint

bp = Blueprint('game', __name__)

@bp.route('/game')
def game():
    return render_template('game_host.html')  # Home page for host