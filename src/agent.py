"""LLM Agent module for playing Zork via Ollama."""

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage


class ZorkAgent:
    """Agent that uses Ollama LLM to play Zork."""

    SYSTEM_PROMPT = """You are playing Zork, a classic text adventure game.

Your goal is to explore the world, solve puzzles, collect treasures, and maximize your score.

Game mechanics:
- Only the first 6 letters of each word are significant (DISASS = DISASSEMBLE)
- Commands: NORTH/N, SOUTH/S, EAST/E, WEST/W, UP, DOWN
- Actions: TAKE/DROP <item>, INVENTORY/I, LOOK/L, OPEN/CLOSE <object>
- Combat: ATTACK <enemy> WITH <weapon>

Respond ONLY with the command to send to the game. No explanation, no quotes.
Examples of valid responses:
- NORTH
- TAKE LAMP
- OPEN MAILBOX
- ATTACK TROLL WITH SWORD

Current game output:"""

    def __init__(self, model_name: str, ollama_url: str) -> None:
        """Initialize the Zork agent.

        Args:
            model_name: Name of the Ollama model to use
            ollama_url: URL of the Ollama API
        """
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.llm = ChatOllama(
            model=model_name,
            base_url=ollama_url,
            temperature=0.7,
        )

    def get_next_command(self, game_output: str, iteration: int) -> str:
        """Get the next command from the LLM based on game output.

        Args:
            game_output: Current output from the game
            iteration: Current iteration number

        Returns:
            The command to send to the game
        """
        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=f"{game_output}\n\nIteration: {iteration}\nYour command:"),
        ]

        response = self.llm.invoke(messages)
        command = self._clean_command(response.content)
        return command

    def _clean_command(self, raw_command: str) -> str:
        """Clean and normalize the command from LLM.

        Args:
            raw_command: Raw command from LLM

        Returns:
            Cleaned command ready for Zork
        """
        if not raw_command:
            return ""

        # Remove quotes
        command = raw_command.strip().strip('"\'')

        # Extract last line if multiline
        if "\n" in command:
            command = command.split("\n")[-1].strip()

        # Remove common prefixes
        prefixes = ["command:", "action:", "i will", "i should"]
        for prefix in prefixes:
            if command.lower().startswith(prefix):
                command = command[len(prefix):].strip()

        # Uppercase the command
        command = command.upper()

        return command
