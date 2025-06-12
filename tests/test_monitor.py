"""
Test suite for the Reddit monitor.
"""

import pytest
from unittest.mock import Mock, patch
from src.monitor import ThreadMonitor
from src.core.claude_client import ClaudeClient

@pytest.fixture
def mock_reddit():
    """Create a mock Reddit instance."""
    mock = Mock()
    mock.subreddit.return_value = Mock()
    return mock

@pytest.fixture
def mock_claude():
    """Create a mock Claude client."""
    mock = Mock()
    mock.generate_responses.return_value = [
        {"text": "Test response 1", "score": 0.9},
        {"text": "Test response 2", "score": 0.8}
    ]
    return mock

def test_thread_monitor_initialization(mock_reddit):
    """Test ThreadMonitor initialization."""
    monitor = ThreadMonitor(mock_reddit)
    assert monitor.reddit == mock_reddit
    assert monitor.subreddits == ["Parenting", "Teachers", "Autism", "ADHD", "SpecialNeeds"]

@patch("src.monitor.ThreadMonitor._analyze_thread")
def test_process_thread(mock_analyze, mock_reddit, mock_claude):
    """Test thread processing with Claude integration."""
    # Setup
    monitor = ThreadMonitor(mock_reddit)
    monitor.claude_client = mock_claude
    
    thread = Mock()
    thread.id = "test123"
    thread.title = "Test Thread"
    thread.selftext = "Test content"
    thread.subreddit.display_name = "Parenting"
    
    # Mock thread analysis
    mock_analyze.return_value = {
        "relevance_score": 0.8,
        "user_type": "Parent",
        "pain_points": ["emotional regulation"]
    }
    
    # Process thread
    result = monitor._process_thread(thread)
    
    # Verify
    assert result is not None
    assert "thread_id" in result
    assert "responses" in result
    assert len(result["responses"]) == 2
    assert all("text" in response for response in result["responses"])
    assert all("score" in response for response in result["responses"])
    
    # Verify Claude was called
    mock_claude.generate_responses.assert_called_once()

@patch("src.monitor.ThreadMonitor._analyze_thread")
def test_process_thread_low_relevance(mock_analyze, mock_reddit):
    """Test thread processing with low relevance score."""
    # Setup
    monitor = ThreadMonitor(mock_reddit)
    
    thread = Mock()
    thread.id = "test123"
    thread.title = "Test Thread"
    thread.selftext = "Test content"
    thread.subreddit.display_name = "Parenting"
    
    # Mock thread analysis with low relevance
    mock_analyze.return_value = {
        "relevance_score": 0.3,
        "user_type": "Parent",
        "pain_points": ["emotional regulation"]
    }
    
    # Process thread
    result = monitor._process_thread(thread)
    
    # Verify thread was skipped
    assert result is None

def test_analyze_thread(mock_reddit):
    """Test thread analysis."""
    monitor = ThreadMonitor(mock_reddit)
    
    thread = Mock()
    thread.title = "Help with my child's emotional outbursts"
    thread.selftext = "My 5-year-old has been having frequent meltdowns"
    thread.subreddit.display_name = "Parenting"
    
    analysis = monitor._analyze_thread(thread)
    
    assert "relevance_score" in analysis
    assert "user_type" in analysis
    assert "pain_points" in analysis
    assert isinstance(analysis["relevance_score"], float)
    assert 0 <= analysis["relevance_score"] <= 1
    assert isinstance(analysis["pain_points"], list)

@patch("src.monitor.ThreadMonitor._process_thread")
def test_monitor_threads(mock_process, mock_reddit, mock_claude):
    """Test thread monitoring with Claude integration."""
    # Setup
    monitor = ThreadMonitor(mock_reddit)
    monitor.claude_client = mock_claude
    
    # Mock subreddit and threads
    mock_subreddit = Mock()
    mock_thread = Mock()
    mock_thread.id = "test123"
    mock_thread.title = "Test Thread"
    mock_thread.selftext = "Test content"
    mock_thread.subreddit.display_name = "Parenting"
    
    mock_subreddit.new.return_value = [mock_thread]
    mock_reddit.subreddit.return_value = mock_subreddit
    
    # Mock thread processing
    mock_process.return_value = {
        "thread_id": "test123",
        "responses": [
            {"text": "Test response 1", "score": 0.9},
            {"text": "Test response 2", "score": 0.8}
        ]
    }
    
    # Monitor threads
    results = monitor.monitor_threads()
    
    # Verify
    assert len(results) > 0
    assert all("thread_id" in result for result in results)
    assert all("responses" in result for result in results)
    
    # Verify Claude was called for each processed thread
    assert mock_claude.generate_responses.call_count == len(results)

def test_claude_integration(mock_reddit, mock_claude):
    """Test full Claude integration in thread monitoring."""
    # Setup
    monitor = ThreadMonitor(mock_reddit)
    monitor.claude_client = mock_claude
    
    # Create test thread
    thread = Mock()
    thread.id = "test123"
    thread.title = "Help with my child's emotional outbursts"
    thread.selftext = "My 5-year-old has been having frequent meltdowns"
    thread.subreddit.display_name = "Parenting"
    
    # Process thread
    result = monitor._process_thread(thread)
    
    # Verify Claude integration
    assert result is not None
    assert "responses" in result
    assert len(result["responses"]) == 2
    assert all("text" in response for response in result["responses"])
    assert all("score" in response for response in result["responses"])
    
    # Verify Claude was called with correct parameters
    mock_claude.generate_responses.assert_called_once()
    call_args = mock_claude.generate_responses.call_args[0]
    assert call_args[1] == "Parent"  # user_type
    assert "emotional" in call_args[2][0]  # pain_points 