from flask_socketio import emit
from app.shared import question_bank


def register_handlers(socketio):
    # Load question groups
    @socketio.on('get_question_groups')
    def get_question_groups():
        question_groups = []

        # Get general questions
        if question_bank["general"]:
            question_groups.append("general")

        # Get park-specific questions
        for park_name, park_data in question_bank["parks"].items():
            for ride_name in park_data["rides"]:
                question_groups.append(f"{park_name} - {ride_name}")

        emit('question_groups', question_groups)
