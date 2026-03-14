# CLAUDE.md

This file provides the plan to follow for guiding Claude when building the project.


##  Architecture Overview

  ┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
  │   LLM Agent     │────▶│  Game Interface  │────▶│   Zork Process  │
  │   (Ollama)      │◀────│   (pexpect/sub)  │◀────│   (frotz)       │
  └─────────────────┘     └──────────────────┘     └─────────────────┘
          │
          ▼
  ┌─────────────────┐
  │  Progress Logger│
  │  (rich/console) │
  └─────────────────┘

## Component Breakdown

  1. Configuration (config.py)
  class Settings(BaseSettings):
      max_iterations: int = 50
      ollama_model: str = "qwen2.5:14b"  # or user's preferred model
      ollama_url: str = "http://localhost:11434"
      zork_game_path: str = "/usr/games/zork"  # or frotz path
      verbose: bool = True  # Show full conversation

  2. Zork Process Manager (game.py)
  class ZorkGame:
      def __init__(self, game_path: str)
      def start(self) -> str  # Returns initial game text
      def send_command(self, command: str) -> tuple[str, Optional[int]]
      # Returns (game_response, score) - score parsed from "SCORE" output
      def get_score(self) -> int  # Explicitly run "SCORE" command and parse
      def close(self)
      def is_game_over(self, output: str) -> bool  # Check QUIT, death, win

  3. LLM Agent with Ollama (agent.py)
  class ZorkAgent:
      def __init__(self, model_name: str, ollama_url: str)
      def create_chain(self)  # LangChain with ChatOllama
      def get_next_command(self, game_output: str, iteration: int) -> str
      # Returns only the command (parsed from LLM response)

  Uses langchain-ollama (or direct Ollama API if needed).

  4. Progress Logger (logger.py)
  class ProgressLogger:
      def show_iteration(self, iteration: int, max_iterations: int)
      def show_command(self, command: str)
      def show_game_output(self, output: str, truncate: bool = True)
      def show_final_score(self, score: int, iterations_used: int)
      def show_separator(self)

  Uses rich library for formatted console output with colors.

  5. Main Controller (main.py)
  def run_game(max_iterations: int, verbose: bool):
      logger = ProgressLogger()
      game = ZorkGame()
      agent = ZorkAgent()

      logger.show_start()
      output = game.start()
      logger.show_game_output(output)

      for iteration in range(1, max_iterations + 1):
          logger.show_iteration(iteration, max_iterations)

          # Get command from LLM
          command = agent.get_next_command(output, iteration)
          logger.show_command(command)

          # Check for quit command
          if command.lower() in ("quit", "q"):
              break

          # Send to game
          output = game.send_command(command)
          logger.show_game_output(output)

          # Check for game over
          if game.is_game_over(output):
              logger.show_game_ended()
              break

      # Get final score
      final_score = game.get_score()
      logger.show_final_score(final_score, iteration)
      game.close()

