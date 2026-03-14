# GenQuestAI
The goal is to create an Application for letting LLMs play text adventure games like Zork by themselve.  The LLM will take the place of the human, interacting itself with the text interface of the game, and try to resolve the game, or have highest score as possible.
This project is initialy created to learn more

# Github project
https://github.com/stef609/GenQuestAI

# uv commands summary
uv python install 3.12 
    -> install python (inside uv -> different install as in system, enable to use multiple different versions easily)
uv init 
    -> init project for uv use
uv venv 
    -> creates a virtual env for the project
    uv venv --python 3.13 -> force using a specific python version
source /venv/bin/activate 
    -> activate the virtual env
uv add package 
    -> add dependencies in pyproject.toml
uv sync 
    -> sync packages with content of file pyproject.toml (if manual changes done in the file without using add command)
uv run main.py

# Ollama commands
ollama ps
ollama pull devstral-small-2
ollama launch claude --model devstral-small-2
ollama list
ollama show devstral-small-2
ollama launch claude --model kimi-k2.5:cloud

# Claude commands summary
# how to install it with local model using Ollama: 
# https://medium.com/@luongnv89/run-claude-code-on-local-cloud-models-in-5-minutes-ollama-openrouter-llama-cpp-6dfeaee03cda
# https://medium.com/@CodeCoup/how-to-run-claude-code-locally-100-free-fully-private-a9eb5845408e
/ide 
    -> Integrate claude in ide
/output_style 
    -> change output_style (detailed/learning/custom...)

# Project init
uv init
.gitignore file

# Summary

  Built a complete Zork-playing LLM agent with the following components:

  ┌─────────────────────┬───────────────┬───────┐
  │      Component      │     File      │ Tests │
  ├─────────────────────┼───────────────┼───────┤
  │ Configuration       │ src/config.py │ 17    │
  ├─────────────────────┼───────────────┼───────┤
  │ Logger              │ src/logger.py │ 14    │
  ├─────────────────────┼───────────────┼───────┤
  │ Zork Game Interface │ src/game.py   │ 20    │
  ├─────────────────────┼───────────────┼───────┤
  │ LLM Agent           │ src/agent.py  │ 13    │
  ├─────────────────────┼───────────────┼───────┤
  │ Game Runner         │ src/runner.py │ 12    │
  ├─────────────────────┼───────────────┼───────┤
  │ Total               │               │ 76    │
  └─────────────────────┴───────────────┴───────┘

# Project Structure

  src/
  ├── __init__.py
  ├── config.py      # Pydantic settings (max_iterations, ollama_model, etc.)
  ├── logger.py      # Rich console output for progress
  ├── game.py        # Zork process management via pexpect
  ├── agent.py       # Ollama LLM integration via LangChain
  ├── runner.py      # Main game loop orchestration
  └── main.py        # Entry point

  tests/
  ├── test_config.py    # Settings validation
  ├── test_logger.py    # Progress display
  ├── test_game.py      # Zork interface
  ├── test_agent.py     # LLM agent
  └── test_runner.py    # Game loop

# How to Run

  Prerequisites:
  - Zork installed (e.g., sudo apt install frotz)
  - Ollama running locally with a model pulled

  Run the application:
  uv run src/main.py

  Configure via environment variables:
  export MAX_ITERATIONS=100
  export OLLAMA_MODEL="qwen2.5:14b"
  export ZORK_GAME_PATH="/usr/games/zork"
  uv run src/main.py

  Run tests:
  uv run pytest tests/ -v

  The application will:
  1. Start Zork and display the initial room
  2. Loop up to max_iterations times:
    - Send game output to Ollama LLM
    - Get the LLM's chosen command
    - Send command to Zork
    - Display the result
  3. Stop on QUIT, game over, or max iterations
  4. Display final score


