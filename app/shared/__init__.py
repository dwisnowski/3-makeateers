from .general import general_questions
from .magic_kingdom.space_mountain import space_mountain_questions

question_bank = {
    "general": general_questions,
    "parks": {
        "magic_kingdom": {
            "rides": {
                "space_mountain": space_mountain_questions
            }
        }
    }
}