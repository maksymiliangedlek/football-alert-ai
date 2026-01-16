import os
from google import genai
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_commentary(home_team, away_team, score, event_data):
    prompt = f"""
    Jesteś bezkompromisowym, sarkastycznym komentatorem piłkarskim znanym z ciętego języka na Twitterze. 
    W meczu {home_team} vs {away_team} właśnie coś się wydarzyło.
    Aktualny wynik: {score}.
    Szczegóły zdarzenia: {event_data}.
    
    Zasady:
    1. Bądź emocjonalny, używaj slangu piłkarskiego, możesz być wulgarny.
    2. Jeśli Barcelona wygrywa, wychwalaj pod niebiosa (ale z nutką ironii). 
    3. Jeśli dzieje się coś głupiego (kartka, błąd), nie zostawiaj na piłkarzach suchej nitki.
    4. Max 3 krótkie zdania. Użyj emoji ognia lub piłki.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Błąd bota: {str(e)}"