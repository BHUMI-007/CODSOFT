import re
import random
from datetime import datetime

# ─────────────────────────────────────────
#  RULE ENGINE — add/edit rules here
# ─────────────────────────────────────────

RULES = [
    {
        "tag": "greeting",
        "patterns": [r"\b(hi|hello|hey|howdy|hiya|good morning|good evening)\b"],
        "responses": [
            "Hello! I'm RuleBot 🤖 How can I help you today?",
            "Hey there! Great to meet you. What's on your mind?",
            "Hi! I'm a rule-based chatbot. Ask me anything!"
        ]
    },
    {
        "tag": "name",
        "patterns": [r"\b(your name|who are you|what are you|introduce yourself)\b"],
        "responses": [
            "I'm RuleBot — a chatbot built using rule-based pattern matching in Python!",
            "My name is RuleBot! I use regex patterns and if-else logic to understand you."
        ]
    },
    {
        "tag": "how_are_you",
        "patterns": [r"\b(how are you|how r u|you okay|you good|how do you do)\b"],
        "responses": [
            "I'm just code, but I'm doing great! How about you?",
            "Running perfectly! All my if-else rules are working fine 😄"
        ]
    },
    {
        "tag": "joke",
        "patterns": [r"\b(joke|funny|make me laugh|tell me something funny)\b"],
        "responses": [
            "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
            "Why did the chatbot go to school? To improve its NLP! 📚",
            "I told my computer I needed a break... now it won't stop sending me Kit-Kat ads.",
            "What do you call a chatbot with no rules? Undefined behavior! 😄"
        ]
    },
    {
        "tag": "ai_info",
        "patterns": [r"\b(what is ai|artificial intelligence|what is nlp|natural language processing|what is ml|machine learning)\b"],
        "responses": [
            "AI is the simulation of human intelligence in machines. NLP (Natural Language Processing) helps computers understand human language — I'm a basic example of that!",
            "NLP = Natural Language Processing. It lets machines read, understand, and respond to text. Rule-based bots like me are the simplest form of NLP!"
        ]
    },
    {
        "tag": "help",
        "patterns": [r"\b(help|what can you do|commands|features|options)\b"],
        "responses": [
            "I can: 👋 Greet you | 😄 Tell jokes | 🤖 Explain AI/NLP | 💻 Talk about programming | 👋 Say goodbye. Try: 'Tell me a joke' or 'What is AI?'"
        ]
    },
    {
        "tag": "programming",
        "patterns": [r"\b(programming|coding|code|python|javascript|software|developer)\b"],
        "responses": [
            "I love programming! I'm built in Python using Flask. Rule-based bots are a great starting point for learning NLP.",
            "Python is awesome for building chatbots! You can start with rules like me, then move to ML-based bots using libraries like NLTK or spaCy."
        ]
    },
    {
        "tag": "thanks",
        "patterns": [r"\b(thank you|thanks|thx|ty|thank u|cheers|appreciated)\b"],
        "responses": [
            "You're welcome! 😊",
            "Happy to help!",
            "Anytime! That's what I'm here for."
        ]
    },
    {
        "tag": "goodbye",
        "patterns": [r"\b(bye|goodbye|see you|cya|take care|later|good night)\b"],
        "responses": [
            "Goodbye! It was great chatting with you! 👋",
            "See you later! Come back anytime.",
            "Take care! Bye bye! 😊"
        ]
    },
    {
        "tag": "time",
        "patterns": [r"\b(time|what time|current time)\b"],
        "responses": ["__TIME__"]   # special — filled dynamically
    },
    {
        "tag": "age",
        "patterns": [r"\b(how old|your age|when were you made|when were you built)\b"],
        "responses": [
            "I was just created! I'm a fresh rule-based chatbot built for an internship project 🎓"
        ]
    }
]

FALLBACKS = [
    "Hmm, I didn't quite catch that. Try asking about AI, jokes, or programming!",
    "I'm not sure how to respond — I only understand specific patterns. Type 'help' to see what I can do.",
    "That's outside my rulebook! Try: 'Tell me a joke' or 'What is AI?'",
    "My pattern matching didn't find a match. Can you rephrase that?"
]


# ─────────────────────────────────────────
#  CORE FUNCTIONS
# ─────────────────────────────────────────

def preprocess(text):
    """Normalize input: lowercase and strip extra spaces."""
    return text.lower().strip()


def match_rule(text):
    """
    Check user input against all rules using regex pattern matching.
    Returns the matched rule's tag and a response, or None if no match.
    """
    processed = preprocess(text)

    for rule in RULES:
        for pattern in rule["patterns"]:
            if re.search(pattern, processed):
                response = random.choice(rule["responses"])

                # Handle dynamic responses
                if response == "__TIME__":
                    response = f"The current time is {datetime.now().strftime('%I:%M %p')} ⏰"

                return {
                    "tag": rule["tag"],
                    "response": response,
                    "matched_pattern": pattern
                }

    return None


def get_response(user_input):
    """
    Main function — takes user input, returns bot response dict.
    This is what Flask will call.
    """
    if not user_input or not user_input.strip():
        return {"response": "Please type something!", "tag": "empty"}

    result = match_rule(user_input)

    if result:
        return {"response": result["response"], "tag": result["tag"]}
    else:
        return {"response": random.choice(FALLBACKS), "tag": "fallback"}