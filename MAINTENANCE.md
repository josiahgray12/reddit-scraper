# Nookly Reddit Monitor - Maintenance Guide

## Quick Start

### Daily Tasks
1. Check if the system is running:
   ```bash
   python check-status.py
   ```
   You should see:
   - ✅ System Status: Running
   - ✅ Configuration files present
   - ✅ Log files created
   - 📝 Number of threads monitored today
   - 📧 Last email sent

2. Check your email for the daily digest (sent at 8 AM)

### Weekly Tasks
1. Check the logs for any errors:
   ```bash
   python view-logs.py
   ```
   Look for any red error messages or warnings.

2. Verify Reddit API usage:
   - Go to [Reddit's Developer Portal](https://www.reddit.com/prefs/apps)
   - Check if your app is still active
   - Verify the API usage limits

## Common Issues and Solutions

### 1. System Not Running
If `check-status.py` shows the system is not running:

1. Start the system:
   ```bash
   python start.py
   ```

2. If it doesn't start, check the error message and:
   - Make sure you're in the correct directory: `/opt/reddit-monitor`
   - Verify Python is installed: `python --version`
   - Check if the virtual environment is active (you should see `(venv)` at the start of your command line)

### 2. No Daily Digest Emails
If you're not receiving the daily digest emails:

1. Check your spam folder
2. Verify email settings in `config.json`:
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
3. Make sure your Gmail App Password is still valid

### 3. Reddit API Issues
If you see Reddit API errors:

1. Check your Reddit API credentials in the `.env` file:
   ```
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=NooklyBot/1.0
   ```
2. Verify these credentials in the [Reddit Developer Portal](https://www.reddit.com/prefs/apps)

## Important Files and Their Purposes

1. `config.json`: Contains email settings
2. `.env`: Contains Reddit API credentials
3. `requirements.txt`: Lists required Python packages
4. `logs/`: Directory containing log files
   - `daily.log`: General operation logs
   - `error.log`: Error messages
5. `data/`: Directory containing identified threads
   - `high_priority/`: Most relevant threads
   - `medium_priority/`: Moderately relevant threads
   - `low_priority/`: Less relevant threads

## Monitoring Subreddits

The system monitors these subreddits:

### Primary (High Priority)
- teachers
- specialed
- autism
- ADHD
- speechtherapy
- occupationaltherapy
- homeschool
- Parenting
- toddlers
- preschool

### Secondary (Medium Priority)
- education
- ABA
- ASD
- learningdisabilities
- Montessori
- waldorf
- ECEProfessionals
- socialwork
- childdevelopment

### Tertiary (Low Priority)
- kindergarten
- elementary
- SLP
- AskParents
- daddit
- Mommit

## Understanding the Output

### Daily Digest Email
You'll receive an email each morning containing:
1. Number of relevant threads found
2. For each thread:
   - Title and subreddit
   - Relevance score (1-10)
   - User type (Parent, Teacher, etc.)
   - Brief summary
   - Drafted response
   - Action buttons (Approve/Edit/Reject)

### Log Files
- `daily.log`: Shows normal operation
- `error.log`: Shows any problems that need attention

## Getting Help

If you encounter any issues:
1. Check the error logs: `python view-logs.py`
2. Run the status check: `python check-status.py`
3. Contact support: support@nookly.com

## Regular Maintenance Schedule

### Daily
- Check system status
- Review daily digest email
- Check for any error messages

### Weekly
- Review error logs
- Verify Reddit API usage
- Check email delivery

### Monthly
- Review monitored subreddits
- Check storage space
- Verify all credentials are valid

## Backup and Recovery

### Important Files to Backup
1. `config.json`
2. `.env`
3. `data/` directory

### Recovery Steps
If the system needs to be restored:
1. Ensure all backup files are in place
2. Run `python start.py`
3. Verify system status with `python check-status.py`

## Security Notes

1. Never share your `.env` file or `config.json`
2. Keep your Gmail App Password secure
3. Regularly update your Reddit API credentials
4. Don't share your server access credentials

## Need More Help?

Contact our support team:
- Email: support@nookly.com
- Hours: Monday-Friday, 9 AM - 5 PM EST
- Include any error messages or logs when contacting support 