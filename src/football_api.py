import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_live_match(team_id):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {
        "X-RapidAPI-Key": os.getenv("FOOTBALL_API_KEY"),
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    params = {"team": team_id, "live": "all"}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    if data['response']:
        return data['response'][0] 
    return None