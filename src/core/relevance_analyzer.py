import re
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter
from src.utils.logger import Logger

# Download required NLTK data
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

class UserType(Enum):
    PARENT = "parent"
    TEACHER = "teacher"
    THERAPIST = "therapist"
    ADMINISTRATOR = "administrator"
    OTHER = "other"

@dataclass
class RelevanceScore:
    total_score: float
    user_type: UserType
    pain_points: List[str]
    keywords_found: List[str]
    sentiment_score: float
    age_relevance: bool
    urgency_level: str
    competitive_mentions: List[str]

class RelevanceAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        
        # High-value keywords (2 points each)
        self.high_value_terms = {
            "visual schedule": 2,
            "social story": 2,
            "autism": 2,
            "speech therapy": 2,
            "special needs": 2,
            "IEP": 2,
            "504": 2,
            "personalized learning": 2,
            "inclusive books": 2,
            "representation": 2,
            "SEL": 2,
            "emotional regulation": 2,
            "one-size-fits-all": 2,
            "screen time": 2,
            "teacher burnout": 2,
            "resource preparation": 2,
            "diverse materials": 2,
            "inclusive materials": 2,
            "personalized approach": 2,
            "social-emotional": 2,
            "speech therapy resources": 2,
            "autism support": 2,
            "ADHD support": 2,
            "transition": 2,
            "routine": 2,
            "visual supports": 2
        }
        
        # Medium-value keywords (1 point each)
        self.medium_value_terms = {
            "preschool": 1,
            "kindergarten": 1,
            "early childhood": 1,
            "toddler": 1,
            "bedtime stories": 1,
            "learning differences": 1,
            "homeschool": 1,
            "teacher resources": 1,
            "educational tools": 1,
            "screen time management": 1,
            "neurodivergent": 1,
            "preschool readiness": 1,
            "reading difficulties": 1,
            "behavior management": 1
        }
        
        # Problem indicators (3 points each)
        self.problem_indicators = {
            "struggling with": 3,
            "need help": 3,
            "at my wit's end": 3,
            "nothing works": 3,
            "looking for": 3,
            "recommendations": 3,
            "difficulty": 3,
            "challenge": 3,
            "frustrated": 3,
            "overwhelmed": 3
        }
        
        # Age patterns
        self.age_patterns = [
            r"\b[2-8]\s*year\s*old",
            r"age\s*[2-8]",
            r"preschool",
            r"kindergarten",
            r"early learner",
            r"young child"
        ]
        
        # User type indicators
        self.user_type_indicators = {
            UserType.PARENT: ["my child", "my kid", "parent", "mom", "dad"],
            UserType.TEACHER: ["my students", "classroom", "teacher", "educator"],
            UserType.THERAPIST: ["client", "patient", "therapy", "therapist", "SLP", "OT"],
            UserType.ADMINISTRATOR: ["school", "district", "principal", "admin"]
        }
        
        # Competitive intelligence terms
        self.competitive_terms = [
            "boardmaker",
            "social stories app",
            "visual schedule app",
            "autism app",
            "speech therapy app",
            "educational app",
            "learning app"
        ]

    def analyze_thread(self, post_content: str, comments_content: List[str]) -> RelevanceScore:
        """Analyze a thread's relevance to Nookly's business model."""
        # Combine post and comments for analysis
        full_content = post_content + " " + " ".join(comments_content)
        
        # Calculate base score from keywords
        keyword_score = self._calculate_keyword_score(full_content)
        
        # Detect user type
        user_type = self._detect_user_type(full_content)
        
        # Find pain points
        pain_points = self._identify_pain_points(full_content)
        
        # Get sentiment score
        sentiment_score = self._analyze_sentiment(full_content)
        
        # Check age relevance
        age_relevance = self._check_age_relevance(full_content)
        
        # Detect urgency
        urgency_level = self._detect_urgency(full_content)
        
        # Find competitive mentions
        competitive_mentions = self._find_competitive_mentions(full_content)
        
        # Calculate final score with adjustments
        final_score = self._calculate_final_score(
            keyword_score,
            sentiment_score,
            age_relevance,
            urgency_level
        )
        
        return RelevanceScore(
            total_score=final_score,
            user_type=user_type,
            pain_points=pain_points,
            keywords_found=self._get_found_keywords(full_content),
            sentiment_score=sentiment_score,
            age_relevance=age_relevance,
            urgency_level=urgency_level,
            competitive_mentions=competitive_mentions
        )

    def _calculate_keyword_score(self, content: str) -> float:
        """Calculate score based on keyword presence."""
        score = 0
        content_lower = content.lower()
        
        # Check high-value terms
        for term, points in self.high_value_terms.items():
            if term in content_lower:
                score += points
        
        # Check medium-value terms
        for term, points in self.medium_value_terms.items():
            if term in content_lower:
                score += points
        
        # Check problem indicators
        for term, points in self.problem_indicators.items():
            if term in content_lower:
                score += points
        
        return score

    def _detect_user_type(self, content: str) -> UserType:
        """Detect the type of user based on content."""
        content_lower = content.lower()
        type_scores = Counter()
        
        for user_type, indicators in self.user_type_indicators.items():
            for indicator in indicators:
                if indicator in content_lower:
                    type_scores[user_type] += 1
        
        if type_scores:
            return type_scores.most_common(1)[0][0]
        return UserType.OTHER

    def _identify_pain_points(self, content: str) -> List[str]:
        """Identify specific pain points mentioned in the content."""
        pain_points = []
        content_lower = content.lower()
        
        for indicator in self.problem_indicators.keys():
            if indicator in content_lower:
                # Extract the sentence containing the pain point
                sentences = content_lower.split('.')
                for sentence in sentences:
                    if indicator in sentence:
                        pain_points.append(sentence.strip())
        
        return pain_points

    def _analyze_sentiment(self, content: str) -> float:
        """Analyze the sentiment of the content."""
        return self.sia.polarity_scores(content)['compound']

    def _check_age_relevance(self, content: str) -> bool:
        """Check if the content mentions relevant age ranges."""
        content_lower = content.lower()
        for pattern in self.age_patterns:
            if re.search(pattern, content_lower):
                return True
        return False

    def _detect_urgency(self, content: str) -> str:
        """Detect the urgency level of the content."""
        content_lower = content.lower()
        urgency_terms = {
            "urgent": 3,
            "emergency": 3,
            "asap": 3,
            "immediately": 3,
            "right away": 3,
            "desperate": 2,
            "need help now": 2,
            "struggling": 2
        }
        
        max_urgency = 0
        for term, level in urgency_terms.items():
            if term in content_lower:
                max_urgency = max(max_urgency, level)
        
        if max_urgency >= 3:
            return "high"
        elif max_urgency >= 2:
            return "medium"
        return "low"

    def _find_competitive_mentions(self, content: str) -> List[str]:
        """Find mentions of competitors or alternative solutions."""
        content_lower = content.lower()
        mentions = []
        
        for term in self.competitive_terms:
            if term in content_lower:
                mentions.append(term)
        
        return mentions

    def _calculate_final_score(self, keyword_score: float, sentiment_score: float,
                             age_relevance: bool, urgency_level: str) -> float:
        """Calculate the final relevance score with adjustments."""
        score = keyword_score
        
        # Adjust for sentiment (negative sentiment indicates more urgency)
        if sentiment_score < -0.5:
            score *= 1.2
        
        # Adjust for age relevance
        if age_relevance:
            score *= 1.1
        
        # Adjust for urgency
        if urgency_level == "high":
            score *= 1.3
        elif urgency_level == "medium":
            score *= 1.1
        
        # Cap the score at 10
        return min(score, 10)

    def _get_found_keywords(self, content: str) -> List[str]:
        """Get list of found keywords in the content."""
        content_lower = content.lower()
        found_keywords = []
        
        # Check all keyword categories
        for term in self.high_value_terms.keys():
            if term in content_lower:
                found_keywords.append(term)
        
        for term in self.medium_value_terms.keys():
            if term in content_lower:
                found_keywords.append(term)
        
        return found_keywords 