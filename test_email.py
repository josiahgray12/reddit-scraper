from src.core.email_sender import EmailSender

def test_email_sending():
    email_sender = EmailSender()
    # Sample threads for testing
    threads = [
        {
            'post': {
                'title': 'Test Thread 1',
                'subreddit': 'test_subreddit',
                'selftext': 'This is a test thread for email sending.'
            },
            'relevance': {
                'score': 0.8,
                'user_type': 'developer'
            },
            'drafted_response': 'This is a drafted response for the test thread.'
        }
    ]
    try:
        email_sender.send_daily_digest(threads)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

if __name__ == "__main__":
    test_email_sending() 