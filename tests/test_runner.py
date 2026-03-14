"""Tests for game runner module."""

from unittest.mock import MagicMock, patch

import pytest

from src.runner import GameRunner


class TestGameRunnerInit:
    """Test runner initialization."""

    def test_runner_stores_settings(self):
        """Test settings are stored."""
        mock_settings = MagicMock()
        mock_settings.max_iterations = 50
        mock_settings.verbose = True

        runner = GameRunner(mock_settings)
        assert runner.settings == mock_settings


class TestGameRunnerRun:
    """Test the main game loop."""

    @patch("src.runner.ZorkGame")
    @patch("src.runner.ZorkAgent")
    @patch("src.runner.ProgressLogger")
    def test_run_starts_game(self, mock_logger_class, mock_agent_class, mock_game_class):
        """Test run starts the game."""
        mock_game = MagicMock()
        mock_game.start.return_value = "West of House"
        mock_game_class.return_value = mock_game

        mock_agent = MagicMock()
        mock_agent.get_next_command.return_value = "QUIT"
        mock_agent_class.return_value = mock_agent

        mock_logger = MagicMock()
        mock_logger_class.return_value = mock_logger

        mock_settings = MagicMock()
        mock_settings.max_iterations = 50
        mock_settings.verbose = True
        mock_settings.zork_game_path = "/usr/games/zork"
        mock_settings.ollama_model = "qwen2.5:14b"
        mock_settings.ollama_url = "http://localhost:11434"

        runner = GameRunner(mock_settings)
        runner.run()

        mock_game.start.assert_called_once()

    @patch("src.runner.ZorkGame")
    @patch("src.runner.ZorkAgent")
    @patch("src.runner.ProgressLogger")
    def test_run_creates_agent(self, mock_logger_class, mock_agent_class, mock_game_class):
        """Test run creates agent with correct settings."""
        mock_game = MagicMock()
        mock_game.start.return_value = "West of House"
        mock_game_class.return_value = mock_game

        mock_agent = MagicMock()
        mock_agent.get_next_command.return_value = "QUIT"
        mock_agent_class.return_value = mock_agent

        mock_logger = MagicMock()
        mock_logger_class.return_value = mock_logger

        mock_settings = MagicMock()
        mock_settings.max_iterations = 50
        mock_settings.verbose = True
        mock_settings.zork_game_path = "/usr/games/zork"
        mock_settings.ollama_model = "qwen2.5:14b"
        mock_settings.ollama_url = "http://localhost:11434"

        runner = GameRunner(mock_settings)
        runner.run()

        mock_agent_class.assert_called_once_with("qwen2.5:14b", "http://localhost:11434")

    @patch("src.runner.ZorkGame")
    @patch("src.runner.ZorkAgent")
    @patch("src.runner.ProgressLogger")
    def test_run_shows_start_header(self, mock_logger_class, mock_agent_class, mock_game_class):
        """Test run shows start header."""
        mock_game = MagicMock()
        mock_game.start.return_value = "West of House"
        mock_game_class.return_value = mock_game

        mock_agent = MagicMock()
        mock_agent.get_next_command.return_value = "QUIT"
        mock_agent_class.return_value = mock_agent

        mock_logger = MagicMock()
        mock_logger_class.return_value = mock_logger

        mock_settings = MagicMock()
        mock_settings.max_iterations = 50
        mock_settings.verbose = True

        runner = GameRunner(mock_settings)
        runner.run()

        mock_logger.show_start.assert_called_once()

    @patch("src.runner.ZorkGame")
    @patch("src.runner.ZorkAgent")
    @patch("src.runner.ProgressLogger")
    def test_run_shows_iterations(self, mock_logger_class, mock_agent_class, mock_game_class):
        """Test run shows iteration counter."""
        mock_game = MagicMock()
        mock_game.start.return_value = "West of House"
        mock_game.send_command.return_value = "North of House"
        mock_game_class.return_value = mock_game

        mock_agent = MagicMock()
        mock_agent.get_next_command.side_effect = ["NORTH", "QUIT"]
        mock_agent_class.return_value = mock_agent

        mock_logger = MagicMock()
        mock_logger_class.return_value = mock_logger

        mock_settings = MagicMock()
        mock_settings.max_iterations = 50
        mock_settings.verbose = True

        runner = GameRunner(mock_settings)
        runner.run()

        # Should show iteration 1
        mock_logger.show_iteration.assert_any_call(1, 50)

    @patch("src.runner.ZorkGame")
    @patch("src.runner.ZorkAgent")
    @patch("src.runner.ProgressLogger")
    def test_run_sends_command_to_game(self, mock_logger_class, mock_agent_class, mock_game_class):
        """Test run sends LLM command to game."""
        mock_game = MagicMock()
        mock_game.start.return_value = "West of House"
        mock_game.send_command.return_value = "North of House"
        mock_game_class.return_value = mock_game

        mock_agent = MagicMock()
        mock_agent.get_next_command.return_value = "NORTH"
        mock_agent_class.return_value = mock_agent

        mock_logger = MagicMock()
        mock_logger_class.return_value = mock_logger

        mock_settings = MagicMock()
        mock_settings.max_iterations = 50
        mock_settings.verbose = True

        runner = GameRunner(mock_settings)
        runner.run()

        mock_game.send_command.assert_called_with("NORTH")

    @patch("src.runner.ZorkGame")
    @patch("src.runner.ZorkAgent")
    @patch("src.runner.ProgressLogger")
    def test_run_stops_on_quit(self, mock_logger_class, mock_agent_class, mock_game_class):
        """Test run stops when agent sends QUIT."""
        mock_game = MagicMock()
        mock_game.start.return_value = "West of House"
        mock_game.send_command.return_value = "Goodbye!"
        mock_game_class.return_value = mock_game

        mock_agent = MagicMock()
        mock_agent.get_next_command.return_value = "QUIT"
        mock_agent_class.return_value = mock_agent

        mock_logger = MagicMock()
        mock_logger_class.return_value = mock_logger

        mock_settings = MagicMock()
        mock_settings.max_iterations = 50
        mock_settings.verbose = True

        runner = GameRunner(mock_settings)
        runner.run()

        # QUIT command breaks before sending to game, so send_command is not called
        assert mock_game.send_command.call_count == 0

    @patch("src.runner.ZorkGame")
    @patch("src.runner.ZorkAgent")
    @patch("src.runner.ProgressLogger")
    def test_run_stops_on_game_over(self, mock_logger_class, mock_agent_class, mock_game_class):
        """Test run stops when game reports game over."""
        mock_game = MagicMock()
        mock_game.start.return_value = "West of House"
        mock_game.send_command.return_value = "You have died"
        mock_game.is_game_over.return_value = True
        mock_game_class.return_value = mock_game

        mock_agent = MagicMock()
        mock_agent.get_next_command.return_value = "ATTACK TROLL"
        mock_agent_class.return_value = mock_agent

        mock_logger = MagicMock()
        mock_logger_class.return_value = mock_logger

        mock_settings = MagicMock()
        mock_settings.max_iterations = 50
        mock_settings.verbose = True

        runner = GameRunner(mock_settings)
        runner.run()

        mock_logger.show_game_ended.assert_called_once()

    @patch("src.runner.ZorkGame")
    @patch("src.runner.ZorkAgent")
    @patch("src.runner.ProgressLogger")
    def test_run_respects_max_iterations(self, mock_logger_class, mock_agent_class, mock_game_class):
        """Test run stops at max iterations."""
        mock_game = MagicMock()
        mock_game.start.return_value = "West of House"
        mock_game.send_command.return_value = "Room description"
        mock_game.is_game_over.return_value = False
        mock_game_class.return_value = mock_game

        mock_agent = MagicMock()
        mock_agent.get_next_command.return_value = "NORTH"
        mock_agent_class.return_value = mock_agent

        mock_logger = MagicMock()
        mock_logger_class.return_value = mock_logger

        mock_settings = MagicMock()
        mock_settings.max_iterations = 5
        mock_settings.verbose = True

        runner = GameRunner(mock_settings)
        runner.run()

        # Should run exactly 5 iterations
        assert mock_game.send_command.call_count == 5

    @patch("src.runner.ZorkGame")
    @patch("src.runner.ZorkAgent")
    @patch("src.runner.ProgressLogger")
    def test_run_shows_final_score(self, mock_logger_class, mock_agent_class, mock_game_class):
        """Test run shows final score."""
        mock_game = MagicMock()
        mock_game.start.return_value = "West of House"
        mock_game.send_command.return_value = "Room"
        mock_game.get_score.return_value = 350
        mock_game_class.return_value = mock_game

        mock_agent = MagicMock()
        mock_agent.get_next_command.return_value = "QUIT"
        mock_agent_class.return_value = mock_agent

        mock_logger = MagicMock()
        mock_logger_class.return_value = mock_logger

        mock_settings = MagicMock()
        mock_settings.max_iterations = 50
        mock_settings.verbose = True

        runner = GameRunner(mock_settings)
        runner.run()

        mock_game.get_score.assert_called_once()
        mock_logger.show_final_score.assert_called_once_with(350, 1)

    @patch("src.runner.ZorkGame")
    @patch("src.runner.ZorkAgent")
    @patch("src.runner.ProgressLogger")
    def test_run_closes_game_on_completion(self, mock_logger_class, mock_agent_class, mock_game_class):
        """Test run closes game when complete."""
        mock_game = MagicMock()
        mock_game.start.return_value = "West of House"
        mock_game.send_command.return_value = "Room"
        mock_game_class.return_value = mock_game

        mock_agent = MagicMock()
        mock_agent.get_next_command.return_value = "QUIT"
        mock_agent_class.return_value = mock_agent

        mock_logger = MagicMock()
        mock_logger_class.return_value = mock_logger

        mock_settings = MagicMock()
        mock_settings.max_iterations = 50
        mock_settings.verbose = True

        runner = GameRunner(mock_settings)
        runner.run()

        mock_game.close.assert_called_once()

    @patch("src.runner.ZorkGame")
    @patch("src.runner.ZorkAgent")
    @patch("src.runner.ProgressLogger")
    def test_run_closes_game_on_exception(self, mock_logger_class, mock_agent_class, mock_game_class):
        """Test run closes game even if exception occurs."""
        mock_game = MagicMock()
        mock_game.start.return_value = "West of House"
        mock_game.send_command.side_effect = Exception("Game crashed")
        mock_game_class.return_value = mock_game

        mock_agent = MagicMock()
        mock_agent.get_next_command.return_value = "NORTH"
        mock_agent_class.return_value = mock_agent

        mock_logger = MagicMock()
        mock_logger_class.return_value = mock_logger

        mock_settings = MagicMock()
        mock_settings.max_iterations = 50
        mock_settings.verbose = True

        runner = GameRunner(mock_settings)
        with pytest.raises(Exception):
            runner.run()

        mock_game.close.assert_called_once()
