"""
Test suite for Claude API integration.
"""

import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch
from src.core.claude_client import ClaudeClient

@pytest.fixture
def mock_config():
    """Create a mock configuration file."""
    config = {
        "claude": {
            "api_key": "test-api-key",
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 1000,
            "temperature": 0.7,
            "response_preferences": {
                "tone": "warm and supportive",
                "style": "conversational",
                "promotion_level": "subtle",
                "include_resources": True,
                "max_responses": 3
            }
        }
    }
    return config

@pytest.fixture
def sample_thread():
    """Create a sample thread for testing."""
    return {
        "id": "test123",
        "subreddit": "r/Parenting",
        "title": "Struggling with my 5-year-old's emotional outbursts",
        "selftext": "My son has been having frequent meltdowns at home and school. His teacher suggested he might need more support with emotional regulation. Any advice?",
        "top_comments": [
            "Have you tried using a feelings chart?",
            "Consider talking to a child psychologist"
        ]
    }

@pytest.fixture
def mock_claude_response():
    """Create a mock Claude API response."""
    mock_response = Mock()
    mock_response.content = [Mock()]
    mock_response.content[0].text = """
Here's a helpful response that acknowledges your situation and provides support.

Relevance Score: 0.9

Another variation focusing on specific strategies.

Relevance Score: 0.85

A third option emphasizing community support.

Relevance Score: 0.8
"""
    mock_response.usage = Mock()
    mock_response.usage.input_tokens = 100
    mock_response.usage.output_tokens = 200
    return mock_response

def test_claude_client_initialization(mock_config, tmp_path):
    """Test Claude client initialization."""
    # Create temporary config file
    config_file = tmp_path / "config.json"
    with open(config_file, "w") as f:
        json.dump(mock_config, f)
    
    # Initialize client
    client = ClaudeClient(str(config_file))
    assert client.config == mock_config
    assert client.usage_log.parent.exists()

def test_system_prompt_creation():
    """Test system prompt creation."""
    client = ClaudeClient()
    prompt = client._create_system_prompt()
    
    # Check key elements in the prompt
    assert "Nookly" in prompt
    assert "educational platform" in prompt
    assert "Guidelines" in prompt
    assert "Response Structure" in prompt
    assert "parent/educator peer" in prompt

def test_user_prompt_creation(sample_thread):
    """Test user prompt creation."""
    client = ClaudeClient()
    prompt = client._create_user_prompt(
        sample_thread,
        "Parent",
        ["emotional regulation", "meltdowns"]
    )
    
    # Check key elements in the prompt
    assert sample_thread["subreddit"] in prompt
    assert sample_thread["title"] in prompt
    assert sample_thread["selftext"] in prompt
    assert "Parent" in prompt
    assert "emotional regulation" in prompt
    assert "meltdowns" in prompt

@patch("anthropic.Anthropic")
def test_response_generation(mock_anthropic, mock_config, sample_thread, mock_claude_response, tmp_path):
    """Test response generation with mock API."""
    # Setup mock
    mock_client = Mock()
    mock_client.messages.create.return_value = mock_claude_response
    mock_anthropic.return_value = mock_client
    
    # Create temporary config file
    config_file = tmp_path / "config.json"
    with open(config_file, "w") as f:
        json.dump(mock_config, f)
    
    # Initialize client and generate responses
    client = ClaudeClient(str(config_file))
    responses = client.generate_responses(
        sample_thread,
        "Parent",
        ["emotional regulation", "meltdowns"]
    )
    
    # Verify responses
    assert len(responses) == 3
    assert all("text" in response for response in responses)
    assert all("score" in response for response in responses)
    assert all(0 <= response["score"] <= 1 for response in responses)
    
    # Verify API call
    mock_client.messages.create.assert_called_once()
    call_args = mock_client.messages.create.call_args[1]
    assert call_args["model"] == mock_config["claude"]["model"]
    assert call_args["max_tokens"] == mock_config["claude"]["max_tokens"]
    assert call_args["temperature"] == mock_config["claude"]["temperature"]

@patch("anthropic.Anthropic")
def test_api_error_handling(mock_anthropic, mock_config, sample_thread, tmp_path):
    """Test error handling when API fails."""
    # Setup mock to raise exception
    mock_client = Mock()
    mock_client.messages.create.side_effect = Exception("API Error")
    mock_anthropic.return_value = mock_client
    
    # Create temporary config file
    config_file = tmp_path / "config.json"
    with open(config_file, "w") as f:
        json.dump(mock_config, f)
    
    # Initialize client and generate responses
    client = ClaudeClient(str(config_file))
    responses = client.generate_responses(
        sample_thread,
        "Parent",
        ["emotional regulation", "meltdowns"]
    )
    
    # Verify fallback response
    assert len(responses) == 1
    assert "text" in responses[0]
    assert "score" in responses[0]
    assert responses[0]["score"] == 0.5

def test_usage_logging(mock_config, sample_thread, mock_claude_response, tmp_path):
    """Test API usage logging."""
    # Create temporary config and log files
    config_file = tmp_path / "config.json"
    log_file = tmp_path / "logs" / "claude_usage.log"
    log_file.parent.mkdir()
    
    with open(config_file, "w") as f:
        json.dump(mock_config, f)
    
    # Initialize client
    client = ClaudeClient(str(config_file))
    client.usage_log = log_file
    
    # Mock API response
    with patch("anthropic.Anthropic") as mock_anthropic:
        mock_client = Mock()
        mock_client.messages.create.return_value = mock_claude_response
        mock_anthropic.return_value = mock_client
        
        # Generate responses
        client.generate_responses(
            sample_thread,
            "Parent",
            ["emotional regulation", "meltdowns"]
        )
    
    # Verify log file
    assert log_file.exists()
    with open(log_file) as f:
        log_content = f.read()
        assert "test123" in log_content  # thread ID
        assert "300" in log_content  # total tokens
        assert "0.000015" in log_content  # input token cost
        assert "0.000075" in log_content  # output token cost

def test_connection_test(mock_config, tmp_path):
    """Test API connection testing."""
    # Create temporary config file
    config_file = tmp_path / "config.json"
    with open(config_file, "w") as f:
        json.dump(mock_config, f)
    
    # Test successful connection
    with patch("anthropic.Anthropic") as mock_anthropic:
        mock_client = Mock()
        mock_client.messages.create.return_value = Mock()
        mock_anthropic.return_value = mock_client
        
        client = ClaudeClient(str(config_file))
        assert client.test_connection() is True
    
    # Test failed connection
    with patch("anthropic.Anthropic") as mock_anthropic:
        mock_client = Mock()
        mock_client.messages.create.side_effect = Exception("Connection Error")
        mock_anthropic.return_value = mock_client
        
        client = ClaudeClient(str(config_file))
        assert client.test_connection() is False 