## Sample Console Output

  ╔══════════════════════════════════════════════════════════════════╗
  ║              GenQuestAI - Zork LLM Player                       ║
  ╚══════════════════════════════════════════════════════════════════╝

  [START] Initial game state:
  West of House
  You are standing in an open field west of a white house, with a boarded front door.
  There is a small mailbox here.

  ═══════════════════════════════════════════════════════════════════
  [Iteration 1/50] > LLM Command: OPEN THE MAILBOX

  West of House
  Opening the small mailbox reveals a leaflet.

  ═══════════════════════════════════════════════════════════════════
  [Iteration 2/50] > LLM Command: TAKE THE LEAFLET

  Taken.

  ═══════════════════════════════════════════════════════════════════
  ...
  ═══════════════════════════════════════════════════════════════════
  [Iteration 47/50] > LLM Command: QUIT

  Your score is 350 (total points 350), in 47 moves.
  This gives you the rank of "Master Adventurer".

  ═══════════════════════════════════════════════════════════════════
  [COMPLETE] Final Score: 350/350 (100%)
  [COMPLETE] Game completed in 47 iterations

  Required Dependencies

  dependencies = [
      "pexpect>=4.9.0",        # Interactive Zork process
      "langchain>=0.3.0",      # LLM framework
      "langchain-ollama",      # Ollama integration
      "rich>=13.0.0",          # Console formatting
      "pydantic>=2.0",         # Configuration
      "pydantic-settings",     # Environment-based config
  ]

  Key Technical Details

  ┌─────────────────────┬─────────────────────────────────────────────────────────────────────┐
  │      Component      │                           Implementation                            │
  ├─────────────────────┼─────────────────────────────────────────────────────────────────────┤
  │ Ollama Connection   │ ChatOllama from langchain-ollama, base_url to localhost:11434       │
  ├─────────────────────┼─────────────────────────────────────────────────────────────────────┤
  │ Score Extraction    │ Parse output from explicit SCORE command: regex (\d+).*total.*(\d+) │
  ├─────────────────────┼─────────────────────────────────────────────────────────────────────┤
  │ Game Over Detection │ Check for: "You have died", "You have won", QUIT confirmation       │
  ├─────────────────────┼─────────────────────────────────────────────────────────────────────┤
  │ Command Extraction  │ Prompt LLM to output ONLY the command, or wrap in JSON/markers      │
  ├─────────────────────┼─────────────────────────────────────────────────────────────────────┤
  │ Progress Display    │ Rich Table or Panel showing iteration counter, command, output      │
  └─────────────────────┴─────────────────────────────────────────────────────────────────────┘

  Prompt Strategy for Ollama

  SYSTEM_PROMPT = """
  You are playing Zork, a text adventure game. Based on the game output,
  decide your next action.

  Game output:
  {game_output}

  Respond ONLY with the command to send. No explanation, no quotes.
  Commands: N, S, E, W, LOOK, TAKE <item>, INVENTORY, etc.
  """

## File Structure

  genquestai/
  ├── __init__.py
  ├── config.py       # Pydantic settings
  ├── game.py         # Zork process manager
  ├── agent.py        # Ollama LLM agent
  ├── logger.py       # Progress display
  └── main.py         # Entry point

  Does this updated plan meet your requirements? Any adjustments before I implement?
       
## Test driven development approach

Strict TDD approach:

  For EACH component:
    1. Write tests (fail initially)
    2. Implement component
    3. Run tests → Fix errors → Repeat until all pass
    4. Only then move to next component

## Development Order & Testing Strategy

  Phase 1: Config + Logger (foundations)
      ↓
  Phase 2: Zork Game Interface (with test mock)
      ↓
  Phase 3: LLM Agent (with test mock)
      ↓
  Phase 4: Main Controller (integration)
      ↓
  Phase 5: Full Integration Tests

  ---
  Phase 1: Configuration & Logger

  Files:
  - src/config.py - Pydantic settings
  - src/logger.py - Rich console output
  - tests/test_config.py - Config validation tests
  - tests/test_logger.py - Output capture tests

  Test Approach:
### tests/test_config.py
  def test_settings_from_env():
      """Test config loads from environment variables."""

  def test_max_iterations_positive():
      """Test max_iterations must be > 0."""

  def test_ollama_url_validation():
      """Test Ollama URL format."""

  Manual Verification:
  uv run python -c "from src.config import Settings; s = Settings(); print(s)"

  ---
  Phase 2: Zork Game Interface

  Files:
  - src/game.py - Zork process manager
  - tests/test_game.py - Unit tests with mocked process
  - tests/test_game_integration.py - Tests against real Zork (optional)

  Test Approach - Mocked Process:

