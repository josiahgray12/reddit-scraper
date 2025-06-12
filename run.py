"""
Main entry point for the Reddit scraper application.
"""

import asyncio
from src.core.reddit_client import RedditClient
from src.monitor import ThreadMonitor
from src.utils.logger import Logger

# Initialize logger
logger = Logger()

async def main():
    """Main entry point for the application."""
    monitor = None
    try:
        # Initialize Reddit client
        reddit_client = RedditClient()
        await reddit_client.initialize()

        # Create thread monitor
        monitor = ThreadMonitor(reddit_client)

        # List of subreddits to monitor
        subreddits = [
            "autism",
            "ADHD",
            "specialed",
            "Teachers",
            "SLP",
            "OccupationalTherapy",
            "homeschool",
            "Parenting"
        ]

        # Start monitoring
        logger.info("Starting thread monitoring...")
        await monitor.run_monitoring(subreddits)

    except KeyboardInterrupt:
        logger.info("Shutting down...")
        if monitor:
            await monitor.stop()
    except Exception as e:
        logger.error("Error in main", e)
        if monitor:
            await monitor.stop()
        raise
    finally:
        if monitor:
            await monitor.stop()

if __name__ == "__main__":
    asyncio.run(main()) 