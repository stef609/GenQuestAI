"""Main entry point for GenQuestAI."""

from src.config import Settings
from src.runner import GameRunner


def main() -> None:
    """Run the GenQuestAI application."""
    settings = Settings()
    runner = GameRunner(settings)
    runner.run()


if __name__ == "__main__":
    main()