### tests/test_game.py
  class MockPexpect:
      """Mock pexpect.spawn for testing without Zork installed."""
      def __init__(self):
          self.before = b"West of House\nYou are in an open field."
          self.after = b">"

      def sendline(self, cmd):
          self.command_sent = cmd

      def expect(self, pattern):
          return 0

  def test_game_start_returns_initial_text():
      """Test game.start() captures initial room description."""

  def test_send_command_returns_output():
      """Test sending command returns game response."""

  def test_score_extraction_regex():
      """Test parsing score from various Zork outputs."""
      # "Your score is 350 (total points 350)"
      # "Your score is 0 (total points 350)"
      # "I don't know the word 'score'."

  def test_game_over_detection():
      """Test detecting death, quit, win conditions."""
      # Death: "You have died"
      # Win: "You have won"
      # Quit: "Do you wish to leave the game?"

  def test_command_limiting():
      """Test command truncation to 6 chars (Zork parser rule)."""

  Test Fixture - FakeZork:
### tests/fixtures/fake_zork.py
  class FakeZork:
      """Simulates Zork responses for testing."""
      def __init__(self):
          self.room = "West of House"
          self.inventory = []
          self.score = 0

      def respond(self, command: str) -> str:
          # Simulated game logic
          if command == "LOOK":
              return self.room_description()
          elif command.startswith("TAKE"):
              return self.take_item(command)
          elif command == "SCORE":
              return f"Your score is {self.score}..."
          # etc.

  Manual Verification:
  # Requires Zork/frotz installed
  uv run pytest tests/test_game_integration.py -v

  ---
  Phase 3: LLM Agent (Ollama)

  Files:
  - src/agent.py - Ollama LLM interface
  - tests/test_agent.py - Unit tests with mocked LLM
  - tests/test_agent_integration.py - Tests against real Ollama

  Test Approach - Mocked LLM:

### tests/test_agent.py
  class MockOllama:
      """Mock Ollama responses for testing."""
      def __init__(self, responses: list[str]):
          self.responses = responses
          self.call_count = 0

      def invoke(self, prompt):
          response = self.responses[self.call_count]
          self.call_count += 1
          return response

  def test_agent_extracts_command_from_response():
      """Test parsing command from LLM output."""
      # Input: "I should go north. NORTH"
      # Output: "NORTH"

  def test_agent_handles_json_format():
      """Test if agent uses JSON mode for reliable extraction."""

  def test_agent_includes_game_history():
      """Test conversation context includes past moves."""

  def test_agent_handles_empty_game_output():
      """Test graceful handling of empty/timeout responses."""

  def test_command_cleaning():
      """Test stripping quotes, extra text from command."""
      # "go north" → "NORTH"
      # "NORTH" → "NORTH"
      # '"take lamp"' → "TAKE LAMP"

  Test Scenarios (Predefined Agent Responses):
### tests/fixtures/agent_scenarios.py
  SCENARIOS = [
      {
          "name": "west_of_house_first_move",
          "game_output": "West of House...",
          "expected_command": "NORTH"  # or OPEN MAILBOX
      },
      {
          "name": "combat_response",
          "game_output": "The troll swings...",
          "expected_command": "ATTACK TROLL"
      }
  ]

  Manual Verification:
  # Requires Ollama running locally
  uv run pytest tests/test_agent_integration.py -v

  ---
  Phase 4: Main Controller

  Files:
  - src/main.py - Main controller
  - src/runner.py - Game loop (separate from entry point)
  - tests/test_runner.py - Full loop tests with mocks
  - tests/test_main.py - Entry point tests

  Test Approach - Fully Mocked:

### tests/test_runner.py
  class MockGame:
      def __init__(self, responses: list[tuple[str, int]]):
          self.responses = responses  # (output, score) pairs

  class MockAgent:
      def __init__(self, commands: list[str]):
          self.commands = commands

  class MockLogger:
      def __init__(self):
          self.events = []

      def show_iteration(self, i, max_i):
          self.events.append(("iteration", i))

  def test_run_completes_max_iterations():
      """Test loop runs exactly max_iterations times."""

  def test_run_stops_on_quit():
      """Test loop stops early when agent sends QUIT."""

  def test_run_stops_on_death():
      """Test loop stops when game reports death."""

  def test_final_score_displayed():
      """Test score is retrieved and displayed at end."""

  def test_progress_logged_each_iteration():
      """Test logger receives all iteration events."""

  def test_game_cleanup_on_exception():
      """Test game.close() called even if loop crashes."""

  Test Scenarios:
