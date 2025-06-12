import asyncio
import schedule
import time
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path
from src.core.reddit_client import RedditClient
from src.core.relevance_analyzer import RelevanceAnalyzer, RelevanceScore
from src.utils.logger import Logger
from src.utils.storage import DataStorage

class ThreadMonitor:
    def __init__(self):
        self.reddit_client = RedditClient()
        self.relevance_analyzer = RelevanceAnalyzer()
        self.logger = Logger()
        self.storage = DataStorage()
        self.monitored_subreddits = self._load_monitored_subreddits()
        
    def _load_monitored_subreddits(self) -> Dict[str, List[str]]:
        """Load monitored subreddits from configuration."""
        return {
            "primary": [
                "teachers", "specialed", "autism", "ADHD",
                "speechtherapy", "occupationaltherapy", "homeschool",
                "Parenting", "toddlers", "preschool"
            ],
            "secondary": [
                "education", "ABA", "ASD", "learningdisabilities",
                "Montessori", "waldorf", "ECEProfessionals",
                "socialwork", "childdevelopment"
            ],
            "tertiary": [
                "kindergarten", "elementary", "SLP",
                "AskParents", "daddit", "Mommit"
            ]
        }
    
    async def monitor_subreddit(self, subreddit: str, priority: str):
        """Monitor a specific subreddit for relevant threads."""
        try:
            # Get recent posts
            posts = await self.reddit_client.search_subreddit(subreddit, limit=50)
            
            for post in posts:
                # Get comments for the post
                comments = await self.reddit_client.get_post_comments(post['id'], limit=100)
                comment_texts = [comment['body'] for comment in comments]
                
                # Analyze thread relevance
                relevance = self.relevance_analyzer.analyze_thread(
                    post['selftext'],
                    comment_texts
                )
                
                # Store if relevant
                if relevance.total_score >= 4:  # Medium priority or higher
                    self._store_relevant_thread(subreddit, post, comments, relevance)
                    
                    # Log high-priority threads
                    if relevance.total_score >= 8:
                        self.logger.info(
                            f"High-priority thread found in r/{subreddit}: "
                            f"Score: {relevance.total_score}, "
                            f"User Type: {relevance.user_type.value}"
                        )
        
        except Exception as e:
            self.logger.error(f"Error monitoring r/{subreddit}", e)
    
    def _store_relevant_thread(self, subreddit: str, post: Dict[str, Any],
                             comments: List[Dict[str, Any]], relevance: RelevanceScore):
        """Store relevant thread data."""
        thread_data = {
            "subreddit": subreddit,
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
        
        # Store in appropriate file based on relevance score
        if relevance.total_score >= 8:
            self.storage.save_high_priority_thread(thread_data)
        elif relevance.total_score >= 6:
            self.storage.save_medium_priority_thread(thread_data)
        else:
            self.storage.save_low_priority_thread(thread_data)
    
    async def run_monitoring(self):
        """Run the monitoring service."""
        running = True
        while running:
            try:
                print("Starting monitoring cycle...")
                # Monitor primary subreddits daily
                for subreddit in self.monitored_subreddits["primary"]:
                    print(f"Monitoring subreddit: {subreddit}")
                    await self.monitor_subreddit(subreddit, "primary")
                
                # Monitor secondary subreddits every 3 days
                if datetime.utcnow().weekday() % 3 == 0:
                    for subreddit in self.monitored_subreddits["secondary"]:
                        print(f"Monitoring subreddit: {subreddit}")
                        await self.monitor_subreddit(subreddit, "secondary")
                
                # Monitor tertiary subreddits weekly
                if datetime.utcnow().weekday() == 0:
                    for subreddit in self.monitored_subreddits["tertiary"]:
                        print(f"Monitoring subreddit: {subreddit}")
                        await self.monitor_subreddit(subreddit, "tertiary")
                
                print("Waiting for next monitoring cycle...")
                # Wait for next monitoring cycle
                await asyncio.sleep(3600)  # Check every hour
                
            except asyncio.CancelledError:
                print("Monitoring task cancelled.")
                running = False
            except Exception as e:
                self.logger.error("Error in monitoring cycle", e)
                await asyncio.sleep(300)  # Wait 5 minutes before retrying 