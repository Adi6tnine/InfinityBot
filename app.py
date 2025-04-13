import os
import re
import json
import datetime
import random
import pytz
from flask import Flask, render_template, request, jsonify
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Timezone dictionary for common locations
timezones = {
    # India and cities
    "india": "Asia/Kolkata",
    "delhi": "Asia/Kolkata",
    "mumbai": "Asia/Kolkata",
    "kolkata": "Asia/Kolkata",
    "chennai": "Asia/Kolkata",
    "bangalore": "Asia/Kolkata",
    "bengaluru": "Asia/Kolkata",
    "hyderabad": "Asia/Kolkata",
    "ahmedabad": "Asia/Kolkata",
    "pune": "Asia/Kolkata",
    "jaipur": "Asia/Kolkata",
    "lucknow": "Asia/Kolkata",
    "new delhi": "Asia/Kolkata",
    
    # Other countries
    "us": "US/Eastern",
    "usa": "US/Eastern",
    "uk": "Europe/London",
    "japan": "Asia/Tokyo",
    "australia": "Australia/Sydney",
    "china": "Asia/Shanghai",
    "russia": "Europe/Moscow",
    "brazil": "America/Sao_Paulo",
    "germany": "Europe/Berlin",
    "france": "Europe/Paris",
    "canada": "America/Toronto",
    "mexico": "America/Mexico_City",
    "spain": "Europe/Madrid",
    "italy": "Europe/Rome",
    "south africa": "Africa/Johannesburg",
    "dubai": "Asia/Dubai",
    "uae": "Asia/Dubai",
    "singapore": "Asia/Singapore",
    "new zealand": "Pacific/Auckland"
}

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "infinity-chatbot-secret")

