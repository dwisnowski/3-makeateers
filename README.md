# 3-makeateers Project

This project is a Flask-based web application that allows users to participate in a game where they can rescue a horse named Starshine. The application features real-time interactions using SocketIO and provides a simple interface for players to join games, answer questions, and track scores.


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

## Features

- **Game Creation**: Hosts can create new game sessions with unique codes.
- **Player Joining**: Players can join existing games using the game code.
- **Real-time Interaction**: Players can answer questions and see real-time updates on scores and leaderboards.
- **Health Check**: A simple endpoint to check the health status of the application.
- **Scene Navigation**: Players can navigate through different scenes in the game, making choices that affect the outcome.

## Installation

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd 3-makeateers

1. Install the required packages and set up the virtual environment:
```sh
make install
```

Initialize the database:
```sh
make init-db
```

Run the application:
```sh
make run
```

## Usage
* Navigate to http://localhost:5000 in your web browser to access the home page.
* Follow the prompts to create or join a game and start playing!


## Clean Up
To clean up the virtual environment, run:
```sh
make clean
```

This project is licensed under the MIT License. See the LICENSE file for details.