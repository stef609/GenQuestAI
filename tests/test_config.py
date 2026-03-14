"""Tests for configuration module."""

import os
from pathlib import Path

import pytest
from pydantic import ValidationError

from src.config import Settings


class TestSettingsDefaults:
    """Test default configuration values."""

    def test_default_max_iterations(self):
        """Test max_iterations defaults to 50."""
        settings = Settings()
        assert settings.max_iterations == 50

    def test_default_ollama_model(self):
        """Test ollama_model defaults to qwen2.5:14b."""
        settings = Settings()
        assert settings.ollama_model == "qwen2.5:14b"

    def test_default_ollama_url(self):
        """Test ollama_url defaults to localhost."""
        settings = Settings()
        assert settings.ollama_url == "http://localhost:11434"

    def test_default_zork_game_path(self):
        """Test zork_game_path has a default."""
        settings = Settings()
        assert settings.zork_game_path is not None
        assert isinstance(settings.zork_game_path, str)

    def test_default_verbose(self):
        """Test verbose defaults to True."""
        settings = Settings()
        assert settings.verbose is True


class TestSettingsFromEnv:
    """Test loading configuration from environment variables."""

    def test_max_iterations_from_env(self, monkeypatch):
        """Test max_iterations loads from env."""
        monkeypatch.setenv("MAX_ITERATIONS", "100")
        settings = Settings()
        assert settings.max_iterations == 100

    def test_ollama_model_from_env(self, monkeypatch):
        """Test ollama_model loads from env."""
        monkeypatch.setenv("OLLAMA_MODEL", "mistral:7b")
        settings = Settings()
        assert settings.ollama_model == "mistral:7b"

    def test_ollama_url_from_env(self, monkeypatch):
        """Test ollama_url loads from env."""
        monkeypatch.setenv("OLLAMA_URL", "http://192.168.1.100:11434")
        settings = Settings()
        assert settings.ollama_url == "http://192.168.1.100:11434"

    def test_zork_game_path_from_env(self, monkeypatch):
        """Test zork_game_path loads from env."""
        monkeypatch.setenv("ZORK_GAME_PATH", "/usr/games/zork")
        settings = Settings()
        assert settings.zork_game_path == "/usr/games/zork"

    def test_verbose_from_env(self, monkeypatch):
        """Test verbose loads from env."""
        monkeypatch.setenv("VERBOSE", "false")
        settings = Settings()
        assert settings.verbose is False


class TestSettingsValidation:
    """Test configuration validation."""

    def test_max_iterations_must_be_positive(self):
        """Test max_iterations must be > 0."""
        with pytest.raises(ValidationError):
            Settings(max_iterations=0)

    def test_max_iterations_cannot_be_negative(self):
        """Test max_iterations cannot be negative."""
        with pytest.raises(ValidationError):
            Settings(max_iterations=-1)

    def test_ollama_url_must_be_valid_format(self):
        """Test ollama_url must start with http."""
        with pytest.raises(ValidationError):
            Settings(ollama_url="not-a-url")

    def test_ollama_url_accepts_https(self):
        """Test ollama_url accepts https."""
        settings = Settings(ollama_url="https://localhost:11434")
        assert settings.ollama_url == "https://localhost:11434"


class TestSettingsTypes:
    """Test configuration type coercion."""

    def test_max_iterations_coerced_from_string(self, monkeypatch):
        """Test max_iterations coerced from string env var."""
        monkeypatch.setenv("MAX_ITERATIONS", "75")
        settings = Settings()
        assert settings.max_iterations == 75
        assert isinstance(settings.max_iterations, int)

    def test_verbose_coerced_from_string_true(self, monkeypatch):
        """Test verbose coerced from 'true' string."""
        monkeypatch.setenv("VERBOSE", "true")
        settings = Settings()
        assert settings.verbose is True

    def test_verbose_coerced_from_string_false(self, monkeypatch):
        """Test verbose coerced from 'false' string."""
        monkeypatch.setenv("VERBOSE", "false")
        settings = Settings()
        assert settings.verbose is False
