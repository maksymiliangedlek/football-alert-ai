import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": os.getenv("FOOTBALL_API_KEY")}


def get_live_match_data(team_id):
    url = f"{BASE_URL}/fixtures"
    params = {
        "team": team_id,
        "live": "all"
    }

    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        data = response.json()

        if data.get("response"):
            return data["response"][0]
        else:
            return None

    except Exception as e:
        print(f"API Error: {e}")
        return None


def get_match_events(fixture_id):
    url = f"{BASE_URL}/fixtures/events"
    params = {"fixture": fixture_id}

    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    data = response.json()

    return data.get("response", [])