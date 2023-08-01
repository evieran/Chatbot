# Function to generate personalized stress relief suggestions
def get_personalized_suggestions(stress_level):
    suggestions = {
        1: "Take a few deep breaths.",
        2: "Listen to some calming music.",
        3: "Go for a walk in nature.",
        4: "Meditate for 10 minutes.",
        5: "Talk to a friend or family member about your stress.",
        6: "Do something you enjoy that helps you relax.",
        7: "Get a massage.",
        8: "Take a hot bath or shower.",
        9: "Read a book or magazine.",
        10: "See a therapist.",
    }

    return suggestions.get(stress_level, "Invalid stress level.")

# Most Common Cognitive Distortions
cognitive_distortions = {
    "black_and_white": {
        "explanation": "Seeing things in only two categories (good or bad, success or failure) without acknowledging any spectrum in between.",
        "reframe": "Consider that things often lie on a spectrum rather than in absolutes."
    },
    "overgeneralization": {
        "explanation": "Making broad interpretations from a single or few events.",
        "reframe": "Recognize that one event does not necessarily represent a consistent pattern."
    },
    "filtering": {
        "explanation": "Focusing on the negative details while ignoring all the positive aspects of a situation.",
        "reframe": "Try to acknowledge and appreciate positive aspects, even in a negative situation."
    },
    "catastrophizing": {
        "explanation": "Exaggerating the importance of insignificant events or mistakes.",
        "reframe": "Ask yourself if the issue will matter in the long term and weigh its actual impact."
    },
    "personalization": {
        "explanation": "Believing that you are the sole cause of every negative event.",
        "reframe": "Understand that not everything is under your control and multiple factors contribute to outcomes."
    },
    "mind_reading": {
        "explanation": "Assuming you know what others are thinking, usually thinking they think negatively of you.",
        "reframe": "Recognize that you cannot read minds and avoid making assumptions without evidence."
    },
    "emotional_reasoning": {
        "explanation": "Believing that your emotions are an accurate reflection of reality.",
        "reframe": "Acknowledge that emotions can sometimes be based on irrational thoughts or biases."
    },
    "should_statements": {
        "explanation": "Having a rigid view of how you or others should behave and getting upset if these rules are not followed.",
        "reframe": "Recognize that people are fallible and that it's more realistic to have preferences rather than rigid expectations."
    },
    "labeling": {
        "explanation": "Assigning global negative traits to yourself and others.",
        "reframe": "Try to view people as complex beings with multiple traits rather than labeling them solely based on specific behaviors."
    },
    "fallacy_of_change": {
        "explanation": "Believing that other people must change in order for you to be happy.",
        "reframe": "Focus on what you can control and change within yourself to improve your well-being."
    }
}

# List of tips or quotes
daily_tips = [
    "Take deep breaths to help alleviate stress.",
    "Remember, thoughts are not always facts.",
    "Challenge your negative thoughts with evidence.",
    "Remember to be kind to yourself today.",
    "You don't have to be perfect to be amazing.",
    "Don't ruin a good today by thinking about a bad yesterday.",
    "You have the power to change your thoughts, and your thoughts have the power to change your life.",
    "Don't be pushed around by your problems. Be led by your dreams.",
    "Take time to do what makes your soul happy.",
    "Believe in yourself and you will be unstoppable.",
]

# List of Challenges
challenges = [
    "Today, try to write down 3 positive things that happened.",
    "Challenge yourself to avoid using absolute words like 'always' or 'never' today.",
    "Try to do something nice for someone else today, no matter how small.",
    "Today, when you find yourself worrying about something, take 5 deep breaths before continuing.",
    "Challenge yourself to engage in a hobby or activity that makes you happy today.",
    "Take a break from social media for the day and focus on real-life interactions.",
    "Practice mindfulness by spending 10 minutes in quiet meditation or reflection.",
    "Set a goal for yourself and take a small step toward achieving it today.",
    "Challenge negative self-talk by replacing it with positive affirmations.",
    "Express gratitude by writing a thank-you note or telling someone you appreciate them."
]
