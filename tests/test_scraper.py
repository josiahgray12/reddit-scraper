import asyncio
import os
from dotenv import load_dotenv
from src.core.reddit_client import RedditClient
from src.core.relevance_analyzer import RelevanceAnalyzer
from src.core.thread_monitor import ThreadMonitor
from src.utils.storage import DataStorage
from src.utils.logger import Logger
import pytest

# Load environment variables
load_dotenv()

@pytest.mark.asyncio
async def test_thread_analysis():
    """Test thread analysis functionality."""
    print("\n=== Testing Thread Analysis ===")
    
    # Initialize components
    reddit_client = RedditClient()
    relevance_analyzer = RelevanceAnalyzer()
    storage = DataStorage()
    logger = Logger()
    
    # Test subreddit and post ID (using a real post from r/Parenting)
    subreddit = "Parenting"
    post_id = "1bqj8x"  # Example post ID
    
    try:
        # Get post details
        print(f"\nFetching post from r/{subreddit}...")
        post = await reddit_client.get_post_details(post_id)
        print(f"Title: {post['title']}")
        
        # Get comments
        print("\nFetching comments...")
        comments = await reddit_client.get_post_comments(post_id)
        print(f"Found {len(comments)} comments")
        
        # Analyze thread
        print("\nAnalyzing thread relevance...")
        comment_texts = [comment['body'] for comment in comments]
        relevance = relevance_analyzer.analyze_thread(
            post['selftext'],
            comment_texts
        )
        
        # Print analysis results
        print("\nRelevance Analysis Results:")
        print(f"Total Score: {relevance.total_score}")
        print(f"User Type: {relevance.user_type.value}")
        print(f"Pain Points: {relevance.pain_points}")
        print(f"Keywords Found: {relevance.keywords_found}")
        print(f"Sentiment Score: {relevance.sentiment_score}")
        print(f"Age Relevance: {relevance.age_relevance}")
        print(f"Urgency Level: {relevance.urgency_level}")
        print(f"Competitive Mentions: {relevance.competitive_mentions}")
        
        # Store thread if relevant
        if relevance.total_score >= 4:
            thread_data = {
                "subreddit": post['subreddit'],
                "post": post,
                "comments": comments,
                "relevance": {
                    "score": relevance.total_score,
                    "user_type": relevance.user_type.value,
                    "pain_points": relevance.pain_points,
                    "keywords_found": relevance.keywords_found,
                    "sentiment_score": relevance.sentiment_score,
                    "age_relevance": relevance.age_relevance,
                    "urgency_level": relevance.urgency_level,
                    "competitive_mentions": relevance.competitive_mentions,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
            
            if relevance.total_score >= 8:
                storage.save_high_priority_thread(thread_data)
                print("\nSaved as high priority thread")
            elif relevance.total_score >= 6:
                storage.save_medium_priority_thread(thread_data)
                print("\nSaved as medium priority thread")
            else:
                storage.save_low_priority_thread(thread_data)
                print("\nSaved as low priority thread")
        
    except Exception as e:
        logger.error("Error in thread analysis test", e)
        print(f"Error: {str(e)}")

@pytest.mark.asyncio
async def test_storage_retrieval():
    """Test storage retrieval functionality."""
    print("\n=== Testing Storage Retrieval ===")
    
    storage = DataStorage()
    
    try:
        # Get recent threads
        print("\nRetrieving recent threads...")
        recent_threads = storage.get_recent_threads(limit=5)
        print(f"Found {len(recent_threads)} recent threads")
        
        # Get threads by subreddit
        print("\nRetrieving threads by subreddit...")
        subreddit_threads = storage.get_threads_by_subreddit("Parenting")
        print(f"Found {len(subreddit_threads)} threads in r/Parenting")
        
        # Get competitive mentions
        print("\nRetrieving competitive mentions...")
        competitive_mentions = storage.get_competitive_mentions()
        print(f"Found {len(competitive_mentions)} competitive mentions")
        
    except Exception as e:
        logger.error("Error in storage retrieval test", e)
        print(f"Error: {str(e)}")

async def main():
    """Run all tests."""
    print("Starting Reddit Scraper Tests...")
    
    # Run tests
    await test_thread_analysis()
    await test_storage_retrieval()
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 