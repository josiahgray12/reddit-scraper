import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

class DataStorage:
    def __init__(self, base_dir: str = "data"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        
        # Create subdirectories for different priority levels
        self.high_priority_dir = self.base_dir / "high_priority"
        self.medium_priority_dir = self.base_dir / "medium_priority"
        self.low_priority_dir = self.base_dir / "low_priority"
        
        for directory in [self.high_priority_dir, self.medium_priority_dir, self.low_priority_dir]:
            directory.mkdir(exist_ok=True)
        
    def _get_timestamp(self) -> str:
        """Get current timestamp in a file-friendly format."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def save_high_priority_thread(self, thread_data: Dict[str, Any]):
        """Save high-priority thread data."""
        timestamp = self._get_timestamp()
        filename = f"high_priority_{timestamp}.json"
        filepath = self.high_priority_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(thread_data, f, indent=2)
    
    def save_medium_priority_thread(self, thread_data: Dict[str, Any]):
        """Save medium-priority thread data."""
        timestamp = self._get_timestamp()
        filename = f"medium_priority_{timestamp}.json"
        filepath = self.medium_priority_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(thread_data, f, indent=2)
    
    def save_low_priority_thread(self, thread_data: Dict[str, Any]):
        """Save low-priority thread data."""
        timestamp = self._get_timestamp()
        filename = f"low_priority_{timestamp}.json"
        filepath = self.low_priority_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(thread_data, f, indent=2)
    
    def get_recent_threads(self, priority: str = "high", limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent threads of specified priority."""
        if priority == "high":
            directory = self.high_priority_dir
        elif priority == "medium":
            directory = self.medium_priority_dir
        else:
            directory = self.low_priority_dir
        
        threads = []
        for file in sorted(directory.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)[:limit]:
            with open(file) as f:
                threads.append(json.load(f))
        
        return threads
    
    def get_threads_by_subreddit(self, subreddit: str, priority: str = None) -> List[Dict[str, Any]]:
        """Get threads from a specific subreddit."""
        threads = []
        
        directories = []
        if priority == "high":
            directories = [self.high_priority_dir]
        elif priority == "medium":
            directories = [self.medium_priority_dir]
        elif priority == "low":
            directories = [self.low_priority_dir]
        else:
            directories = [self.high_priority_dir, self.medium_priority_dir, self.low_priority_dir]
        
        for directory in directories:
            for file in directory.glob("*.json"):
                with open(file) as f:
                    thread_data = json.load(f)
                    if thread_data["subreddit"] == subreddit:
                        threads.append(thread_data)
        
        return sorted(threads, key=lambda x: x["relevance"]["timestamp"], reverse=True)
    
    def get_threads_by_user_type(self, user_type: str, priority: str = None) -> List[Dict[str, Any]]:
        """Get threads from a specific user type."""
        threads = []
        
        directories = []
        if priority == "high":
            directories = [self.high_priority_dir]
        elif priority == "medium":
            directories = [self.medium_priority_dir]
        elif priority == "low":
            directories = [self.low_priority_dir]
        else:
            directories = [self.high_priority_dir, self.medium_priority_dir, self.low_priority_dir]
        
        for directory in directories:
            for file in directory.glob("*.json"):
                with open(file) as f:
                    thread_data = json.load(f)
                    if thread_data["relevance"]["user_type"] == user_type:
                        threads.append(thread_data)
        
        return sorted(threads, key=lambda x: x["relevance"]["timestamp"], reverse=True)
    
    def get_competitive_mentions(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get threads mentioning competitors."""
        mentions = {}
        
        for directory in [self.high_priority_dir, self.medium_priority_dir, self.low_priority_dir]:
            for file in directory.glob("*.json"):
                with open(file) as f:
                    thread_data = json.load(f)
                    for mention in thread_data["relevance"]["competitive_mentions"]:
                        if mention not in mentions:
                            mentions[mention] = []
                        mentions[mention].append(thread_data)
        
        return mentions
    
    def save_posts(self, subreddit: str, posts: List[Dict[str, Any]]):
        """Save posts data to a JSON file."""
        timestamp = self._get_timestamp()
        filename = f"{subreddit}_posts_{timestamp}.json"
        filepath = self.base_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump({
                'subreddit': subreddit,
                'timestamp': timestamp,
                'posts': posts
            }, f, indent=2)
    
    def save_comments(self, post_id: str, comments: List[Dict[str, Any]]):
        """Save comments data to a JSON file."""
        timestamp = self._get_timestamp()
        filename = f"post_{post_id}_comments_{timestamp}.json"
        filepath = self.base_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump({
                'post_id': post_id,
                'timestamp': timestamp,
                'comments': comments
            }, f, indent=2)
    
    def save_user_data(self, username: str, user_data: Dict[str, Any]):
        """Save user data to a JSON file."""
        timestamp = self._get_timestamp()
        filename = f"user_{username}_{timestamp}.json"
        filepath = self.base_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump({
                'username': username,
                'timestamp': timestamp,
                'data': user_data
            }, f, indent=2)
    
    def get_latest_data(self, pattern: str) -> Dict[str, Any]:
        """Get the most recent data file matching the pattern."""
        files = list(self.base_dir.glob(f"{pattern}*.json"))
        if not files:
            return {}
        
        latest_file = max(files, key=lambda x: x.stat().st_mtime)
        with open(latest_file) as f:
            return json.load(f) 