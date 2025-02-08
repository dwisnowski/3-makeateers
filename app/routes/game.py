from flask import render_template, Blueprint

game_bp = Blueprint('game', __name__)

@game_bp.route('/game')
def game():
    return render_template('game_host.html')  # Home page for host