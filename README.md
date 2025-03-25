# Triv-IA Pursuit

## Description
Triv-IA Pursuit is a trivia-based game inspired by the classic Trivial Pursuit. It is built using Streamlit and SQLModel, allowing players to answer questions from various themes, collect camemberts, and compete to win the game. The game supports multiple players and includes features like saving and loading games, a final test phase, and a visually interactive interface.

## Features
- **Multiplayer Support**: Add up to 6 players to compete in the game.
- **Thematic Questions**: Questions are categorized into themes such as Databases, Programming Languages, Unix Commands, AI News, DevOps, and Tech AI.
- **Camembert Collection**: Players collect camemberts by answering questions correctly.
- **Final Test**: A challenging final phase for players who collect all camemberts.
- **Save and Load Games**: Save your progress and resume the game later.
- **Interactive Dice Roll**: Simulates dice rolls with animations and sound effects.

## Directory Structure
```
raoufaddeche-brief_triv-ia_pursuit/
├── README.md
├── all_data.json
├── all_json.txt
├── controller.py
├── database_tester.py
├── database_utils.py
├── dump_questions.json
├── enums.py
├── init_db.py
├── json_handler.py
├── main.py
├── playermodels.py
├── positions.py
├── question_creation_tool.py
├── question_data.py
├── questionmodels.py
├── requirements.txt
├── save_game_tester.py
├── streamlit_functions.py
├── pictures/
│   └── dice/
├── positions/
├── sounds/
└── .streamlit/
    └── config.toml
```

## Installation
1. Clone the repository:
   ```bash
   git clone git@github.com:RaoufAddeche/Brief_Triv-IA_Pursuit.git
   cd raoufaddeche-brief_triv-ia_pursuit
   ```
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scriptsctivate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```bash
   streamlit run main.py
   ```
2. Use the interface to:
   - Add players.
   - Roll the dice and answer questions.
   - Save or load games.
3. Follow the on-screen instructions to play the game.

## Themes
The game includes the following themes:
- **Databases**
- **Programming Languages**
- **Unix Commands**
- **AI News**
- **DevOps**
- **Tech AI**

## Dependencies
- SQLModel==0.0.22
- Streamlit==1.41.1

## Notes
- Ensure that the `all_data.json` file is present in the project directory for the questions.
- The SQLite database file (`triv-IA_Pursuit.db`) will be created automatically.
- Images and sounds are stored in the `pictures/` and `sounds/` directories, respectively.

## License
This project is licensed under the MIT License.
