# Infinity AI - Knowledge Chatbot

Infinity AI is a general knowledge chatbot with a focus on India-related information, built with Flask and vanilla JavaScript. It handles various question types with rule-based logic without requiring external APIs.

## Features

- **Knowledge Base**: Extensive information about Indian cities, landmarks, culture, personalities, and more
- **Time & Date Queries**: Supports time/date information for various cities, especially in India
- **Math Calculations**: Performs basic arithmetic operations
- **Jokes & Motivation**: Offers jokes and motivational quotes
- **Modern UI**: Features gradient design, animations, particle effects, and responsive layout
- **Theme Toggle**: Switch between dark and light themes
- **Suggestion Chips**: Quick access to popular topics

## Dependencies

- Python 3.11+
- Flask
- pytz (for timezone support)
- Other dependencies in requirements.txt

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/infinity-ai.git
cd infinity-ai
```

2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```
python main.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Deployment

The application is ready for deployment on any platform that supports Python/Flask applications, such as:

- Heroku
- AWS Elastic Beanstalk
- Google Cloud App Engine
- PythonAnywhere
- Vercel
- Replit

## Project Structure

- `app.py`: Contains the Flask routes and chatbot logic
- `main.py`: Entry point for the application
- `/static`: CSS and JavaScript files
- `/templates`: HTML templates

## How It Works

The chatbot uses a rule-based approach to understanding and responding to user queries:

1. **Pattern Matching**: Identifies keywords and patterns in user messages
2. **Knowledge Base**: Stores predefined responses for common questions
3. **Fallback Responses**: Handles unknown queries gracefully

## Customizing the Chatbot

### Adding Knowledge

To add more information to the chatbot, edit the `knowledge_base` dictionary in `app.py`. For example:

```python
knowledge_base = {
    # Add your new entries here
    "new topic": "Information about the new topic",
    
    # Existing entries below
    "capital of india": "The capital of India is New Delhi...",
}
```

### Adding Features

The chatbot's functionality can be extended by:

1. Adding new condition blocks in the `get_response()` function
2. Creating new collections (like the jokes list) for specific types of responses
3. Implementing regex patterns for more complex query recognition

## License

This project is released under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Built with Flask and vanilla JavaScript
- Uses Bootstrap for styling
- Particles.js for background effects

---

Created with 💜 by [Your Name]