# Knowledge base for responses
knowledge_base = {
    # Geographical questions
    "capital of india": "The capital of India is New Delhi. It is part of the National Capital Territory of Delhi (NCT) and serves as the seat of all three branches of the Government of India.",
    "capital of usa": "The capital of the United States is Washington, D.C.",
    "capital of uk": "The capital of the United Kingdom is London.",
    "capital of australia": "The capital of Australia is Canberra.",
    "capital of canada": "The capital of Canada is Ottawa.",
    "capital of china": "The capital of China is Beijing.",
    "capital of japan": "The capital of Japan is Tokyo.",
    "capital of russia": "The capital of Russia is Moscow.",
    "capital of brazil": "The capital of Brazil is Brasília.",
    "capital of france": "The capital of France is Paris.",
    "capital of germany": "The capital of Germany is Berlin.",
    "capital of italy": "The capital of Italy is Rome.",
    "capital of spain": "The capital of Spain is Madrid.",
    "capital of mexico": "The capital of Mexico is Mexico City.",
    
    # Indian cities
    "mumbai": "Mumbai (formerly known as Bombay) is the capital city of the Indian state of Maharashtra and the financial capital of India. It is the most populous city in India with an estimated population of 20 million.",
    "delhi": "Delhi is a city and union territory of India containing New Delhi, the capital of India. Delhi's urban area is now considered the second-largest in the world.",
    "bangalore": "Bangalore (officially Bengaluru) is the capital of the Indian state of Karnataka. It is known as India's 'Silicon Valley' and is a major center of India's IT industry.",
    "bengaluru": "Bengaluru (formerly known as Bangalore) is the capital of the Indian state of Karnataka. It is known as India's 'Silicon Valley' and is a major center of India's IT industry.",
    "kolkata": "Kolkata (formerly Calcutta) is the capital of the Indian state of West Bengal. It is known for its grand colonial architecture, art galleries, and cultural festivals.",
    "chennai": "Chennai (formerly Madras) is the capital of the Indian state of Tamil Nadu. It is known for its beaches, temples, and being a major center for the South Indian film industry.",
    "hyderabad": "Hyderabad is the capital of the Indian state of Telangana. It is a major center for the IT industry and known for its rich history, food, and multi-lingual culture.",
    "ahmedabad": "Ahmedabad is the largest city in the Indian state of Gujarat. It is known for its textile industry and is a rapidly growing economic and industrial hub.",
    "pune": "Pune is the second-largest city in the state of Maharashtra, after Mumbai. It is known as the 'Oxford of the East' due to the presence of several well-known educational institutions.",
    
    # Indian landmarks
    "taj mahal": "The Taj Mahal is an ivory-white marble mausoleum on the right bank of the river Yamuna in Agra, Uttar Pradesh, India. It was commissioned in 1632 by the Mughal emperor Shah Jahan to house the tomb of his favorite wife, Mumtaz Mahal. It is one of the New Seven Wonders of the World.",
    "india gate": "India Gate is a war memorial located in New Delhi. It was built to honor the soldiers of the British Indian Army who died during the First World War and the Third Anglo-Afghan War.",
    "red fort": "The Red Fort is a historic fort in Old Delhi that served as the main residence of the Mughal Emperors. Built in 1639, it gets its name from its massive red sandstone walls.",
    "gateway of india": "The Gateway of India is an arch monument in Mumbai built during the 20th century. It was erected to commemorate the landing of King George V and Queen Mary at Apollo Bunder in 1911.",
    "golden temple": "The Golden Temple (also known as Sri Harmandir Sahib) is a gurdwara located in Amritsar, Punjab. It is the preeminent spiritual site of Sikhism and one of the most visited tourist destinations in India.",
    "qutub minar": "Qutub Minar is a 73-meter tall minaret built in 1193, located in Delhi. It is a UNESCO World Heritage Site and one of the earliest and most prominent examples of Indo-Islamic architecture.",
    "lotus temple": "The Lotus Temple is a Baháʼí House of Worship located in Delhi. Notable for its flowerlike shape, it serves as the Mother Temple of the Indian subcontinent and has become a prominent attraction in the city.",
    
    # Indian culture
    "indian food": "Indian cuisine consists of a variety of regional and traditional cuisines native to the Indian subcontinent. It features a wide assortment of dishes and cooking techniques, varying significantly by region. Common elements include spices, herbs, vegetables, fruits, and dairy products.",
    "bollywood": "Bollywood is the Hindi-language film industry based in Mumbai (formerly Bombay), India. It is part of the larger Indian cinema industry, which includes other production centers producing films in various regional languages.",
    "cricket in india": "Cricket is the most popular sport in India. The Indian cricket team is governed by the Board of Control for Cricket in India (BCCI), and the team has won the Cricket World Cup twice (1983 and 2011).",
    "yoga": "Yoga is a group of physical, mental, and spiritual practices that originated in ancient India. It is one of India's most successful cultural exports and is practiced worldwide for health and relaxation.",
    "diwali": "Diwali, or Deepavali, is the Hindu festival of lights, usually lasting five days and celebrated during the Hindu lunisolar month Kartika. It is one of the most popular festivals of Hinduism and symbolizes the spiritual 'victory of light over darkness, good over evil'.",
    "holi": "Holi is a popular ancient Hindu festival, also known as the 'Festival of Spring', the 'Festival of Colors', or the 'Festival of Love'. It signifies the triumph of good over evil and the arrival of spring.",
    
    # People and personalities
    "prime minister of india": "The current Prime Minister of India is Narendra Modi. He has been serving as the Prime Minister of India since May 2014.",
    "narendra modi": "Narendra Modi is an Indian politician serving as the 14th and current Prime Minister of India since May 2014. He was the Chief Minister of Gujarat from 2001 to 2014 and is a member of the Bharatiya Janata Party (BJP) and the Rashtriya Swayamsevak Sangh (RSS).",
    "president of india": "The current President of India is Droupadi Murmu. She is the 15th President of India, serving since July 2022, and the second woman to hold the position.",
    "president of usa": "The current President of the United States is Joe Biden. He took office as the 46th president on January 20, 2021.",
    "prime minister of uk": "The current Prime Minister of the United Kingdom is Rishi Sunak. He took office in October 2022 as the first British Asian and Hindu to become UK Prime Minister.",
    "elon musk": "Elon Musk is a business magnate, investor, and entrepreneur. He is the founder, CEO, and chief engineer of SpaceX; CEO and product architect of Tesla, Inc.; founder of The Boring Company; and co-founder of Neuralink and OpenAI. He acquired Twitter (now X) in 2022 and serves as its CEO.",
    "steve jobs": "Steve Jobs (1955-2011) was an American entrepreneur, industrial designer, business magnate, and media proprietor. He was the co-founder, chairman, and CEO of Apple Inc., as well as the chairman and majority shareholder of Pixar.",
    "bill gates": "Bill Gates is an American business magnate, software developer, investor, and philanthropist. He co-founded Microsoft Corporation and served as its chairman, CEO, and chief software architect. He is known for his philanthropy through the Bill & Melinda Gates Foundation.",
    "mark zuckerberg": "Mark Zuckerberg is an American business magnate, internet entrepreneur, and philanthropist. He is known for co-founding Meta Platforms (formerly Facebook, Inc.) and serves as its chairman, CEO, and controlling shareholder.",
    
    # Technical concepts
    "python": "Python is a high-level, interpreted programming language known for its readability and versatility. It's widely used in web development, data science, artificial intelligence, and automation.",
    "javascript": "JavaScript is a high-level, interpreted programming language that is one of the core technologies of the World Wide Web. It enables interactive web pages and is an essential part of web applications.",
    "ai": "AI (Artificial Intelligence) refers to computer systems designed to perform tasks that typically require human intelligence, such as visual perception, speech recognition, decision-making, and language translation.",
    "machine learning": "Machine Learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It uses algorithms and statistical models to analyze patterns in data.",
    "blockchain": "Blockchain is a distributed, decentralized, public ledger technology that records transactions across many computers so that any involved record cannot be altered retroactively, without the alteration of all subsequent blocks.",
    "cloud computing": "Cloud computing is the delivery of computing services—including servers, storage, databases, networking, software, analytics, and intelligence—over the Internet (\"the cloud\") to offer faster innovation, flexible resources, and economies of scale.",
    "big data": "Big data refers to extremely large data sets that may be analyzed computationally to reveal patterns, trends, and associations, especially relating to human behavior and interactions.",
    
    # Science concepts
    "relativity": "Relativity is a theory developed by Albert Einstein that describes the laws of gravity and motion. It consists of two parts: Special Relativity (1905) which deals with the physics of objects moving at constant speeds, and General Relativity (1915) which incorporates gravity and acceleration.",
    "quantum physics": "Quantum physics, also known as quantum mechanics, is a fundamental theory in physics that provides a description of the physical properties of nature at the scale of atoms and subatomic particles.",
    "black hole": "A black hole is a region of spacetime where gravity is so strong that nothing—no particles or even electromagnetic radiation such as light—can escape from it. The boundary of the region from which no escape is possible is called the event horizon.",
    "climate change": "Climate change refers to long-term shifts in temperatures and weather patterns. These shifts may be natural, but since the 1800s, human activities have been the main driver of climate change, primarily due to the burning of fossil fuels which produces heat-trapping gases.",
    
    # Historical questions
    "world war 2": "World War II was a global war that lasted from 1939 to 1945. It involved the vast majority of the world's countries forming two opposing military alliances: the Allies and the Axis powers. It was the deadliest conflict in human history, marked by mass deaths, the Holocaust, and the first use of nuclear weapons.",
    "ancient egypt": "Ancient Egypt was a civilization of ancient North Africa, concentrated along the lower reaches of the Nile River, situated in the place that is now the country Egypt. Ancient Egyptian civilization followed prehistoric Egypt and coalesced around 3100 BC with the political unification of Upper and Lower Egypt.",
    "renaissance": "The Renaissance was a period in European history marking the transition from the Middle Ages to modernity and covering the 15th and 16th centuries. It was characterized by an effort to revive and surpass ideas and achievements of classical antiquity, marked by developments in art, architecture, politics, science, and literature.",
    
    # Advice and motivation
    "study better": "To study better: 1) Create a dedicated study space, 2) Break study sessions into 25-minute focused intervals with short breaks, 3) Use active learning techniques like teaching the material to someone else, 4) Get enough sleep, and 5) Stay hydrated and maintain a healthy diet.",
    "learn coding": "To learn coding: 1) Start with the basics of a beginner-friendly language like Python, 2) Practice regularly with small projects, 3) Use online resources like documentation and tutorials, 4) Join coding communities to ask questions, 5) Build projects that interest you to stay motivated.",
    "stay healthy": "To stay healthy: 1) Maintain a balanced diet rich in fruits, vegetables, and whole grains, 2) Exercise regularly (at least 30 minutes most days), 3) Get 7-9 hours of quality sleep, 4) Stay hydrated, 5) Manage stress through techniques like meditation, and 6) Schedule regular health check-ups.",
    "motivation": [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
        "The secret of getting ahead is getting started. - Mark Twain",
        "It does not matter how slowly you go as long as you do not stop. - Confucius",
        "Quality is not an act, it is a habit. - Aristotle",
        "The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
        "Your time is limited, don't waste it living someone else's life. - Steve Jobs"
    ],
    "meaning of life": "The meaning of life is a philosophical question that has been debated throughout history. Some believe it's about happiness, others about fulfilling one's purpose, contributing to society, or spiritual fulfillment. Ultimately, many philosophers suggest that each person must discover their own meaning."
}

