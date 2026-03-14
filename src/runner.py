"""Game runner module that orchestrates the Zork LLM player."""

from src.config import Settings
from src.game import ZorkGame
from src.agent import ZorkAgent
from src.logger import ProgressLogger


class GameRunner:
    """Orchestrates the game loop between Zork and the LLM agent."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the game runner.

        Args:
            settings: Application settings
        """
        self.settings = settings

    def run(self) -> None:
        """Run the main game loop."""
        # Initialize components
        logger = ProgressLogger(verbose=self.settings.verbose)
        game = ZorkGame(self.settings.zork_game_path)
        agent = ZorkAgent(self.settings.ollama_model, self.settings.ollama_url)

        try:
            # Show start header
            logger.show_start()

            # Start game and get initial output
            output = game.start()
            logger.show_game_output(output)

            # Main game loop
            iterations_used = 0
            for iteration in range(1, self.settings.max_iterations + 1):
                iterations_used = iteration
                logger.show_iteration(iteration, self.settings.max_iterations)

                # Get command from LLM
                command = agent.get_next_command(output, iteration)
                logger.show_command(command)

                # Check for quit command
                if command.upper() in ("QUIT", "Q"):
                    break

                # Send command to game
                output = game.send_command(command)
                logger.show_game_output(output)

                # Check if game is over
                if game.is_game_over(output):
                    logger.show_game_ended()
                    break

            # Get and display final score
            final_score = game.get_score()
            if final_score is None:
                final_score = 0
            logger.show_final_score(final_score, iterations_used)

        finally:
            # Always close the game process
            game.close()
