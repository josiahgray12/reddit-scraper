import os
import json
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.core.reddit_client import RedditClient
from src.core.relevance_analyzer import RelevanceAnalyzer
from src.core.thread_monitor import ThreadMonitor
from src.utils.logger import Logger
from src.utils.storage import DataStorage
from typing import Dict, List, Any
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Reddit Scraper MCP Server",
    description="MCP server for scraping and monitoring Reddit data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
reddit_client = RedditClient()
relevance_analyzer = RelevanceAnalyzer()
thread_monitor = ThreadMonitor()
logger = Logger()
storage = DataStorage()

# Server status tracking
server_start_time = datetime.utcnow()
request_count = 0

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring server status."""
    global request_count
    request_count += 1
    
    return {
        "status": "healthy",
        "uptime_seconds": (datetime.utcnow() - server_start_time).total_seconds(),
        "total_requests": request_count,
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/")
async def root():
    """Root endpoint returning API status."""
    return {
        "status": "active",
        "message": "Reddit Scraper MCP Server is running",
        "endpoints": {
            "health": "/health",
            "search_subreddit": "/mcp/search_subreddit",
            "get_post_details": "/mcp/get_post_details",
            "get_comments": "/mcp/get_comments",
            "monitor_user": "/mcp/monitor_user",
            "track_thread": "/mcp/track_thread",
            "get_subreddit_info": "/mcp/get_subreddit_info",
            "analyze_thread": "/mcp/analyze_thread",
            "get_relevant_threads": "/mcp/get_relevant_threads",
            "get_competitive_mentions": "/mcp/get_competitive_mentions"
        }
    }

@app.get("/mcp/search_subreddit")
async def search_subreddit(subreddit: str, query: str = None, limit: int = 100):
    """MCP Tool: Search posts in specific subreddits."""
    try:
        logger.info(f"Searching subreddit: {subreddit}")
        posts = await reddit_client.search_subreddit(subreddit, query, limit)
        storage.save_posts(subreddit, posts)
        return {"subreddit": subreddit, "posts": posts}
    except Exception as e:
        logger.error("Error searching subreddit", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mcp/get_post_details")
async def get_post_details(post_id: str):
    """MCP Tool: Get detailed post information by ID."""
    try:
        logger.info(f"Getting details for post: {post_id}")
        post_details = await reddit_client.get_post_details(post_id)
        return post_details
    except Exception as e:
        logger.error("Error getting post details", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mcp/get_comments")
async def get_comments(post_id: str, limit: int = 1000):
    """MCP Tool: Retrieve comment threads."""
    try:
        logger.info(f"Getting comments for post: {post_id}")
        comments = await reddit_client.get_post_comments(post_id, limit)
        storage.save_comments(post_id, comments)
        return {"post_id": post_id, "comments": comments}
    except Exception as e:
        logger.error("Error getting comments", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mcp/monitor_user")
async def monitor_user(username: str):
    """MCP Tool: Track specific user activity."""
    try:
        logger.info(f"Monitoring user: {username}")
        user_info = await reddit_client.get_user_activity(username)
        storage.save_user_data(username, user_info)
        return user_info
    except Exception as e:
        logger.error("Error monitoring user", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mcp/track_thread")
async def track_thread(post_id: str):
    """MCP Tool: Monitor threads for new comments."""
    try:
        logger.info(f"Tracking thread: {post_id}")
        thread_info = await reddit_client.track_thread(post_id)
        return thread_info
    except Exception as e:
        logger.error("Error tracking thread", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mcp/get_subreddit_info")
async def get_subreddit_info(subreddit: str):
    """MCP Tool: Get subreddit metadata."""
    try:
        logger.info(f"Getting info for subreddit: {subreddit}")
        subreddit_info = await reddit_client.get_subreddit_info(subreddit)
        return subreddit_info
    except Exception as e:
        logger.error("Error getting subreddit info", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mcp/analyze_thread")
async def analyze_thread(post_id: str):
    """Analyze a thread's relevance to Nookly's business model."""
    try:
        # Get post details
        post = await reddit_client.get_post_details(post_id)
        
        # Get comments
        comments = await reddit_client.get_post_comments(post_id)
        comment_texts = [comment['body'] for comment in comments]
        
        # Analyze relevance
        relevance = relevance_analyzer.analyze_thread(
            post['selftext'],
            comment_texts
        )
        
        # Store if relevant
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
            elif relevance.total_score >= 6:
                storage.save_medium_priority_thread(thread_data)
            else:
                storage.save_low_priority_thread(thread_data)
        
        return {
            "post_id": post_id,
            "relevance": {
                "score": relevance.total_score,
                "user_type": relevance.user_type.value,
                "pain_points": relevance.pain_points,
                "keywords_found": relevance.keywords_found,
                "sentiment_score": relevance.sentiment_score,
                "age_relevance": relevance.age_relevance,
                "urgency_level": relevance.urgency_level,
                "competitive_mentions": relevance.competitive_mentions
            }
        }
    
    except Exception as e:
        logger.error("Error analyzing thread", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mcp/get_relevant_threads")
async def get_relevant_threads(
    priority: str = None,
    subreddit: str = None,
    user_type: str = None,
    limit: int = 10
):
    """Get relevant threads based on filters."""
    try:
        if subreddit:
            threads = storage.get_threads_by_subreddit(subreddit, priority)
        elif user_type:
            threads = storage.get_threads_by_user_type(user_type, priority)
        else:
            threads = storage.get_recent_threads(priority, limit)
        
        return {
            "count": len(threads),
            "threads": threads
        }
    
    except Exception as e:
        logger.error("Error getting relevant threads", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mcp/get_competitive_mentions")
async def get_competitive_mentions():
    """Get threads mentioning competitors."""
    try:
        mentions = storage.get_competitive_mentions()
        return {
            "count": len(mentions),
            "mentions": mentions
        }
    
    except Exception as e:
        logger.error("Error getting competitive mentions", e)
        raise HTTPException(status_code=500, detail=str(e))

async def initialize_components():
    """Initialize components asynchronously."""
    global reddit_client
    await reddit_client.initialize()

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup."""
    await initialize_components()

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", "8000"))
    uvicorn.run(app, host=host, port=port) 