# Jokes collection
jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
    "Why was the math book sad? Because it had too many problems.",
    "What do you call a parade of rabbits hopping backwards? A receding hare-line.",
    "Why don't skeletons fight each other? They don't have the guts.",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "What's the best thing about Switzerland? I don't know, but the flag is a big plus.",
    "How do you organize a space party? You planet!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I would tell you a chemistry joke, but I know I wouldn't get a reaction.",
    "Why did the bicycle fall over? Because it was two tired!",
    "What's orange and sounds like a parrot? A carrot.",
    "Why can't you give Elsa a balloon? Because she will let it go.",
    "I'm reading a book about anti-gravity. It's impossible to put down!",
    "What do you call a fish with no eyes? Fsh.",
    "How do you make a tissue dance? Put a little boogie in it!",
    "What did one ocean say to the other ocean? Nothing, they just waved.",
    "What's the difference between a poorly dressed man on a trampoline and a well-dressed man on a trampoline? Attire."
]

# Fallback responses for when we don't have a specific answer
fallback_responses = [
    "I'm still learning. Try asking something else!",
    "I don't have that information yet, but I'm constantly learning!",
    "Hmm, I'm not sure about that. Could you try asking in a different way?",
    "That's an interesting question! Unfortunately, I don't have the answer right now.",
    "I wish I knew more about that! Is there something else I can help with?",
    "I'm still growing my knowledge base. Could you ask me something else?"
]

