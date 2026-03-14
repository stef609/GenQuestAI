"""Zork game interface module using pexpect."""

import re
from typing import Optional

import pexpect


class ZorkGame:
    """Interface to the Zork game process."""

    def __init__(self, game_path: str) -> None:
        """Initialize the Zork game interface.

        Args:
            game_path: Path to the Zork game executable
        """
        self.game_path = game_path
        self.process: Optional[pexpect.spawn] = None

    def start(self) -> str:
        """Start the Zork game and return initial output.

        Returns:
            Initial game text
        """
        self.process = pexpect.spawn(self.game_path, encoding="utf-8")
        self.process.expect([r">", pexpect.EOF])
        output = self._clean_output(self.process.before)
        return output

    def send_command(self, command: str) -> str:
        """Send a command to the game and return the response.

        Args:
            command: The command to send

        Returns:
            Game output response
        """
        if self.process is None:
            raise RuntimeError("Game not started. Call start() first.")

        # Truncate words to 6 characters (Zork parser rule)
        truncated_command = self._truncate_words(command)
        self.process.sendline(truncated_command)
        self.process.expect([r">", pexpect.EOF])
        return self._clean_output(self.process.before)

    def get_score(self) -> Optional[int]:
        """Get the current score by sending SCORE command.

        Returns:
            Current score or None if unable to parse
        """
        if self.process is None:
            return None

        self.process.sendline("SCORE")
        self.process.expect([r">", pexpect.EOF])
        output = self._clean_output(self.process.before)

        # Parse "Your score is X (total points Y)"
        match = re.search(r"Your score is (\d+)", output, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None

    def is_game_over(self, output: str) -> bool:
        """Check if the game has ended.

        Args:
            output: Game output to check

        Returns:
            True if game is over
        """
        output_lower = output.lower()
        game_over_phrases = [
            "you have died",
            "you have won",
            "do you wish to leave the game",
            "your score is",
            "final score",
        ]
        return any(phrase in output_lower for phrase in game_over_phrases)

    def close(self) -> None:
        """Terminate the game process."""
        if self.process is not None:
            self.process.terminate()
            self.process = None

    def _clean_output(self, output: Optional[str | bytes]) -> str:
        """Clean raw output from pexpect.

        Args:
            output: Raw output string or bytes

        Returns:
            Cleaned output string
        """
        if output is None:
            return ""
        # Convert bytes to str if needed
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        # Remove carriage returns
        return output.replace("\r", "").strip()

    def _truncate_words(self, command: str) -> str:
        """Truncate words to 6 characters per Zork parser rules.

        Args:
            command: Original command

        Returns:
            Command with words truncated to 6 chars
        """
        words = command.split()
        truncated = [word[:6] for word in words]
        return " ".join(truncated)
