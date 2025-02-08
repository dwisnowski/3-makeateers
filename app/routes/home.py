from flask import render_template, Blueprint
from app import app

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('index.html')