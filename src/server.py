import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from core.reddit_client import RedditClient
from typing import Dict, List, Any

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Reddit Scraper API",
    description="API for scraping and monitoring Reddit data",
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

# Initialize Reddit client
reddit_client = RedditClient()

@app.get("/")
async def root():
    """Root endpoint returning API status."""
    return {"status": "active", "message": "Reddit Scraper API is running"}

@app.get("/subreddits/{subreddit_name}/posts")
async def get_subreddit_posts(subreddit_name: str, limit: int = 100):
    """Get posts from a specific subreddit."""
    try:
        posts = reddit_client.get_subreddit_posts(subreddit_name, limit)
        return {"subreddit": subreddit_name, "posts": posts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/posts/{post_id}/comments")
async def get_post_comments(post_id: str):
    """Get comments for a specific post."""
    try:
        comments = reddit_client.get_post_comments(post_id)
        return {"post_id": post_id, "comments": comments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{username}")
async def get_user_info(username: str):
    """Get information about a specific user."""
    try:
        user_info = reddit_client.get_user_activity(username)
        return user_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/monitor")
async def monitor_subreddits():
    """Monitor all configured subreddits."""
    try:
        results = reddit_client.monitor_subreddits()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", "8000"))
    uvicorn.run(app, host=host, port=port) 