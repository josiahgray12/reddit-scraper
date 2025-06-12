# Reddit Scraper

A Python application that monitors Reddit threads for relevant content in education and special needs communities.

## Quick Start

### Prerequisites
- Python 3.8 or newer
- Git (for cloning the repository)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/reddit-scraper.git
cd reddit-scraper
```

2. Create and activate the virtual environment:

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Configuration

1. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Reddit API credentials:
```
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

### Running the Application

#### Method 1: Using the Start Script (Recommended)
Simply run:
```bash
python start.py
```

This script will:
- Check Python version
- Create and activate the virtual environment if needed
- Install dependencies
- Start the application

#### Method 2: Manual Start
If you prefer to start manually:

1. Ensure you're in the virtual environment:
```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
.\venv\Scripts\activate
```

2. Run the application:
```bash
python run.py
```

### Monitoring

The application will:
- Monitor specified subreddits for new threads
- Calculate relevance scores based on engagement
- Log high-priority threads
- Generate daily digests

### Logs

Logs are stored in the `logs` directory:
- `reddit_scraper.log`: Main application log
- `thread_metrics.log`: Detailed thread metrics

## Development

### Project Structure
```
reddit-scraper/
├── src/
│   ├── core/
│   │   ├── reddit_client.py
│   │   └── thread_analyzer.py
│   ├── monitor.py
│   └── utils/
│       ├── logger.py
│       └── storage.py
├── logs/
├── .env
├── requirements.txt
├── run.py
└── start.py
```

### Adding New Features

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes
3. Run tests
4. Submit a pull request

## Troubleshooting

### Common Issues

1. **Virtual Environment Not Active**
   - Symptoms: Import errors, missing packages
   - Solution: Activate the virtual environment using the commands above

2. **Missing Dependencies**
   - Symptoms: Import errors
   - Solution: Run `pip install -r requirements.txt`

3. **API Rate Limits**
   - Symptoms: Connection errors, timeouts
   - Solution: Check your Reddit API credentials and rate limits

### Getting Help

If you encounter issues:
1. Check the logs in the `logs` directory
2. Review the troubleshooting section
3. Open an issue on GitHub

## License

This project is licensed under the MIT License - see the LICENSE file for details. 