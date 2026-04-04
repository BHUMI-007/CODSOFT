# RuleBot — Rule-Based Chatbot 🤖

A simple rule-based chatbot built with **Python + Flask** that uses
**regex pattern matching** and **if-else logic** to respond to user queries.

## Features
- Pattern matching using Regular Expressions (regex)
- Rule-based NLP with tagged intents
- Multiple responses per rule (randomized)
- Dynamic responses (e.g., current time)
- Clean web interface with Flask

## Tech Stack
- Python 3.x
- Flask (web server)
- HTML / CSS / JavaScript (frontend)

## Project Structure
```
rule-based-chatbot/
├── app.py          → Flask web server
├── chatbot.py      → Rule engine & pattern matching
├── templates/
│   └── index.html  → Chat UI
├── static/
│   ├── style.css
│   └── script.js
└── requirements.txt
```

## How to Run
```bash
git clone https://github.com/YOUR_USERNAME/rule-based-chatbot
cd rule-based-chatbot
pip install -r requirements.txt
python app.py
```

Then open: `http://127.0.0.1:5000`

## How It Works

1. User sends a message via the browser
2. Flask receives it at the `/chat` POST endpoint
3. `chatbot.py` normalizes the text (lowercase, strip)
4. Each rule's regex pattern is tested against the input
5. First matching rule's response is returned (randomized)
6. If no match → fallback response

## Internship Project
Built as part of internship training on NLP basics and chatbot development.