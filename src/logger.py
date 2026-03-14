"""Progress logger module for displaying game state."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class ProgressLogger:
    """Logger for displaying game progress and output."""

    def __init__(self, verbose: bool = True):
        """Initialize the logger.

        Args:
            verbose: Whether to show full game output
        """
        self.verbose = verbose
        self.console = Console()

    def show_start(self) -> None:
        """Display the game start header."""
        title = Text("GenQuestAI - Zork LLM Player", style="bold cyan")
        self.console.print(Panel(title, border_style="cyan"))

    def show_iteration(self, iteration: int, max_iterations: int) -> None:
        """Display the current iteration counter.

        Args:
            iteration: Current iteration number
            max_iterations: Maximum number of iterations
        """
        self.console.print()
        separator = "═" * 67
        self.console.print(f"[bold blue]{separator}[/]")
        self.console.print(
            f"[bold yellow][Iteration {iteration}/{max_iterations}][/]"
        )

    def show_command(self, command: str) -> None:
        """Display the LLM's chosen command.

        Args:
            command: The command to display
        """
        self.console.print(f"[bold green]> LLM Command: {command}[/]")
        self.console.print()

    def show_game_output(self, output: str) -> str:
        """Display the game output.

        Args:
            output: The text output from the game

        Returns:
            The displayed output
        """
        if not output:
            return ""

        if self.verbose:
            self.console.print(output)
            return output
        else:
            # Show first few lines when not verbose
            lines = output.split("\n")
            truncated = "\n".join(lines[:10])
            if len(lines) > 10:
                truncated += "\n..."
            self.console.print(truncated)
            return truncated

    def show_game_ended(self) -> None:
        """Display game ended message."""
        self.console.print()
        self.console.print("[bold red]Game ended.[/]")

    def show_final_score(self, score: int, iterations_used: int) -> None:
        """Display the final score and statistics.

        Args:
            score: Final score achieved
            iterations_used: Number of iterations used
        """
        self.console.print()
        separator = "═" * 67
        self.console.print(f"[bold green]{separator}[/]")
        self.console.print(f"[bold green][COMPLETE] Final Score: {score}[/]")
        self.console.print(
            f"[bold green][COMPLETE] Game completed in {iterations_used} iterations[/]"
        )

    def show_separator(self) -> None:
        """Display a separator line."""
        self.console.print("─" * 67, style="dim")
