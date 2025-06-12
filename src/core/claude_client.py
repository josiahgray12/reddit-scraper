"""
Claude API integration for intelligent response generation.
"""

import os
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime
import anthropic
from pathlib import Path

logger = logging.getLogger(__name__)

class ClaudeClient:
    def __init__(self, config_path: str = "config.json"):
        """Initialize Claude client with configuration."""
        self.config = self._load_config(config_path)
        self.client = anthropic.Anthropic(api_key=self.config["claude"]["api_key"])
        self.usage_log = Path("logs/claude_usage.log")
        self._setup_logging()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            if "claude" not in config:
                raise KeyError("Missing Claude configuration in config.json")
            return config
        except Exception as e:
            logger.error(f"Failed to load config: {str(e)}")
            raise

    def _setup_logging(self):
        """Setup usage logging."""
        self.usage_log.parent.mkdir(exist_ok=True)
        if not self.usage_log.exists():
            self.usage_log.write_text("timestamp,thread_id,tokens_used,cost\n")

    def _log_usage(self, thread_id: str, tokens_used: int, cost: float):
        """Log API usage for tracking."""
        timestamp = datetime.now().isoformat()
        with open(self.usage_log, 'a') as f:
            f.write(f"{timestamp},{thread_id},{tokens_used},{cost}\n")

    def _create_system_prompt(self) -> str:
        """Create the system prompt for Claude."""
        return """You are helping draft Reddit responses for Nookly, an AI-powered educational platform for children ages 2-8 focusing on personalized learning, SEL, and special needs support.

Guidelines:
- Be genuinely helpful first, promotional second
- Share relevant free resources when possible
- Only mention Nookly if it directly solves their problem
- Match the subreddit's tone and culture
- Avoid being salesy or pushy
- Focus on the child's needs and development
- Be empathetic and understanding
- Use a warm, supportive tone
- Provide specific, actionable advice
- Include relevant research or expert opinions when helpful

Response Structure:
1. Acknowledge their situation and show empathy
2. Share relevant free resources or advice
3. If Nookly is relevant, mention it naturally
4. End with encouragement and support

Remember: You are writing as a helpful parent/educator peer, not a salesperson."""

    def _create_user_prompt(self, thread_content: Dict, user_type: str, pain_points: List[str]) -> str:
        """Create the user prompt with thread context."""
        return f"""CONTEXT:
Subreddit: {thread_content['subreddit']}
Original Post: {thread_content['title']}
{thread_content['selftext']}

Top Comments:
{chr(10).join([f"- {comment}" for comment in thread_content['top_comments']])}

USER TYPE: {user_type}
PAIN POINTS: {', '.join(pain_points)}

Please generate 3 different response variations that are:
1. Helpful and empathetic
2. Natural and conversational
3. Subtly promotional when relevant
4. Tailored to this specific situation

For each response, include a relevance score (0-1) indicating how well it matches the user's needs."""

    def generate_responses(self, thread_content: Dict, user_type: str, pain_points: List[str]) -> List[Dict]:
        """Generate multiple response variations using Claude."""
        try:
            system_prompt = self._create_system_prompt()
            user_prompt = self._create_user_prompt(thread_content, user_type, pain_points)
            
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                temperature=0.7,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            # Parse responses and scores
            responses = []
            current_response = {"text": "", "score": 0.0}
            
            for line in response.content[0].text.split('\n'):
                if line.startswith('Relevance Score:'):
                    current_response["score"] = float(line.split(':')[1].strip())
                    responses.append(current_response)
                    current_response = {"text": "", "score": 0.0}
                else:
                    current_response["text"] += line + '\n'
            
            if current_response["text"]:
                responses.append(current_response)
            
            # Log usage
            self._log_usage(
                thread_content.get('id', 'unknown'),
                response.usage.input_tokens + response.usage.output_tokens,
                response.usage.input_tokens * 0.000015 + response.usage.output_tokens * 0.000075
            )
            
            return responses
            
        except Exception as e:
            logger.error(f"Claude API error: {str(e)}")
            # Fallback to simple template if API fails
            return self._generate_fallback_response(thread_content, user_type, pain_points)

    def _generate_fallback_response(self, thread_content: Dict, user_type: str, pain_points: List[str]) -> List[Dict]:
        """Generate a simple fallback response if Claude API fails."""
        logger.warning("Using fallback response generation")
        return [{
            "text": f"I understand you're dealing with {', '.join(pain_points)}. "
                   f"As a fellow {user_type.lower()}, I've found these resources helpful: "
                   f"[Free Resource Link]. "
                   f"Would you like to know more about how Nookly can help with this?",
            "score": 0.5
        }]

    def test_connection(self) -> bool:
        """Test Claude API connection."""
        try:
            self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=10,
                messages=[{"role": "user", "content": "Test connection"}]
            )
            return True
        except Exception as e:
            logger.error(f"Claude API connection test failed: {str(e)}")
            return False 