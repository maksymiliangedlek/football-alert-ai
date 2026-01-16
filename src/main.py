import time
from football_api import get_live_match
from brain import generate_commentary
from discord_bot import send_to_discord

TEAM_ID = [529,541,24] 
last_score = [None,None,None]

print("Bot wystartował...")

while True:
    for id in TEAM_ID:
        match = get_live_match(id)
        
        if match:
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            current_score = f"{match['goals']['home']}:{match['goals']['away']}"
            
            if current_score != last_score[TEAM_ID.index(id)]:
                print(f"Gol! Nowy wynik: {current_score}")
                
                commentary = generate_commentary(home, away, current_score, match['events'])
                
                send_to_discord(f"⚽ GOOOL w meczu {home}!", commentary, current_score)
                
                last_score[[TEAM_ID.index(id)]] = current_score
        else:
            print("Obecnie nie trwa żaden mecz tej drużyny.")

        time.sleep(120)