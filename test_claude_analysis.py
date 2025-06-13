import asyncio
from src.core.relevance_analyzer import RelevanceAnalyzer
from src.utils.logger import Logger
import json

async def test_claude_analysis():
    """Test Claude integration in the relevance analyzer."""
    logger = Logger()
    analyzer = RelevanceAnalyzer()
    
    # Load config to get the new model name
    with open('config.json', 'r') as f:
        config = json.load(f)
    new_model = config['claude']['model']
    
    # Test thread content
    test_thread = {
        "title": "Struggling with my 5-year-old's emotional outbursts",
        "content": """
        My 5-year-old has been having frequent meltdowns at home and school. His teacher suggested he might need more support with emotional regulation. We've tried visual schedules and social stories, but nothing seems to work consistently. I'm at my wit's end and looking for any advice or resources that might help.
        
        We've been using some apps like Boardmaker and a visual schedule app, but they're not really helping with the emotional part. I'm worried about his transition to kindergarten next year if we can't get this under control.
        """,
        "comments": [
            "Have you tried using a feelings chart? That helped my daughter a lot.",
            "Consider talking to a child psychologist. Early intervention is key.",
            "We use a social-emotional learning app that's been helpful for our son with ADHD."
        ]
    }
    
    try:
        logger.info("Testing Claude analysis...")
        relevance = analyzer.analyze_thread(test_thread["content"], test_thread["comments"])
        
        # Print analysis results
        print("\nAnalysis Results:")
        print(f"Total Score: {relevance.total_score}")
        print(f"User Type: {relevance.user_type.value}")
        print(f"Pain Points: {', '.join(relevance.pain_points)}")
        print(f"Keywords Found: {', '.join(relevance.keywords_found)}")
        print(f"Sentiment Score: {relevance.sentiment_score}")
        print(f"Age Relevant: {relevance.age_relevance}")
        print(f"Urgency Level: {relevance.urgency_level}")
        print(f"Competitive Mentions: {', '.join(relevance.competitive_mentions)}")
        
        logger.info("Claude analysis test completed successfully")
        
    except Exception as e:
        logger.error("Error testing Claude analysis", e)
        raise

if __name__ == "__main__":
    asyncio.run(test_claude_analysis()) 