@app.route('/')
def index():
    logger.info("Serving index page")
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip().lower()
    
    if not user_message:
        return jsonify({'response': 'Please type a message!'})
    
    logger.info(f"Received message: {user_message}")
    
    # Get the bot's response
    response = get_response(user_message)
    logger.info(f"Sending response: {response}")
    
    return jsonify({'response': response})

def get_response(message):
    # Check for math calculations
    if re.search(r'what is \d+[\+\-\*\/]\d+', message) or re.search(r'\d+[\+\-\*\/]\d+', message):
        try:
            # Extract the math expression
            if 'what is ' in message:
                expression = message.replace('what is ', '')
            else:
                expression = message
                
            # Replace word operators with symbols
            expression = expression.replace('plus', '+').replace('minus', '-')
            expression = expression.replace('times', '*').replace('multiply by', '*')
            expression = expression.replace('divided by', '/').replace('divide by', '/')
            
            # Extract only numbers and operators
            expression = re.sub(r'[^0-9\+\-\*\/\.\(\)]', '', expression)
            
            # Calculate the result
            result = eval(expression)
            # Format result: round to 2 decimal places if it's a float
            if isinstance(result, float):
                # Check if the result is effectively an integer
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 2)
            
            return f"The answer is {result}"
        except Exception as e:
            logger.error(f"Error calculating math expression: {str(e)}")
            return "I couldn't calculate that. Please check the expression."
    
    # Check for date and time queries with timezone support
    if 'time' in message:
        # Check if asking for time in a specific location
        location = None
        for loc in timezones.keys():
            if loc in message:
                location = loc
                break
        
        if location:
            # Get time for specific location
            tz = pytz.timezone(timezones[location])
            current_time = datetime.datetime.now(tz).strftime('%H:%M:%S')
            return f"The current time in {location.title()} is {current_time}"
        elif 'what' in message or 'current' in message or 'now' in message:
            # Default to UTC time if no location specified
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            return f"The current time is {current_time} (UTC)"
    
    if 'date' in message:
        # Check if asking for date in a specific location
        location = None
        for loc in timezones.keys():
            if loc in message:
                location = loc
                break
        
        if location:
            # Get date for specific location
            tz = pytz.timezone(timezones[location])
            current_date = datetime.datetime.now(tz).strftime('%A, %B %d, %Y')
            return f"Today's date in {location.title()} is {current_date}"
        elif 'what' in message or 'current' in message or 'today' in message:
            # Default to UTC date if no location specified
            current_date = datetime.datetime.now().strftime('%A, %B %d, %Y')
            return f"Today's date is {current_date} (UTC)"
    
    # Check for joke request
    if any(word in message for word in ['joke', 'funny', 'make me laugh', 'tell me something funny']):
        return random.choice(jokes)
    
    # Check for greetings
    if any(greeting in message for greeting in ['hello', 'hi', 'hey', 'greetings', 'howdy']):
        greetings = [
            "Hello! I'm Infinity. How can I help you today?",
            "Hi there! What can I assist you with?",
            "Hey! I'm here to answer your questions. What would you like to know?",
            "Greetings! What can I help you discover today?"
        ]
        return random.choice(greetings)
    
    # Check for gratitude
    if any(word in message for word in ['thank', 'thanks', 'appreciate']):
        gratitude_responses = [
            "You're welcome! Feel free to ask if you have more questions.",
            "Glad I could help! What else would you like to know?",
            "My pleasure! Is there anything else you'd like to ask?",
            "Anytime! I'm happy to assist."
        ]
        return random.choice(gratitude_responses)
    
    # Check for introduction questions
    if any(phrase in message for phrase in ['who are you', 'what are you', 'your name', 'about you']):
        return "I'm Infinity AI, a knowledge assistant with expertise in India-related topics. I can provide information about Indian cities, landmarks, culture, and notable people, as well as answer general questions about science, history, and technology. I can also help with calculations, tell jokes, provide current time in different cities, and offer advice. How can I assist you today?"
    
    # Check knowledge base
    for key, value in knowledge_base.items():
        if key in message:
            if isinstance(value, list):
                return random.choice(value)
            return value
    
    # If no specific response is found
    return random.choice(fallback_responses)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
