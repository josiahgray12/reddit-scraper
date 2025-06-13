# Installation Guide

This guide will help you set up the Nookly Reddit Monitor step by step.

## 1. Python Installation

### Windows
1. Visit [python.org](https://python.org)
2. Click "Download Python"
3. Run the installer
4. ✅ Check "Add Python to PATH"
5. Click "Install Now"

### macOS
1. Visit [python.org](https://python.org)
2. Click "Download Python"
3. Open the .pkg file
4. Follow the installation wizard

### Linux
```bash
sudo apt update
sudo apt install python3 python3-pip
```

## 2. Reddit API Setup

1. Go to [Reddit's Developer Portal](https://www.reddit.com/prefs/apps)
2. Click "create another app..."
3. Fill in the details:
   - Name: Nookly Bot
   - Type: Script
   - Description: Reddit monitoring for Nookly
   - About URL: (leave blank)
   - Redirect URI: http://localhost:8080
4. Click "create app"
5. Note down:
   - Client ID (under the app name)
   - Client Secret (labeled "secret")

## 3. Email Setup (Gmail)

1. Go to your [Google Account Settings](https://myaccount.google.com)
2. Click "Security"
3. Enable "2-Step Verification" if not already enabled
4. Go back to Security
5. Click "App passwords"
6. Select:
   - App: Mail
   - Device: Other (Custom name)
   - Name: Nookly Bot
7. Click "Generate"
8. Copy the 16-character password

## 4. Configuration Files

### .env File
Create a file named `.env` with:
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=NooklyBot/1.0
```

### config.json
1. Copy `config-template.json` to `config.json`
2. Update the email settings:
   - `sender_email`: Your Gmail address
   - `sender_password`: Your Gmail App Password
   - `recipient_email`: Where to send digests

## 5. First Run

1. Open terminal/command prompt
2. Navigate to the project folder
3. Run:
   ```bash
   python start.py
   ```
4. The script will:
   - Check Python version
   - Install required packages
   - Validate configuration
   - Start monitoring

## 6. Verifying Installation

Run the status check:
```bash
python check-status.py
```

You should see:
- ✅ System Status: Running (with process ID and start time)
- ✅ All configuration files present
- ✅ Log files created:
  - `logs/daily.log`: General operation logs
  - `logs/error.log`: Error-specific logs

## 7. Testing Email

1. Wait for the first daily digest (8 AM)
2. Or run the test:
   ```bash
   python test-email.py
   ```

## 8. Monitoring Logs

The system creates two types of logs:
1. `logs/daily.log`: Contains all operational logs (INFO level and above)
   - Thread monitoring
   - Email sending
   - General system status
2. `logs/error.log`: Contains only error messages
   - API errors
   - Connection issues
   - Configuration problems

To view logs:
```bash
# View daily logs
cat logs/daily.log

# View error logs
cat logs/error.log
```

## Common Issues

### Python Not Found
- Make sure Python is installed
- Check if Python is in PATH
- Try running `python --version`

### Package Installation Fails
- Check internet connection
- Try running:
  ```bash
  pip install --upgrade pip
  pip install -r requirements.txt
  ```

### Email Not Sending
- Verify Gmail App Password
- Check if 2-Step Verification is enabled
- Ensure correct SMTP settings
- Check `logs/error.log` for specific error messages

### Reddit API Errors
- Verify Client ID and Secret
- Check if the app is properly created
- Ensure correct User Agent string
- Check `logs/error.log` for API-related errors

### System Not Running
- Check if the process is running:
  ```bash
  python check-status.py
  ```
- If not running, check `logs/error.log` for errors
- Restart the system:
  ```bash
  python start.py
  ```

## Need Help?

Contact support:
- Email: support@nookly.com
- Hours: Monday-Friday, 9 AM - 5 PM EST
- Include any error messages from `logs/error.log` when contacting support 