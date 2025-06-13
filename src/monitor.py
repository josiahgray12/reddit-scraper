"""
Thread monitoring system for Reddit threads.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from .core.reddit_client import RedditClient
from .core.response_generator import ResponseGenerator
from .core.email_sender import EmailSender
import os

logger = logging.getLogger(__name__)

class ThreadMonitor:
    def __init__(self, reddit_client: RedditClient):
        """Initialize the thread monitor."""
        self.reddit_client = reddit_client
        self.response_generator = ResponseGenerator()
        self.email_sender = EmailSender()
        self.monitored_threads: Dict[str, Dict] = {}
        self._stop_event = asyncio.Event()

    async def cleanup(self):
        """Clean up resources."""
        delete_status_file()  # Delete status file
        await self.reddit_client.cleanup()
        self._stop_event.set()

    async def monitor_thread(self, thread_id: str, subreddit: str) -> None:
        """Monitor a specific thread for updates."""
        try:
            thread = await self.reddit_client.get_thread(thread_id, subreddit)
            if not thread:
                return

            # Check if thread has required data structure
            if not thread.get('post') or not thread['post'].get('relevance'):
                logger.warning(f"Thread {thread_id} missing relevance data, skipping")
                return

            # Ensure relevance is present before accessing it
            relevance_score = thread['post']['relevance'].get('score', 0)
            if relevance_score >= 6:
                response = self.response_generator.generate_response(thread)
                if response:
                    thread['drafted_response'] = response
                    self.monitored_threads[thread_id] = thread
                    logger.info(f"Generated response for thread {thread_id} (score: {relevance_score})")

        except Exception as e:
            logger.error(f"Error monitoring thread {thread_id}: {str(e)}")
            # Log the full thread data for debugging if available
            if thread:
                logger.debug(f"Thread data: {thread}")

    async def run_monitoring(self, subreddits: List[str], interval: int = 300) -> None:
        """Run the monitoring loop."""
        logger.info("Starting thread monitoring...")
        
        while not self._stop_event.is_set():
            try:
                # Get relevant threads from each subreddit
                for subreddit in subreddits:
                    threads = await self.reddit_client.get_relevant_threads(subreddit)
                    
                    # Monitor each thread
                    for thread in threads:
                        await self.monitor_thread(thread['post']['id'], subreddit)
                
                # Send daily digest if it's time
                if self._should_send_digest():
                    await self._send_daily_digest()
                
                # Wait for next interval
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {str(e)}")
                await asyncio.sleep(60)  # Wait a minute before retrying

    def _should_send_digest(self) -> bool:
        """Check if it's time to send the daily digest."""
        now = datetime.now()
        return now.hour == 8 and now.minute == 0  # Send at 8 AM

    async def _send_daily_digest(self) -> None:
        """Send the daily digest of relevant threads."""
        try:
            # Filter threads from the last 24 hours
            cutoff_time = datetime.now() - timedelta(days=1)
            recent_threads = [
                thread for thread in self.monitored_threads.values()
                if datetime.fromtimestamp(thread['post']['created_utc']) > cutoff_time
            ]
            
            if recent_threads:
                self.email_sender.send_daily_digest(recent_threads)
                logger.info(f"Sent daily digest with {len(recent_threads)} threads")
                
                # Clear old threads
                self.monitored_threads.clear()
                
        except Exception as e:
            logger.error(f"Error sending daily digest: {str(e)}")

    async def stop(self) -> None:
        """Stop the monitoring loop and clean up resources."""
        self._stop_event.set()
        await self.cleanup()
        logger.info("Stopping thread monitoring...") 