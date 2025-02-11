from flask_socketio import emit
from app.shared.general import questions as general_questions
from app.shared.parks.magic_kingdom.rides import space_mountain
from app.shared.parks.hollywood_studios.rides import the_twilight_zone_tower_of_terror, rock_n_roller_coaster_starring_aerosmith, millennium_falcon_smugglers_run, star_wars_rise_of_the_resistance, slinky_dog_dash
from app.shared.parks.epcot.rides import guardians_of_the_galaxy_cosmic_rewind, test_track

# Dictionary to map parks and rides to their respective question banks
question_groups = {
    "general": general_questions,
    "magic_kingdom": {
        "space_mountain": space_mountain.questions
    },
    "hollywood_studios": {
        "the_twilight_zone_tower_of_terror": the_twilight_zone_tower_of_terror.questions,
        "rock_n_roller_coaster_starring_aerosmith": rock_n_roller_coaster_starring_aerosmith.questions,
        "millennium_falcon_smugglers_run": millennium_falcon_smugglers_run.questions,
        "star_wars_rise_of_the_resistance": star_wars_rise_of_the_resistance.questions,
        "slinky_dog_dash": slinky_dog_dash.questions
    },
    "epcot": {
        "guardians_of_the_galaxy_cosmic_rewind": guardians_of_the_galaxy_cosmic_rewind.questions,
        "test_track": test_track.questions
    }
}

def register_handlers(socketio):
    @socketio.on('start_game')
    def start_game(data):
        """Start the game and send the first question."""
        game_code = data['game_code']
        park = data['park']
        ride = data['ride']
        
        # Get the question bank based on the selected park and ride
        if park == "general":
            question_bank = question_groups.get("general")
        else:
            question_bank = question_groups.get(park, {}).get(ride)
        
        # Ensure the question_bank is not empty and contains questions
        if question_bank and len(question_bank) > 0:
            question = question_bank[0]
            emit('new_question', question, room=game_code)
        else:
            emit('error', {'message': 'No questions available for the selected park and ride'}, room=game_code)