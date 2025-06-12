import os
import time
import schedule
from dotenv import load_dotenv
from core.reddit_client import RedditClient
from utils.storage import DataStorage

def run_scraper():
    """Run the Reddit scraper and save data."""
    print("Starting Reddit scraper...")
    
    # Initialize clients
    reddit_client = RedditClient()
    storage = DataStorage()
    
    # Monitor subreddits
    results = reddit_client.monitor_subreddits()
    
    # Save data for each subreddit
    for subreddit, posts in results.items():
        print(f"Saving {len(posts)} posts from r/{subreddit}")
        storage.save_posts(subreddit, posts)
        
        # Get and save comments for each post
        for post in posts:
            comments = reddit_client.get_post_comments(post['id'])
            storage.save_comments(post['id'], comments)
    
    print("Scraping completed successfully!")

def main():
    """Main function to run the scraper on a schedule."""
    # Load environment variables
    load_dotenv()
    
    # Run immediately on startup
    run_scraper()
    
    # Schedule regular runs
    interval = int(os.getenv('UPDATE_INTERVAL', '300'))  # Default to 5 minutes
    schedule.every(interval).seconds.do(run_scraper)
    
    print(f"Scraper scheduled to run every {interval} seconds")
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main() 