### tests/fixtures/game_scenarios.py
  COMPLETION_SCENARIO = {
      "max_iterations": 5,
      "agent_commands": ["NORTH", "SOUTH", "EAST", "WEST", "QUIT"],
      "game_responses": [
          ("North of House...", 0),
          ("South of House...", 0),
          ("East of House...", 5),
          ("West of House...", 5),
          ("Do you wish to leave? (Y/N)", 5)
      ],
      "expected_iterations": 5,
      "expected_final_score": 5
  }

  DEATH_SCENARIO = {
      "max_iterations": 50,
      "agent_commands": ["NORTH", "ATTACK TROLL"] * 25,
      "game_responses": [
          ("Forest", 0),
          ("Troll Room\nThe troll attacks!", 0),
          ("Forest", 0),
          ("You have died", 10),
          # ... loop should stop here
      ],
      "expected_iterations": 4,
      "expected_final_score": 10
  }

  ---
  Phase 5: Full Integration Tests

  Files:
  - tests/test_full_integration.py - End-to-end with real dependencies

  Requirements:
  - Zork/frotz installed
  - Ollama running with model pulled

### tests/test_full_integration.py
  @pytest.mark.integration
  def test_full_game_real_zork_real_ollama():
      """Full test with real components."""
      # Run with max_iterations=5
      # Verify Zork process spawned
      # Verify Ollama called
      # Verify score retrieved

  ---
  Test Infrastructure

  tests/conftest.py:
  import pytest

  @pytest.fixture
  def mock_settings():
      """Default test settings."""
      return Settings(
          max_iterations=10,
          ollama_model="test-model",
          zork_game_path="/fake/path"
      )

  @pytest.fixture
  def capture_output():
      """Capture Rich console output."""
      # Use io.StringIO or rich.console.Console with file=

  @pytest.fixture
  def temp_zork_save(tmp_path):
      """Create temporary save file for testing."""

  pyproject.toml additions:
  [tool.pytest.ini_options]
  markers = [
      "integration: marks tests requiring external services (Zork, Ollama)",
      "slow: marks tests taking >1 second"
  ]
  filterwarnings = [
      "ignore::DeprecationWarning",
  ]

  ---
##  Makefile Commands (convenience)

  # Run all unit tests (fast, no external deps)
  test:
        uv run pytest tests/ -v -m "not integration" --tb=short

  # Run integration tests (requires Zork + Ollama)
  test-integration:
        uv run pytest tests/ -v -m integration --tb=short

  # Run specific component tests
  test-game:
        uv run pytest tests/test_game.py -v

  test-agent:
        uv run pytest tests/test_agent.py -v

  test-runner:
        uv run pytest tests/test_runner.py -v

  # Test with coverage
  test-cov:
        uv run pytest tests/ -v --cov=src --cov-report=term-missing -m "not integration"

  ---
## Development Workflow

  # 1. Start with config + logger
  uv run pytest tests/test_config.py tests/test_logger.py -v

  # 2. Develop game interface with mocks
  uv run pytest tests/test_game.py -v

  # 3. Verify with real Zork (if available)
  uv run pytest tests/test_game_integration.py -v

  # 4. Develop agent with mocks
  uv run pytest tests/test_agent.py -v

  # 5. Verify with real Ollama (if running)
  uv run pytest tests/test_agent_integration.py -v

  # 6. Develop runner with mocks
  uv run pytest tests/test_runner.py -v

  # 7. Full integration
  uv run pytest tests/ -v
