import os
import pytest
import asyncio
from src.core.reddit_client import RedditClient
from src.utils.logger import Logger
from src.utils.storage import DataStorage

# Test configuration
TEST_SUBREDDIT = "python"
TEST_POST_ID = "1a2b3c"  # Replace with a real post ID from r/python
TEST_USERNAME = "spez"  # Reddit CEO's username for testing

@pytest.fixture
def reddit_client():
    """Create a Reddit client instance for testing."""
    return RedditClient()

@pytest.fixture
def logger():
    """Create a logger instance for testing."""
    return Logger()

@pytest.fixture
def storage():
    """Create a storage instance for testing."""
    return DataStorage()

@pytest.mark.asyncio
async def test_search_subreddit(reddit_client):
    """Test searching subreddits."""
    # Test basic search
    posts = await reddit_client.search_subreddit(TEST_SUBREDDIT, limit=5)
    assert len(posts) <= 5
    assert all(isinstance(post, dict) for post in posts)
    assert all('id' in post for post in posts)
    
    # Test search with query
    query_posts = await reddit_client.search_subreddit(TEST_SUBREDDIT, query="python", limit=5)
    assert len(query_posts) <= 5
    assert all(isinstance(post, dict) for post in query_posts)

@pytest.mark.asyncio
async def test_get_post_details(reddit_client):
    """Test getting post details."""
    # Get a real post ID from the search results
    posts = await reddit_client.search_subreddit(TEST_SUBREDDIT, limit=1)
    if posts:
        post_id = posts[0]['id']
        post_details = await reddit_client.get_post_details(post_id)
        assert isinstance(post_details, dict)
        assert 'id' in post_details
        assert 'title' in post_details
        assert 'author' in post_details

@pytest.mark.asyncio
async def test_get_comments(reddit_client):
    """Test getting post comments."""
    # Get a real post ID from the search results
    posts = await reddit_client.search_subreddit(TEST_SUBREDDIT, limit=1)
    if posts:
        post_id = posts[0]['id']
        comments = await reddit_client.get_post_comments(post_id, limit=5)
        assert len(comments) <= 5
        assert all(isinstance(comment, dict) for comment in comments)
        assert all('id' in comment for comment in comments)

@pytest.mark.asyncio
async def test_monitor_user(reddit_client):
    """Test monitoring user activity."""
    user_info = await reddit_client.get_user_activity(TEST_USERNAME)
    assert isinstance(user_info, dict)
    assert 'username' in user_info
    assert 'comment_karma' in user_info
    assert 'link_karma' in user_info

@pytest.mark.asyncio
async def test_get_subreddit_info(reddit_client):
    """Test getting subreddit information."""
    subreddit_info = await reddit_client.get_subreddit_info(TEST_SUBREDDIT)
    assert isinstance(subreddit_info, dict)
    assert 'name' in subreddit_info
    assert 'subscribers' in subreddit_info
    assert 'description' in subreddit_info

def test_storage(storage):
    """Test data storage functionality."""
    # Test saving and retrieving data
    test_data = {
        'test_key': 'test_value',
        'timestamp': '2024-01-01'
    }
    
    # Save test data
    storage.save_posts('test_subreddit', [test_data])
    
    # Retrieve latest data
    latest_data = storage.get_latest_data('test_subreddit')
    assert isinstance(latest_data, dict)
    assert 'posts' in latest_data

def test_logger(logger):
    """Test logging functionality."""
    # Test different log levels
    logger.info("Test info message")
    logger.warning("Test warning message")
    logger.error("Test error message")
    logger.debug("Test debug message")
    
    # Test error logging with exception
    try:
        raise ValueError("Test error")
    except Exception as e:
        logger.error("Test error with exception", e)

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 