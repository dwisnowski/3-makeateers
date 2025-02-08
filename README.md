# 3-makeateers Project

This project is a Flask-based web application that allows users to participate in a game where they can rescue a horse named Starshine. The application features real-time interactions using SocketIO and provides a simple interface for players to join games, answer questions, and track scores.

## Project Structure

```
3-makeateers
├── app
│   ├── __init__.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── add_message.py
│   │   ├── game.py
│   │   ├── health_check.py
│   │   ├── home.py
│   │   ├── join.py
│   │   ├── messages.py
│   │   └── scene.py
│   └── socketio
│       ├── __init__.py
│       ├── create_game.py
│       ├── join_game.py
│       ├── next_question.py
│       ├── start_game.py
│       └── submit_answer.py
├── templates
│   ├── game_host.html
│   ├── game_index.html
│   ├── game_join.html
│   ├── game_story.html
│   └── index.html
├── database.db
├── requirements.txt
└── README.md
```

## Features

- **Game Creation**: Hosts can create new game sessions with unique codes.
- **Player Joining**: Players can join existing games using the game code.
- **Real-time Interaction**: Players can answer questions and see real-time updates on scores and leaderboards.
- **Health Check**: A simple endpoint to check the health status of the application.
- **Scene Navigation**: Players can navigate through different scenes in the game, making choices that affect the outcome.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd 3-makeateers
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```
   python -c "from app import init_db; init_db()"
   ```

4. Run the application:
   ```
   python app/__init__.py
   ```

## Usage

- Navigate to `http://localhost:5000` in your web browser to access the home page.
- Follow the prompts to create or join a game and start playing!

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.