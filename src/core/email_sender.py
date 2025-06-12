"""
Email sender for daily digests of relevant Reddit threads.
"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
from datetime import datetime

class EmailSender:
    def __init__(self):
        """Initialize the email sender with configuration."""
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load email configuration from config.json."""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)['email']
        except FileNotFoundError:
            raise Exception("config.json not found. Please create it with email settings.")
        except json.JSONDecodeError:
            raise Exception("Invalid config.json format. Please check the file.")

    def _create_email_content(self, threads: List[Dict[str, Any]]) -> str:
        """Create HTML content for the email."""
        html = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; }
                .thread { margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
                .thread-title { font-size: 18px; font-weight: bold; color: #2c3e50; }
                .thread-meta { color: #7f8c8d; font-size: 14px; margin: 5px 0; }
                .thread-summary { margin: 10px 0; }
                .thread-response { background: #f9f9f9; padding: 10px; border-left: 3px solid #3498db; }
                .action-buttons { margin-top: 10px; }
                .button { display: inline-block; padding: 8px 15px; margin-right: 10px; 
                         text-decoration: none; border-radius: 3px; color: white; }
                .approve { background: #2ecc71; }
                .edit { background: #f1c40f; }
                .reject { background: #e74c3c; }
            </style>
        </head>
        <body>
            <h1>Daily Digest: Relevant Reddit Threads</h1>
            <p>Here are the relevant threads from the past 24 hours:</p>
        """

        for thread in threads:
            post = thread['post']
            relevance = thread['relevance']
            
            html += f"""
            <div class="thread">
                <div class="thread-title">{post['title']}</div>
                <div class="thread-meta">
                    Subreddit: r/{post['subreddit']} | 
                    Relevance Score: {relevance['score']} | 
                    User Type: {relevance['user_type']}
                </div>
                <div class="thread-summary">
                    <strong>Summary:</strong> {post['selftext'][:200]}...
                </div>
                <div class="thread-response">
                    <strong>Drafted Response:</strong><br>
                    {thread['drafted_response']}
                </div>
                <div class="action-buttons">
                    <a href="#" class="button approve">Approve</a>
                    <a href="#" class="button edit">Edit</a>
                    <a href="#" class="button reject">Reject</a>
                </div>
            </div>
            """

        html += """
        </body>
        </html>
        """
        return html

    def send_daily_digest(self, threads: List[Dict[str, Any]]) -> None:
        """Send daily digest email with relevant threads."""
        if not threads:
            return

        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Daily Digest: {len(threads)} Relevant Threads - {datetime.now().strftime('%Y-%m-%d')}"
        msg['From'] = self.config['sender_email']
        msg['To'] = self.config['recipient_email']

        # Create HTML content
        html_content = self._create_email_content(threads)
        msg.attach(MIMEText(html_content, 'html'))

        try:
            # Connect to SMTP server
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.starttls()
                server.login(self.config['sender_email'], self.config['sender_password'])
                server.send_message(msg)
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}") 