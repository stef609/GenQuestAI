"""LLM Agent module for playing Zork via Ollama."""

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage


class ZorkAgent:
    """Agent that uses Ollama LLM to play Zork."""

    SYSTEM_PROMPT = """You are an expert player of the text adventure ZORK. 
    Your objective: maximize score by collecting treasures and solving puzzles.

OPERATIONAL RULES:
1. RESPONSE FORMAT: Output ONLY the command. No quotes, no explanations.
2. SYNTAX: Use 1-3 word commands (e.g., "WEST", "TAKE LAMP", "OPEN WINDOW").
3. NAVIGATION STRATEGY: 
   - If a direction is blocked or leads nowhere, try every other compass point (N, S, E, W, NE, NW, SE, SW, UP, DOWN).
   - To enter the White House: You cannot enter through the front door. You must go EAST or WEST to reach the BEHIND HOUSE area, then OPEN WINDOW and ENTER.
4. LOOP PREVENTION: 
   - Never repeat the exact same command twice in a row if the game state hasn't changed.
   - If you have tried all cardinal directions in a room, try "OPEN", "MOVE", or "LOOK AT" specific objects mentioned in the description.
5. OBJECT HANDLING:
   - Always "TAKE" any portable object you find.
   - if you see multiple objects, take them all (one at a time).
   - "EXAMINE" or "READ" new objects immediately to find clues.
   - "I" (Inventory) only if you forget what you are carrying.
6. STUCK PROTOCOL: 
   - If you are in a forest/up a tree and cannot move, go "DOWN" then "EAST" to return to the clearing.
   - If you see a passage, try to enter into it
   - if you see stairs, try to go upstairs then move another direction, or downstairs then take another direction
   - if you see a door try to open it

Respond with your first move.

SUMMARY FROM PREVIOUS RUN TO USE AS CONTEXT FOR IMPROVEMENT:
I was unable to collect any treasures or solve puzzles due to an impasse in the vertical movement. The only 
command that worked was "DOWN", but it led to a dead-end with a locked grating. After 20 iterations, no progress could be made 
beyond this point. I should have tried alternative navigation strategies, such as going east-west instead of north-south, or 
examining objects more closely for hidden clues. To improve performance in the next session, I will prioritize exploring different 
directions and examining objects to uncover potential solutions.

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
    
    def create_summary(self, final_output: str, iterations_used: int) -> str:
        """Create a summary of the game session for future reference.

        Args:
            final_output: The final output from the game
            iterations_used: Number of iterations used in the session   
        Returns:
            A summary string to be used in the next game session
        """        
        summary_prompt = f"""Based on the final game output and the number of iterations used, create a concise summary of the key events, treasures collected, puzzles solved, and any important locations visited during this Zork session. The summary should be no more than 5 sentences and should highlight the most significant achievements and challenges faced. This summary will be provided at the start of the next game session to help improve performance and strategy.
Final game output: {final_output}
Iterations used: {iterations_used}
"""
        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=summary_prompt),
        ]

        response = self.llm.invoke(messages)
        return response.content
