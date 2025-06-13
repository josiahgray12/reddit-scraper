# Reddit Scraper

A Python-based tool for monitoring and analyzing Reddit threads related to educational content for children ages 2-8.

## Features

- Monitors multiple subreddits for relevant content
- Analyzes thread relevance using Claude AI and NLTK
- Generates personalized responses using Claude AI
- Sends daily email digests of relevant threads
- Stores data in JSON format

## Prerequisites

- Python 3.10 or higher
- Reddit API credentials
- Claude API key
- SMTP server credentials for email notifications

## Configuration

### Environment Variables (.env)

Create a `.env` file in the project root with your credentials:
```env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# Logging Configuration
LOG_LEVEL=DEBUG
LOG_FILE=logs/app.log

# Storage Configuration
DATA_DIR=data
```

### Application Configuration (config.json)

Create a `config.json` file in the project root with the following structure:
```json
{
   "email": {
      // Gmail SMTP server settings
      "smtp_server": "smtp.gmail.com",
      "smtp_port": 587,
      
      // Your Gmail address that will send the emails
      "sender_email": "your-email@gmail.com",
      
      // Your Gmail App Password (not your regular Gmail password)
      // To get an App Password:
      // 1. Go to your Google Account settings
      // 2. Enable 2-Step Verification if not already enabled
      // 3. Go to Security > App passwords
      // 4. Select "Mail" and "Other (Custom name)"
      // 5. Name it "Nookly Bot"
      // 6. Copy the 16-character password Google generates
      "sender_password": "wxzy wxyz wxyz wxyz",
      
      // The email address where you want to receive daily digests
      "recipient_email": "your-email@gmail.com"
   },
   "claude": {
      "api_key": "your-anthropic-api-key",
      "model": "claude-3-5-sonnet-20241022",
      "max_tokens": 1000,
      "temperature": 0.7,
      "response_preferences": {
         "tone": "warm and supportive",
         "style": "conversational",
         "promotion_level": "subtle",
         "include_resources": true,
         "max_responses": 3
      }
   }
}
```

#### Configuration Options

- **claude**
  - `model`: Claude model to use for analysis
  - `api_key`: Your Claude API key (can also be set in .env)

- **email**
  - `from_email`: Sender email address
  - `to_email`: Recipient email address
  - `subject`: Subject line for daily digest
  - `send_time`: Time to send daily digest (24-hour format)

## Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/reddit-scraper.git
cd reddit-scraper
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create both `.env` and `config.json` files as described above.

5. Run the application:
```bash
python run.py
```

## Droplet Deployment and Management

### Initial Setup

1. SSH into your droplet:
```bash
ssh root@your_droplet_ip
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/reddit-scraper.git
cd reddit-scraper
```

3. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create and configure both `.env` and `config.json` files:
```bash
nano .env
nano config.json
# Add your credentials and configuration as shown above
```

### Running the Application

1. Create a new screen session:
```bash
screen -S reddit-scraper
```

2. Activate the virtual environment:
```bash
source venv/bin/activate
```

3. Start the application:
```bash
python run.py
```

4. Detach from the screen session:
- Press `Ctrl+A`, then `D`

### Managing the Application

1. List screen sessions:
```bash
screen -ls
```

2. Reattach to the screen session:
```bash
screen -r reddit-scraper
```

3. Stop the application:
- Reattach to the screen session
- Press `Ctrl+C` to stop the application
- Type `exit` to close the screen session

4. Restart the application:
- Create a new screen session
- Activate the virtual environment
- Run `python run.py`

### Updating the Application

1. Pull the latest changes:
```bash
cd reddit-scraper
git pull
```

2. Update dependencies if needed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

3. Restart the application:
- Stop the current instance (Ctrl+C in screen session)
- Start a new instance (python run.py)

### Monitoring Logs

1. View the daily log:
```bash
tail -f logs/daily.log
```

2. View the error log:
```bash
tail -f logs/error.log
```

## Project Structure

```
reddit-scraper/
├── src/
│   ├── core/
│   │   ├── reddit_client.py
│   │   ├── relevance_analyzer.py
│   │   ├── response_generator.py
│   │   └── claude_client.py
│   ├── utils/
│   │   ├── logger.py
│   │   └── storage.py
│   └── monitor.py
├── data/
│   └── threads/
├── logs/
├── tests/
├── .env
├── config.json
├── requirements.txt
└── README.md
```

## Testing

Run the test suite:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
