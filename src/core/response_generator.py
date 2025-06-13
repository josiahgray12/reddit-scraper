"""
Response generator for automatically drafting Reddit responses based on thread content.
"""

from typing import Dict, Any, List, Optional
import re
from .response_templates import (
    PARENT_TEMPLATES,
    TEACHER_TEMPLATES,
    THERAPIST_TEMPLATES,
    FREE_RESOURCES,
    NOOKLY_FEATURES
)
from .claude_client import ClaudeClient

class ResponseGenerator:
    def __init__(self):
        """Initialize the response generator."""
        self.templates = {
            "parent": PARENT_TEMPLATES,
            "teacher": TEACHER_TEMPLATES,
            "therapist": THERAPIST_TEMPLATES
        }
        self.claude_client = ClaudeClient()

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text."""
        # Common keywords to look for
        keywords = [
            "autism", "adhd", "dyslexia", "speech", "therapy",
            "behavior", "emotional", "regulation", "classroom",
            "curriculum", "homeschool", "visual", "schedule"
        ]
        
        found_keywords = []
        text_lower = text.lower()
        for keyword in keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        return found_keywords

    def _determine_template_type(self, thread: Dict[str, Any]) -> str:
        """Determine which template type to use based on thread content."""
        user_type = thread['relevance']['user_type'].lower()
        keywords = self._extract_keywords(thread['post']['selftext'])
        
        if user_type == "parent":
            if "autism" in keywords or "adhd" in keywords:
                return "autism_support"
            elif "emotional" in keywords or "regulation" in keywords:
                return "emotional_regulation"
            elif "homeschool" in keywords:
                return "homeschool_help"
        elif user_type == "teacher":
            if "classroom" in keywords or "behavior" in keywords:
                return "classroom_management"
            elif "curriculum" in keywords:
                return "curriculum_planning"
        elif user_type == "therapist":
            if "speech" in keywords:
                return "speech_therapy"
            elif "behavior" in keywords:
                return "behavior_management"
        
        # Default to first template in the user type's templates
        return list(self.templates[user_type].keys())[0]

    def _get_relevant_resources(self, keywords: List[str]) -> tuple:
        """Get relevant free resources based on keywords."""
        # Map keywords to resource types
        resource_map = {
            "autism": ["visual_schedules", "parent_support"],
            "adhd": ["visual_schedules", "emotional_regulation"],
            "speech": ["speech_activities"],
            "behavior": ["behavior_tracking"],
            "emotional": ["emotional_regulation"],
            "classroom": ["curriculum_planning"],
            "curriculum": ["curriculum_planning"],
            "homeschool": ["curriculum_planning", "parent_support"]
        }
        
        # Get resources for each keyword
        resources = []
        for keyword in keywords:
            if keyword in resource_map:
                resources.extend(resource_map[keyword])
        
        # Remove duplicates and get unique resources
        resources = list(set(resources))
        
        # Return two resources, or pad with defaults if needed
        if len(resources) >= 2:
            return FREE_RESOURCES[resources[0]], FREE_RESOURCES[resources[1]]
        elif len(resources) == 1:
            return FREE_RESOURCES[resources[0]], FREE_RESOURCES["parent_support"]
        else:
            return FREE_RESOURCES["parent_support"], FREE_RESOURCES["visual_schedules"]

    def _get_relevant_feature(self, keywords: List[str]) -> str:
        """Get relevant Nookly feature based on keywords."""
        # Map keywords to features
        feature_map = {
            "autism": "visual_schedules",
            "adhd": "emotional_regulation",
            "speech": "speech_activities",
            "behavior": "behavior_tracking",
            "emotional": "emotional_regulation",
            "classroom": "curriculum_planning",
            "curriculum": "curriculum_planning",
            "homeschool": "curriculum_planning"
        }
        
        # Find the first matching feature
        for keyword in keywords:
            if keyword in feature_map:
                return NOOKLY_FEATURES[feature_map[keyword]]
        
        # Default to visual schedules if no match
        return NOOKLY_FEATURES["visual_schedules"]

    def _get_child_pronoun(self, text: str) -> str:
        """Extract child's pronoun from text."""
        # Look for common patterns indicating child's gender
        if re.search(r'\b(he|him|his)\b', text.lower()):
            return "him"
        elif re.search(r'\b(she|her|hers)\b', text.lower()):
            return "her"
        return "them"  # Default to gender-neutral

    def generate_response(self, thread: Dict[str, Any]) -> Optional[str]:
        """Generate a response for the given thread."""
        if thread['relevance']['score'] < 6:
            return None

        user_type = thread['relevance']['user_type'].lower()
        if user_type not in self.templates:
            return None

        # Extract information from thread
        text = thread['post']['selftext']
        keywords = self._extract_keywords(text)
        pain_points = thread['relevance'].get('pain_points', [])

        # Use Claude to generate responses
        responses = self.claude_client.generate_responses(
            thread_content=thread,
            user_type=user_type,
            pain_points=pain_points
        )

        if responses and len(responses) > 0:
            # Use the highest-scoring response
            best_response = max(responses, key=lambda x: x['score'])
            return best_response['text'].strip()
        else:
            # Fallback to template-based response if Claude fails
            template_type = self._determine_template_type(thread)
            template = self.templates[user_type].get(template_type)
            if not template:
                return None

            resource1, resource2 = self._get_relevant_resources(keywords)
            feature = self._get_relevant_feature(keywords)
            
            template_vars = {
                'specific_issue': keywords[0] if keywords else "these challenges",
                'specific_situation': keywords[0] if keywords else "facing these challenges",
                'specific_need': keywords[0] if keywords else "your needs",
                'free_resource_1': resource1,
                'free_resource_2': resource2,
                'specific_feature': feature,
                'child_pronoun': self._get_child_pronoun(text)
            }

            try:
                response = template.format(**template_vars)
                return response.strip()
            except KeyError as e:
                print(f"Error filling template: {str(e)}")
                return None 