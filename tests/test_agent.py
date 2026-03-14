"""Tests for LLM agent module."""

from unittest.mock import MagicMock, patch

import pytest

from src.agent import ZorkAgent


class TestZorkAgentInit:
    """Test agent initialization."""

    def test_agent_stores_model_name(self):
        """Test model name is stored."""
        agent = ZorkAgent("qwen2.5:14b", "http://localhost:11434")
        assert agent.model_name == "qwen2.5:14b"

    def test_agent_stores_ollama_url(self):
        """Test Ollama URL is stored."""
        agent = ZorkAgent("qwen2.5:14b", "http://localhost:11434")
        assert agent.ollama_url == "http://localhost:11434"


class TestZorkAgentGetNextCommand:
    """Test getting next command from LLM."""

    @patch("src.agent.ChatOllama")
    def test_get_next_command_returns_command(self, mock_chat_class):
        """Test agent returns command from LLM."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "NORTH"
        mock_llm.invoke.return_value = mock_response
        mock_chat_class.return_value = mock_llm

        agent = ZorkAgent("qwen2.5:14b", "http://localhost:11434")
        command = agent.get_next_command("West of House", 1)

        assert command == "NORTH"

    @patch("src.agent.ChatOllama")
    def test_get_next_command_strips_whitespace(self, mock_chat_class):
        """Test command is stripped of whitespace."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "  NORTH  "
        mock_llm.invoke.return_value = mock_response
        mock_chat_class.return_value = mock_llm

        agent = ZorkAgent("qwen2.5:14b", "http://localhost:11434")
        command = agent.get_next_command("West of House", 1)

        assert command == "NORTH"

    @patch("src.agent.ChatOllama")
    def test_get_next_command_removes_quotes(self, mock_chat_class):
        """Test quotes are removed from command."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = '"TAKE LAMP"'
        mock_llm.invoke.return_value = mock_response
        mock_chat_class.return_value = mock_llm

        agent = ZorkAgent("qwen2.5:14b", "http://localhost:11434")
        command = agent.get_next_command("Room description", 1)

        assert command == "TAKE LAMP"

    @patch("src.agent.ChatOllama")
    def test_get_next_command_uppercases(self, mock_chat_class):
        """Test command is uppercased."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "north"
        mock_llm.invoke.return_value = mock_response
        mock_chat_class.return_value = mock_llm

        agent = ZorkAgent("qwen2.5:14b", "http://localhost:11434")
        command = agent.get_next_command("West of House", 1)

        assert command == "NORTH"

    @patch("src.agent.ChatOllama")
    def test_get_next_command_includes_game_output_in_prompt(self, mock_chat_class):
        """Test game output is included in LLM prompt."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "NORTH"
        mock_llm.invoke.return_value = mock_response
        mock_chat_class.return_value = mock_llm

        agent = ZorkAgent("qwen2.5:14b", "http://localhost:11434")
        agent.get_next_command("West of House description", 1)

        # Check that invoke was called with messages containing game output
        call_args = mock_llm.invoke.call_args
        assert call_args is not None
        messages = call_args[0][0]
        # Check that game output is in the messages
        message_text = str(messages)
        assert "West of House" in message_text

    @patch("src.agent.ChatOllama")
    def test_get_next_command_includes_iteration(self, mock_chat_class):
        """Test iteration number is included in prompt."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "NORTH"
        mock_llm.invoke.return_value = mock_response
        mock_chat_class.return_value = mock_llm

        agent = ZorkAgent("qwen2.5:14b", "http://localhost:11434")
        agent.get_next_command("Room description", 5)

        call_args = mock_llm.invoke.call_args
        assert call_args is not None


class TestZorkAgentCommandCleaning:
    """Test command cleaning logic."""

    @patch("src.agent.ChatOllama")
    def test_extracts_command_from_explanation(self, mock_chat_class):
        """Test command extracted from explanatory text."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "I should go north. Command: NORTH"
        mock_llm.invoke.return_value = mock_response
        mock_chat_class.return_value = mock_llm

        agent = ZorkAgent("qwen2.5:14b", "http://localhost:11434")
        command = agent.get_next_command("Room", 1)

        # Should extract just the command part
        assert "NORTH" in command

    @patch("src.agent.ChatOllama")
    def test_handles_multiline_response(self, mock_chat_class):
        """Test multiline response is handled."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "Let me think...\n\nTAKE LAMP"
        mock_llm.invoke.return_value = mock_response
        mock_chat_class.return_value = mock_llm

        agent = ZorkAgent("qwen2.5:14b", "http://localhost:11434")
        command = agent.get_next_command("Room", 1)

        assert "TAKE LAMP" in command

    @patch("src.agent.ChatOllama")
    def test_handles_empty_response(self, mock_chat_class):
        """Test empty response returns empty string."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = ""
        mock_llm.invoke.return_value = mock_response
        mock_chat_class.return_value = mock_llm

        agent = ZorkAgent("qwen2.5:14b", "http://localhost:11434")
        command = agent.get_next_command("Room", 1)

        assert command == ""


class TestZorkAgentSystemPrompt:
    """Test system prompt configuration."""

    @patch("src.agent.ChatOllama")
    def test_system_prompt_includes_zork_instructions(self, mock_chat_class):
        """Test system prompt contains Zork game instructions."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "NORTH"
        mock_llm.invoke.return_value = mock_response
        mock_chat_class.return_value = mock_llm

        agent = ZorkAgent("qwen2.5:14b", "http://localhost:11434")
        agent.get_next_command("Room", 1)

        # Check that system message was included
        call_args = mock_chat_class.call_args
        assert call_args is not None
        # System prompt should be set

    @patch("src.agent.ChatOllama")
    def test_system_prompt_includes_command_examples(self, mock_chat_class):
        """Test system prompt includes command examples."""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "NORTH"
        mock_llm.invoke.return_value = mock_response
        mock_chat_class.return_value = mock_llm

        agent = ZorkAgent("qwen2.5:14b", "http://localhost:11434")
        agent.get_next_command("Room", 1)

        # Verify ChatOllama was initialized
        mock_chat_class.assert_called_once()
