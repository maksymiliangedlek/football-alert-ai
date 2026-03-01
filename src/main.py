import time
import sys
from brain import generate_commentary
from notification import send_all_notifications
from football_api import get_live_match_data, get_match_events


TEAM_NAME = "FC BARCELONA"
TEAM_ID = 529  # Hardcoded ID for FC Barcelona ("REAL MADRID": 541, "BAYERN MONACHIUM": 157,"Atletico Madrid":530)

MOCK_MODE = True  

def get_mock_match_data():
    """Returns fake match data without calling the API."""
    return {
        "fixture": {"id": 99999},
        "teams": {
            "home": {"name": "FC BARCELONA"},
            "away": {"name": "VILLAREAL"}
        },
        "goals": {"home": 3, "away": 1}
    }

def get_mock_events():
    """Returns a fake event (e.g., a goal)."""
    return [
        {
            "type": "Goal",
            "detail": "Normal Goal. Hat-trick for Yamal first in career",
            "player": {"name": "Lamine Yamal"},
            "time": {"elapsed": 69}
        }
    ]

def main():
    print(f"🚀 Starting console bot for: {TEAM_NAME} (ID: {TEAM_ID})")
    
    if MOCK_MODE:
        print("⚠️ WARNING: Running in MOCK mode (fake data). Not consuming API limits.\n")

    last_event_id = None

    while True:
        try:
            print(f"[{time.strftime('%H:%M:%S')}] Checking API...")
            
            if MOCK_MODE:
                match_data = get_mock_match_data()
            else:
                match_data = get_live_match_data(TEAM_ID)

            if match_data:
                fixture_id = match_data["fixture"]["id"]
                home_team = match_data['teams']['home']['name']
                away_team = match_data['teams']['away']['name']
                score = f"{match_data['goals']['home']}:{match_data['goals']['away']}"
                
                print(f"Match: {home_team} vs {away_team} ({score})")
                
                if MOCK_MODE:
                    events = get_mock_events()
                else:
                    events = get_match_events(fixture_id)

                if events:
                    event = events[-1]
                    
                    current_event_id = f"{event['type']}_{event.get('detail', '')}_{event.get('player', {}).get('name', '')}_{event['time']['elapsed']}"

                    if current_event_id != last_event_id:
                        p_name = event.get('player', {}).get('name') if event.get('player') else "Unknown"
                        detail = event.get('detail', 'Action')
                        minute = event['time']['elapsed']
                        
                        event_desc = f"{event['type']}: {detail} ({p_name}, {minute} min)"
                        print(f"🔥 New event: {event_desc}")
                        
                        print("🧠 Generating AI commentary...")
                        commentary = generate_commentary(home_team, away_team, TEAM_NAME, score, event_desc)
                        
                        print(f"💬 AI:\n{commentary}\n")
                        
                        print("🔔 Sending notifications (Mac + Discord)...")
                        send_all_notifications(f"EVENT: {home_team} vs {away_team}", commentary, score, event_desc)
                        
                        last_event_id = current_event_id
                        
                        if MOCK_MODE:
                            print("\nMock mode completed successfully. Stopping the script to prevent infinite loops.")
                            break
                    else:
                        print("Event already processed, waiting for the next one.")
                else:
                    print("No events in the match yet.")
            else:
                print("No LIVE match currently.")

        except Exception as e:
            print(f"CRITICAL LOOP ERROR: {e}")

        if MOCK_MODE:
            break

        time.sleep(60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBot stopped manually (Ctrl+C).")
        sys.exit(0)