import requests
import os

def send_to_discord(title, description, score):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    payload = {
        "embeds": [{
            "title": title,
            "description": description,
            "color": 15158332,
            "fields": [
                {"name": "Wynik", "value": f"**{score}**", "inline": True}
            ],
            "footer": {"text": "Live Football Update via Gemini AI"}
        }]
    }
    
    requests.post(webhook_url, json=payload)