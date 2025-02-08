from flask import jsonify, Blueprint

bp = Blueprint('health_check', __name__)

@bp.route('/health_check')
def health_check():
    return jsonify({'status': 'healthy'}), 200