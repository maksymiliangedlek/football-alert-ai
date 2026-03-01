import os
from google import genai
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_commentary(home_team, away_team, your_team, score, event_data):
    prompt = f"""
    You are an uncompromising, sarcastic football commentator known for your sharp tongue on Twitter. 
    Something just happened in the {home_team} vs {away_team} match.
    Current score: {score}.
    Event details: {event_data}.
    
    Rules:
    1. You are a fan of {your_team}.
    2. Be emotional and use football slang.
    3. If {your_team} is winning, praise them to the skies (but with a hint of irony). 
    4. If something stupid happens (a card, a mistake), don't hold back and roast the players.
    5. Max 3 short sentences. Use fire or football emojis.
    6. If it's a substitution, the mentioned player is the one leaving the pitch.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt,
            config={
                'temperature': 0.8, 
                'max_output_tokens': 150
            }
        )
        return response.text
    except Exception as e:
        return f"Bot error: {str(e)}"