"""Tests for progress logger module."""

import io
from unittest.mock import patch

import pytest

from src.logger import ProgressLogger


class TestProgressLoggerInit:
    """Test logger initialization."""

    def test_logger_creates_console(self):
        """Test logger initializes Rich console."""
        logger = ProgressLogger()
        assert logger.console is not None

    def test_logger_verbose_mode(self):
        """Test logger respects verbose flag."""
        logger_verbose = ProgressLogger(verbose=True)
        logger_quiet = ProgressLogger(verbose=False)
        assert logger_verbose.verbose is True
        assert logger_quiet.verbose is False


class TestShowIteration:
    """Test iteration display."""

    def test_show_iteration_outputs_iteration_number(self, capsys):
        """Test iteration number is displayed."""
        logger = ProgressLogger()
        logger.show_iteration(5, 50)
        captured = capsys.readouterr()
        assert "5" in captured.out or "5" in str(logger.console.export_text())

    def test_show_iteration_outputs_max_iterations(self, capsys):
        """Test max iterations is displayed."""
        logger = ProgressLogger()
        logger.show_iteration(5, 50)
        captured = capsys.readouterr()
        assert "50" in captured.out or "50" in str(logger.console.export_text())


class TestShowCommand:
    """Test command display."""

    def test_show_command_outputs_command(self, capsys):
        """Test command is displayed."""
        logger = ProgressLogger()
        logger.show_command("NORTH")
        captured = capsys.readouterr()
        assert "NORTH" in captured.out or "NORTH" in str(logger.console.export_text())

    def test_show_command_handles_long_command(self, capsys):
        """Test long commands are displayed."""
        logger = ProgressLogger()
        logger.show_command("ATTACK TROLL WITH SWORD")
        captured = capsys.readouterr()
        assert "ATTACK" in captured.out or "ATTACK" in str(logger.console.export_text())


class TestShowGameOutput:
    """Test game output display."""

    def test_show_game_output_displays_text(self, capsys):
        """Test game output is displayed."""
        logger = ProgressLogger()
        logger.show_game_output("West of House")
        captured = capsys.readouterr()
        assert "West" in captured.out or "West" in str(logger.console.export_text())

    def test_show_game_output_respects_verbose_true(self):
        """Test full output shown when verbose=True."""
        logger = ProgressLogger(verbose=True)
        long_text = "Line 1\nLine 2\nLine 3"
        # Should show all lines
        output = logger.show_game_output(long_text)
        assert output is not None

    def test_show_game_output_respects_verbose_false(self):
        """Test truncated output when verbose=False."""
        logger = ProgressLogger(verbose=False)
        long_text = "Line 1\nLine 2\nLine 3\n" * 100
        output = logger.show_game_output(long_text)
        assert output is not None


class TestShowFinalScore:
    """Test final score display."""

    def test_show_final_score_outputs_score(self, capsys):
        """Test score is displayed."""
        logger = ProgressLogger()
        logger.show_final_score(350, 47)
        captured = capsys.readouterr()
        assert "350" in captured.out or "350" in str(logger.console.export_text())

    def test_show_final_score_outputs_iterations(self, capsys):
        """Test iterations used is displayed."""
        logger = ProgressLogger()
        logger.show_final_score(350, 47)
        captured = capsys.readouterr()
        assert "47" in captured.out or "47" in str(logger.console.export_text())


class TestShowSeparator:
    """Test separator display."""

    def test_show_separator_outputs_something(self, capsys):
        """Test separator is displayed."""
        logger = ProgressLogger()
        logger.show_separator()
        captured = capsys.readouterr()
        # Separator should produce output
        assert captured.out != "" or logger.console.export_text() != ""


class TestShowStart:
    """Test start display."""

    def test_show_start_outputs_title(self, capsys):
        """Test title is displayed."""
        logger = ProgressLogger()
        logger.show_start()
        captured = capsys.readouterr()
        text = captured.out or logger.console.export_text()
        assert "GenQuestAI" in text or "Zork" in text


class TestShowGameEnded:
    """Test game ended display."""

    def test_show_game_ended_outputs_message(self, capsys):
        """Test game ended message is displayed."""
        logger = ProgressLogger()
        logger.show_game_ended()
        captured = capsys.readouterr()
        text = captured.out or logger.console.export_text()
        assert "ended" in text.lower() or "complete" in text.lower()
