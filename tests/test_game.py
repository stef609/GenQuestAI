"""Tests for Zork game interface module."""

import re
from unittest.mock import MagicMock, patch

import pytest

from src.game import ZorkGame


class TestZorkGameInit:
    """Test game interface initialization."""

    def test_game_stores_game_path(self):
        """Test game path is stored."""
        game = ZorkGame("/usr/games/zork")
        assert game.game_path == "/usr/games/zork"

    def test_game_initializes_with_none_process(self):
        """Test process is None initially."""
        game = ZorkGame("/usr/games/zork")
        assert game.process is None


class TestZorkGameStart:
    """Test starting the game."""

    @patch("src.game.pexpect.spawn")
    def test_start_spawns_process(self, mock_spawn):
        """Test start spawns Zork process."""
        mock_process = MagicMock()
        mock_process.before = b"West of House\r\n"
        mock_process.after = b">"
        mock_spawn.return_value = mock_process

        game = ZorkGame("/usr/games/zork")
        game.start()

        mock_spawn.assert_called_once()
        assert game.process is not None

    @patch("src.game.pexpect.spawn")
    def test_start_returns_initial_output(self, mock_spawn):
        """Test start returns initial game text."""
        mock_process = MagicMock()
        mock_process.before = b"West of House\r\nYou are standing..."
        mock_process.after = b">"
        mock_spawn.return_value = mock_process

        game = ZorkGame("/usr/games/zork")
        output = game.start()

        assert "West of House" in output

    @patch("src.game.pexpect.spawn")
    def test_start_waits_for_prompt(self, mock_spawn):
        """Test start waits for Zork prompt."""
        mock_process = MagicMock()
        mock_process.before = b"Game text"
        mock_process.after = b">"
        mock_spawn.return_value = mock_process

        game = ZorkGame("/usr/games/zork")
        game.start()

        mock_process.expect.assert_called()


class TestZorkGameSendCommand:
    """Test sending commands."""

    @patch("src.game.pexpect.spawn")
    def test_send_command_sends_to_process(self, mock_spawn):
        """Test command is sent to process."""
        mock_process = MagicMock()
        mock_process.before = b"Room description"
        mock_spawn.return_value = mock_process

        game = ZorkGame("/usr/games/zork")
        game.start()
        game.send_command("NORTH")

        mock_process.sendline.assert_called_with("NORTH")

    @patch("src.game.pexpect.spawn")
    def test_send_command_returns_output(self, mock_spawn):
        """Test command returns game response."""
        mock_process = MagicMock()
        mock_process.before = b"North of House\r\nYou are here."
        mock_spawn.return_value = mock_process

        game = ZorkGame("/usr/games/zork")
        game.start()
        output = game.send_command("NORTH")

        assert "North of House" in output

    @patch("src.game.pexpect.spawn")
    def test_send_command_strips_carriage_returns(self, mock_spawn):
        """Test output strips \\r characters."""
        mock_process = MagicMock()
        mock_process.before = b"Line1\r\nLine2\r\n"
        mock_spawn.return_value = mock_process

        game = ZorkGame("/usr/games/zork")
        game.start()
        output = game.send_command("LOOK")

        assert "\r" not in output
        assert "Line1\nLine2" in output


class TestZorkGameGetScore:
    """Test score extraction."""

    @patch("src.game.pexpect.spawn")
    def test_get_score_parses_score_output(self, mock_spawn):
        """Test score extracted from game output."""
        mock_process = MagicMock()
        mock_process.before = b"Your score is 350 (total points 350)"
        mock_spawn.return_value = mock_process

        game = ZorkGame("/usr/games/zork")
        game.start()
        score = game.get_score()

        assert score == 350

    @patch("src.game.pexpect.spawn")
    def test_get_score_parses_zero_score(self, mock_spawn):
        """Test zero score is parsed."""
        mock_process = MagicMock()
        mock_process.before = b"Your score is 0 (total points 350)"
        mock_spawn.return_value = mock_process

        game = ZorkGame("/usr/games/zork")
        game.start()
        score = game.get_score()

        assert score == 0

    @patch("src.game.pexpect.spawn")
    def test_get_score_sends_score_command(self, mock_spawn):
        """Test SCORE command is sent."""
        mock_process = MagicMock()
        mock_process.before = b"Your score is 0"
        mock_spawn.return_value = mock_process

        game = ZorkGame("/usr/games/zork")
        game.start()
        game.get_score()

        mock_process.sendline.assert_called_with("SCORE")

    @patch("src.game.pexpect.spawn")
    def test_get_score_returns_none_on_parse_failure(self, mock_spawn):
        """Test None returned when score can't be parsed."""
        mock_process = MagicMock()
        mock_process.before = b"I don't know the word 'score'."
        mock_spawn.return_value = mock_process

        game = ZorkGame("/usr/games/zork")
        game.start()
        score = game.get_score()

        assert score is None


class TestZorkGameIsGameOver:
    """Test game over detection."""

    def test_detects_death(self):
        """Test death is detected."""
        game = ZorkGame("/usr/games/zork")
        assert game.is_game_over("You have died") is True

    def test_detects_death_lowercase(self):
        """Test death detection is case insensitive."""
        game = ZorkGame("/usr/games/zork")
        assert game.is_game_over("you have DIED") is True

    def test_detects_win(self):
        """Test win is detected."""
        game = ZorkGame("/usr/games/zork")
        assert game.is_game_over("You have won") is True

    def test_detects_quit_confirmation(self):
        """Test quit confirmation is detected."""
        game = ZorkGame("/usr/games/zork")
        assert game.is_game_over("Do you wish to leave the game?") is True

    def test_game_continues(self):
        """Test normal output doesn't trigger game over."""
        game = ZorkGame("/usr/games/zork")
        assert game.is_game_over("West of House") is False


class TestZorkGameClose:
    """Test cleanup."""

    @patch("src.game.pexpect.spawn")
    def test_close_terminates_process(self, mock_spawn):
        """Test close terminates process."""
        mock_process = MagicMock()
        mock_spawn.return_value = mock_process

        game = ZorkGame("/usr/games/zork")
        game.start()
        game.close()

        mock_process.terminate.assert_called_once()

    def test_close_handles_none_process(self):
        """Test close doesn't fail if process never started."""
        game = ZorkGame("/usr/games/zork")
        game.close()  # Should not raise


class TestZorkGameCommandTruncation:
    """Test Zork's 6-letter word limit."""

    @patch("src.game.pexpect.spawn")
    def test_long_words_truncated_to_six_chars(self, mock_spawn):
        """Test words longer than 6 chars are truncated."""
        mock_process = MagicMock()
        mock_process.before = b""
        mock_spawn.return_value = mock_process

        game = ZorkGame("/usr/games/zork")
        game.start()
        game.send_command("DISASSEMBLE THE ENCYCLOPEDIA")

        # Zork only uses first 6 letters: DISASS, ENCYCL
        mock_process.sendline.assert_called_with("DISASS THE ENCYCL")
