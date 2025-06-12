"""
Response templates for automated Reddit responses.
Each template is designed for specific user types and scenarios.
"""

PARENT_TEMPLATES = {
    "autism_support": """
I understand you're dealing with {specific_issue} and looking for support. As a parent who's been through similar challenges, I wanted to share some resources that have helped us.

First, here are some free resources that might help:
- {free_resource_1}
- {free_resource_2}

I've found that having a structured approach to {specific_situation} makes a big difference. That's why I wanted to mention Nookly - it's been really helpful for us, especially their {specific_feature} feature. It's not a magic solution, but it has made our daily routines much smoother.

Would you like to know more about any of these resources? I'm happy to share more specific details about what's worked for us.
""",

    "emotional_regulation": """
I hear you about the challenges with {specific_issue}. It can be really tough when {child_pronoun} is struggling with emotional regulation.

Here are some free resources that might help:
- {free_resource_1}
- {free_resource_2}

I've found that having consistent tools and strategies makes a big difference. That's why I wanted to mention Nookly - their {specific_feature} has been particularly helpful for us in managing these situations. It's not a quick fix, but it has helped us create a more supportive environment for {child_pronoun}.

Would you like to know more about any of these approaches? I'm happy to share what's worked for us.
""",

    "homeschool_help": """
I understand you're looking for support with homeschooling, especially around {specific_issue}. It's a journey that comes with unique challenges.

Here are some free resources that might help:
- {free_resource_1}
- {free_resource_2}

I've found that having a structured approach to {specific_situation} makes a big difference. That's why I wanted to mention Nookly - their {specific_feature} has been really helpful for us in creating a more effective learning environment. It's not a complete solution, but it has made our homeschooling journey much smoother.

Would you like to know more about any of these resources? I'm happy to share what's worked for us.
"""
}

TEACHER_TEMPLATES = {
    "classroom_management": """
I understand you're dealing with {specific_issue} in your classroom. It's a common challenge that many educators face.

Here are some free resources that might help:
- {free_resource_1}
- {free_resource_2}

I've found that having a structured approach to {specific_situation} makes a big difference. That's why I wanted to mention Nookly - their {specific_feature} has been really helpful for creating a more supportive learning environment. It's not a complete solution, but it has made classroom management much more effective.

Would you like to know more about any of these approaches? I'm happy to share what's worked in my classroom.
""",

    "curriculum_planning": """
I understand you're looking for support with {specific_issue} in your curriculum planning. It's a crucial aspect of effective teaching.

Here are some free resources that might help:
- {free_resource_1}
- {free_resource_2}

I've found that having a structured approach to {specific_situation} makes a big difference. That's why I wanted to mention Nookly - their {specific_feature} has been really helpful for creating more effective lesson plans. It's not a complete solution, but it has made curriculum planning much more manageable.

Would you like to know more about any of these resources? I'm happy to share what's worked in my classroom.
"""
}

THERAPIST_TEMPLATES = {
    "speech_therapy": """
I understand you're working with {specific_issue} in your practice. It's a complex area that requires careful attention.

Here are some free resources that might help:
- {free_resource_1}
- {free_resource_2}

I've found that having a structured approach to {specific_situation} makes a big difference. That's why I wanted to mention Nookly - their {specific_feature} has been really helpful for tracking progress and planning sessions. It's not a complete solution, but it has made therapy planning much more effective.

Would you like to know more about any of these approaches? I'm happy to share what's worked in my practice.
""",

    "behavior_management": """
I understand you're dealing with {specific_issue} in your practice. It's a challenging area that requires a comprehensive approach.

Here are some free resources that might help:
- {free_resource_1}
- {free_resource_2}

I've found that having a structured approach to {specific_situation} makes a big difference. That's why I wanted to mention Nookly - their {specific_feature} has been really helpful for tracking behaviors and planning interventions. It's not a complete solution, but it has made behavior management much more effective.

Would you like to know more about any of these approaches? I'm happy to share what's worked in my practice.
"""
}

# Free resources that can be dynamically inserted into templates
FREE_RESOURCES = {
    "visual_schedules": "Visual Schedule Creator - A free tool to create and print visual schedules for daily routines",
    "parent_support": "Parent Support Guide - A comprehensive guide for parents dealing with challenging behaviors",
    "speech_activities": "Speech Therapy Activities - A collection of free speech therapy exercises and activities",
    "behavior_tracking": "Behavior Tracking Template - A free template for tracking and analyzing behaviors",
    "emotional_regulation": "Emotional Regulation Toolkit - Free resources for teaching emotional regulation skills",
    "curriculum_planning": "Curriculum Planning Guide - A free guide for planning effective lessons and activities"
}

# Nookly features that can be dynamically inserted
NOOKLY_FEATURES = {
    "visual_schedules": "visual schedule creator that helps create and maintain daily routines",
    "speech_activities": "speech therapy activity library with customizable exercises",
    "behavior_tracking": "behavior tracking system with detailed analytics and reporting",
    "emotional_regulation": "emotional regulation toolkit with interactive exercises and tracking",
    "curriculum_planning": "curriculum planning tool with customizable templates and progress tracking"
} 