from flask import render_template
from app import app

@app.route('/game')
def index():
    return render_template('game_host.html')  # Home page for host