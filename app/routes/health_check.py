from flask import jsonify

def health_check():
    return jsonify({'status': 'healthy'}), 200