# Cognitive Distortion Identification Chatbot

This project is a web-based Chatbot built for educational purposes, demonstrating Python, SQL, and Flask skills. 
It aims to identify common cognitive distortions in user inputs and provide constructive feedback and suggestions.

## Features

1. **Thought Input:** Allows users to log in, record their stress levels and input thoughts or statements.
2. **Distortion Identification:** The chatbot analyzes these thoughts and identifies if any common cognitive distortions are present.
3. **Explanation and Education:** Provides explanations of the identified cognitive distortions and their potential negative effects.
4. **Reframing Suggestions:** Suggests more balanced or rational perspectives to think about the situation.
5. **Progress Tracking:** Tracks which distortions are most common for the user over time.
6. **Stress Level Assessment:** Allows users to rate their current stress or anxiety levels.
7. **Personalized Suggestions:** Offers specific techniques for stress relief based on the user’s response.

## Dependencies
To run this project, you need the following Python libraries:

- Flask: A web framework for Python.
- Flask-SQLAlchemy: An extension for Flask that simplifies the use of SQLAlchemy for database operations.
- Flask-Login: A Flask extension that provides user session management.
- Flask-Session: A Flask extension that provides server-side session capabilities.
- Werkzeug: A WSGI utility library for Python, used here for password hashing utilities.
- SQLite: A C library that provides a lightweight disk-based database.

## Limitations
The current implementation for identifying cognitive distortions is simple and might yield many false positives or negatives. 
It's recommended to utilize natural language processing (NLP) techniques or machine learning models for more accurate results in a real-world application.
