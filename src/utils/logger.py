import logging
import json
import os
from pathlib import Path
from typing import Dict, Any

class Logger:
    def __init__(self, config_path: str = "config/config.json"):
        self.config = self._load_config(config_path)
        self._setup_logger()
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load logging configuration from JSON file."""
        try:
            with open(config_path) as f:
                return json.load(f)
        except FileNotFoundError:
            print("Configuration file not found. Using default settings.")
            return {
                "logging": {
                    "level": "INFO",
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    "file": "logs/daily.log"
                }
            }
    
    def _setup_logger(self):
        """Set up the logger with configuration."""
        log_config = self.config.get("logging", {})
        log_level = getattr(logging, log_config.get("level", "INFO"))
        log_format = log_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Create handlers for different log files
        daily_handler = logging.FileHandler("logs/daily.log")
        error_handler = logging.FileHandler("logs/error.log")
        console_handler = logging.StreamHandler()
        
        # Set formatters
        formatter = logging.Formatter(log_format)
        daily_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Set levels
        daily_handler.setLevel(logging.INFO)
        error_handler.setLevel(logging.ERROR)
        console_handler.setLevel(log_level)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        # Add handlers
        root_logger.addHandler(daily_handler)
        root_logger.addHandler(error_handler)
        root_logger.addHandler(console_handler)
        
        # Create application logger
        self.logger = logging.getLogger("reddit_scraper")
    
    def info(self, message: str):
        """Log an info message."""
        self.logger.info(message)
    
    def error(self, message: str, error: Exception = None):
        """Log an error message with plain English explanation."""
        if error:
            error_message = self._get_plain_english_error(error)
            self.logger.error(f"{message}: {error_message}")
        else:
            self.logger.error(message)
    
    def warning(self, message: str):
        """Log a warning message."""
        self.logger.warning(message)
    
    def debug(self, message: str):
        """Log a debug message."""
        self.logger.debug(message)
    
    def _get_plain_english_error(self, error: Exception) -> str:
        """Convert technical error messages to plain English."""
        error_messages = {
            "prawcore.exceptions.NotFound": "The requested Reddit content was not found. It may have been deleted or is private.",
            "prawcore.exceptions.Forbidden": "Access to this Reddit content is forbidden. You may not have permission to view it.",
            "prawcore.exceptions.TooManyRequests": "Too many requests to Reddit. Please wait a moment before trying again.",
            "prawcore.exceptions.ServerError": "Reddit's servers are having issues. Please try again later.",
            "prawcore.exceptions.RequestException": "There was a problem connecting to Reddit. Please check your internet connection.",
            "json.JSONDecodeError": "There was a problem reading the configuration file. Please check its format.",
            "FileNotFoundError": "A required file is missing. Please check your installation.",
            "PermissionError": "Permission denied. Please check file permissions.",
            "ValueError": "Invalid value provided. Please check your configuration.",
            "KeyError": "Missing required configuration. Please check your settings."
        }
        
        error_type = type(error).__name__
        return error_messages.get(error_type, f"An unexpected error occurred: {str(error)}") 