import requests
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


def get_team_id(team_name):
    team_dict = {"FC BARCELONA": 529, "REAL MADRID": 541, "BAYERN MONACHIUM": 157,"Atletico Madrid":530}
    if team_name not in team_dict:
        raise ValueError(f"Unknown team: {team_name}. Add it to team_dict first.")
    return team_dict[team_name]


URL = "https://v3.football.api-sports.io/teams"
API_KEY = os.getenv("FOOTBALL_API_KEY")

headers = {"x-apisports-key": API_KEY}


def get_team_info(team_name):
    params = {"name": team_name}

    try:
        response = requests.get(URL, headers=headers, params=params)
        data = response.json()

        if data["response"]:
            team_id = data["response"][0]["team"]["id"]
            return team_id
        return "Team not found."
    except Exception as e:
        return f"Error: {e}"
