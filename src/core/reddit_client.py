import os
import asyncpraw
from dotenv import load_dotenv
from src.utils.logger import Logger
from src.utils.storage import DataStorage
import json
import asyncio
from datetime import datetime
from ratelimit import limits, sleep_and_retry
from typing import List, Dict, Any, Optional
from pathlib import Path
from src.core.relevance_analyzer import RelevanceAnalyzer

# Load environment variables from .env file
load_dotenv()

class RedditClient:
    def __init__(self):
        self.client = None
        self.config = self._load_config()
        self.logger = Logger()
        self.relevance_analyzer = RelevanceAnalyzer()
        
    async def initialize(self):
        """Initialize Reddit client with credentials from environment variables."""
        self.client = asyncpraw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
    
    async def cleanup(self):
        """Clean up resources and close client session."""
        if self.client:
            try:
                # Close the Reddit client
                await self.client.close()
                # Force cleanup of any remaining aiohttp sessions
                await asyncio.sleep(0.1)  # Give time for sessions to close
                self.client = None
            except Exception as e:
                self.logger.error(f"Error during cleanup: {str(e)}")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON files."""
        config_path = Path('config/config.json')
        with open(config_path) as f:
            return json.load(f)
    
    @sleep_and_retry
    @limits(calls=60, period=60)
    async def search_subreddit(self, subreddit_name: str, query: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Search posts in a subreddit with optional query."""
        subreddit = await self.client.subreddit(subreddit_name)
        posts = []
        
        if query:
            search_results = subreddit.search(query, limit=limit)
        else:
            search_results = subreddit.new(limit=limit)
        
        async for post in search_results:
            posts.append(self._format_post(post))
        
        return posts
    
    @sleep_and_retry
    @limits(calls=60, period=60)
    async def get_post_details(self, post_id: str) -> Dict[str, Any]:
        """Get detailed information about a post."""
        submission = await self.client.submission(id=post_id)
        return self._format_post(submission, detailed=True)
    
    @sleep_and_retry
    @limits(calls=60, period=60)
    async def get_post_comments(self, post_id: str, limit: int = 1000) -> List[Dict[str, Any]]:
        """Get comments for a specific post with rate limiting."""
        submission = await self.client.submission(id=post_id)
        await submission.comments.replace_more(limit=0)
        comments = []
        
        # Convert to list first, then slice
        all_comments = await submission.comments.list()
        for comment in all_comments[:limit]:
            comments.append(self._format_comment(comment))
        
        return comments
    
    @sleep_and_retry
    @limits(calls=60, period=60)
    async def get_user_activity(self, username: str) -> Dict[str, Any]:
        """Get user activity with rate limiting."""
        user = await self.client.redditor(username)
        recent_posts = []
        recent_comments = []
        
        # Get submissions
        submissions = await user.submissions.new(limit=10)
        async for post in submissions:
            recent_posts.append(self._format_post(post))
            
        # Get comments
        comments = await user.comments.new(limit=10)
        async for comment in comments:
            recent_comments.append(self._format_comment(comment))
            
        return {
            'username': username,
            'created_utc': user.created_utc,
            'comment_karma': user.comment_karma,
            'link_karma': user.link_karma,
            'is_gold': user.is_gold,
            'is_mod': user.is_mod,
            'recent_posts': recent_posts,
            'recent_comments': recent_comments
        }
    
    @sleep_and_retry
    @limits(calls=60, period=60)
    async def track_thread(self, post_id: str) -> Dict[str, Any]:
        """Monitor a thread for new comments."""
        submission = await self.client.submission(id=post_id)
        recent_comments = []
        
        # Get new comments
        comments = await submission.comments.new(limit=10)
        async for comment in comments:
            recent_comments.append(self._format_comment(comment))
            
        return {
            'post': self._format_post(submission),
            'comment_count': submission.num_comments,
            'last_updated': datetime.utcnow().timestamp(),
            'recent_comments': recent_comments
        }
    
    @sleep_and_retry
    @limits(calls=60, period=60)
    async def get_subreddit_info(self, subreddit_name: str) -> Dict[str, Any]:
        """Get subreddit metadata."""
        subreddit = await self.client.subreddit(subreddit_name)
        return {
            'name': subreddit.display_name,
            'title': await subreddit.title,
            'description': await subreddit.description,
            'subscribers': await subreddit.subscribers,
            'created_utc': subreddit.created_utc,
            'over18': subreddit.over18,
            'is_private': subreddit.subreddit_type == 'private'
        }
    
    @sleep_and_retry
    @limits(calls=60, period=60)
    async def get_subreddit_posts(self, subreddit_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get posts from a subreddit."""
        return await self.search_subreddit(subreddit_name, limit=limit)
    
    def _format_post(self, post, detailed: bool = False) -> Dict[str, Any]:
        """Format post data consistently."""
        base_data = {
            'id': post.id,
            'title': post.title,
            'author': str(post.author),
            'created_utc': post.created_utc,
            'score': post.score,
            'num_comments': post.num_comments,
            'url': post.url,
            'selftext': post.selftext
        }
        
        if detailed:
            base_data.update({
                'upvote_ratio': post.upvote_ratio,
                'is_original_content': post.is_original_content,
                'is_self': post.is_self,
                'permalink': post.permalink,
                'subreddit': str(post.subreddit),
                'edited': post.edited,
                'stickied': post.stickied,
                'locked': post.locked
            })
        
        return base_data
    
    def _format_comment(self, comment) -> Dict[str, Any]:
        """Format comment data consistently."""
        return {
            'id': comment.id,
            'author': str(comment.author),
            'body': comment.body,
            'created_utc': comment.created_utc,
            'score': comment.score,
            'permalink': comment.permalink,
            'is_submitter': comment.is_submitter,
            'edited': comment.edited,
            'stickied': comment.stickied
        }
    
    def _log_thread_metrics(self, post_id: str, metrics: Dict[str, Any]) -> None:
        """Log thread engagement metrics consistently."""
        self.logger.info(
            f"Thread {post_id} metrics: "
            f"score={metrics['score']:.2f}, "
            f"comments={metrics['comment_count']}, "
            f"engagement={metrics['engagement_rate']:.2f}"
        )

    @sleep_and_retry
    @limits(calls=60, period=60)
    async def get_relevant_threads(self, subreddit_name: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get relevant threads from a subreddit."""
        try:
            self.logger.info(f"Fetching relevant threads from r/{subreddit_name} (limit: {limit})")
            # Get recent posts
            posts = await self.search_subreddit(subreddit_name, limit=limit)
            self.logger.info(f"Found {len(posts)} posts in r/{subreddit_name}")
            relevant_threads = []
            
            for post in posts:
                try:
                    if not post or not isinstance(post, dict):
                        self.logger.warning(f"Invalid post data received for subreddit {subreddit_name}")
                        continue

                    # Validate required post fields
                    required_fields = ['id', 'score', 'num_comments']
                    if not all(field in post for field in required_fields):
                        self.logger.warning(f"Post {post.get('id', 'unknown')} missing required fields")
                        continue

                    # Get comments for the post
                    comments = await self.get_post_comments(post['id'], limit=100)

                    # Use Claude/NLTK for relevance analysis
                    relevance = self.relevance_analyzer.analyze_thread(
                        post_content=post.get('selftext', ''),
                        comments_content=[c.get('body', '') for c in comments]
                    )
                    post['relevance'] = relevance.__dict__ if relevance else {}

                    relevant_threads.append({
                        'post': post,
                        'comments': comments
                    })

                    # Log if thread is considered relevant
                    if relevance and relevance.total_score >= 6:
                        self.logger.info(
                            f"High-priority thread found in r/{subreddit_name}: "
                            f"Score: {relevance.total_score:.2f}, "
                            f"Comments: {len(comments)}"
                        )
                except Exception as post_error:
                    self.logger.error(
                        f"Error processing post {post.get('id', 'unknown')} in r/{subreddit_name}",
                        post_error
                    )
                    continue
            self.logger.info(
                f"Completed processing r/{subreddit_name}: "
                f"Found {len(relevant_threads)} relevant threads"
            )
            return relevant_threads
        except Exception as e:
            self.logger.error(f"Error getting relevant threads from r/{subreddit_name}", e)
            return []
    
    @sleep_and_retry
    @limits(calls=60, period=60)
    async def get_thread(self, thread_id: str, subreddit_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific thread with its comments."""
        try:
            # Get post details
            post = await self.get_post_details(thread_id)
            if not post:
                return None
            # Get comments
            comments = await self.get_post_comments(thread_id)
            # Use Claude/NLTK for relevance analysis
            relevance = self.relevance_analyzer.analyze_thread(
                post_content=post.get('selftext', ''),
                comments_content=[c.get('body', '') for c in comments]
            )
            post['relevance'] = relevance.__dict__ if relevance else {}
            return {
                'post': post,
                'comments': comments
            }
        except Exception as e:
            self.logger.error(f"Error getting thread {thread_id} from r/{subreddit_name}", e)
            return None
    
    async def monitor_subreddits(self) -> Dict[str, List[Dict[str, Any]]]:
        """Monitor configured subreddits and return their posts."""
        results = {}
        for subreddit in self.config['monitored_subreddits']:
            results[subreddit['name']] = await self.get_subreddit_posts(
                subreddit['name'],
                limit=self.config['max_posts_per_subreddit']
            )
        return results 