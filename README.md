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




# Project setup
uv init
.gitignore file


