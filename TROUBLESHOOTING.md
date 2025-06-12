# Troubleshooting Guide

## Quick Reference

| Issue | Check | Solution |
|-------|-------|----------|
| System won't start | `python --version` | Install Python 3.8+ |
| Email not sending | Gmail App Password | Generate new App Password |
| Reddit API errors | API credentials | Verify in Reddit Developer Portal |
| No daily digest | Log files | Check `logs/daily.log` |

## Common Issues and Solutions

### 1. System Won't Start

#### Error: "Python not found"
```
❌ Python version too old!
Please install Python 3.8 or newer
```

**Solution:**
1. Download Python from [python.org](https://python.org)
2. During installation:
   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install for all users"

#### Error: "Missing required packages"
```
❌ Error installing packages: [error message]
```

**Solution:**
1. Open terminal/command prompt
2. Run:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### 2. Email Issues

#### Error: "Failed to send email"
```
❌ Error sending email: [error message]
```

**Solution:**
1. Verify Gmail settings:
   - 2-Step Verification is enabled
   - App Password is correct
   - SMTP settings are correct
2. Check `config.json`:
   ```json
   {
       "email": {
           "smtp_server": "smtp.gmail.com",
           "smtp_port": 587,
           "sender_email": "your-email@gmail.com",
           "sender_password": "your-app-password",
           "recipient_email": "your-email@gmail.com"
       }
   }
   ```

#### No Daily Digest Received
1. Check if system is running:
   ```bash
   python check-status.py
   ```
2. Check log files:
   ```bash
   python view-logs.py
   ```
3. Verify email settings in `config.json`

### 3. Reddit API Issues

#### Error: "Invalid Reddit credentials"
```
❌ Error: Invalid Reddit credentials
```

**Solution:**
1. Go to [Reddit's Developer Portal](https://www.reddit.com/prefs/apps)
2. Verify app settings:
   - App type: Script
   - Client ID is correct
   - Client Secret is correct
3. Check `.env` file:
   ```
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=NooklyBot/1.0
   ```

#### Error: "Rate limit exceeded"
```
❌ Error: Rate limit exceeded
```

**Solution:**
1. Wait 5-10 minutes
2. Restart the monitor:
   ```bash
   python start.py
   ```

### 4. Log File Issues

#### Error: "Cannot create log file"
```
❌ Error: Cannot create log file
```

**Solution:**
1. Check directory permissions:
   ```bash
   python check-status.py
   ```
2. Create logs directory:
   ```bash
   mkdir logs
   ```

#### Log Files Missing
1. Check if system is running
2. Verify directory structure:
   ```
   reddit-scraper/
   ├── logs/
   │   ├── daily.log
   │   └── error.log
   ├── data/
   └── status.txt
   ```

### 5. Configuration Issues

#### Error: "Missing configuration file"
```
❌ config.json not found!
```

**Solution:**
1. Copy template:
   ```bash
   cp config-template.json config.json
   ```
2. Update settings in `config.json`

#### Error: "Invalid configuration"
```
❌ Error validating configuration: [error message]
```

**Solution:**
1. Check `config.json` format
2. Verify all required fields:
   - `smtp_server`
   - `smtp_port`
   - `sender_email`
   - `sender_password`
   - `recipient_email`

## Maintenance Tasks

### Daily Checks
1. Run status check:
   ```bash
   python check-status.py
   ```
2. Check email digest received
3. Review log files:
   ```bash
   python view-logs.py
   ```

### Weekly Checks
1. Verify Reddit API usage
2. Check email delivery
3. Review error logs

### Monthly Checks
1. Update monitoring keywords
2. Review performance metrics
3. Backup configuration

## Getting Help

### Contact Support
- Email: support@nookly.com
- Hours: Monday-Friday, 9 AM - 5 PM EST

### Provide Information
When contacting support, include:
1. Error message
2. Log files
3. System status
4. Steps to reproduce

### Documentation
- [Installation Guide](INSTALLATION.md)
- [README](README.md)
- [API Documentation](API.md) 