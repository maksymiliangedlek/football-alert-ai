import requests
import os
from dotenv import load_dotenv

# Wskazujemy ścieżkę do .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def find_team_id(team_name):
    api_key = os.getenv("FOOTBALL_API_KEY")
    url = "https://api-football-v1.p.rapidapi.com/v3/teams"
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params={"search": team_name})
    data = response.json()
    
    # DEBUG: To nam pokaże co dokładnie wysyła serwer
    print("--- DEBUG DATA START ---")
    print(data)
    print("--- DEBUG DATA END ---")

    if 'response' in data and data['response']:
        for item in data['response']:
            print(f"Nazwa: {item['team']['name']} | ID: {item['team']['id']}")
    elif 'message' in data:
        print(f"Informacja od API: {data['message']}")
    else:
        print("Coś poszło nie tak. Spójrz na sekcję DEBUG powyżej.")

nazwa = input("Wpisz nazwę drużyny: ")
find_team_id(nazwa)