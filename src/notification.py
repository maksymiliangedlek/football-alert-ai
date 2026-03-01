import os
import requests
import subprocess


def send_all_notifications(title, message, score, subtitle):
    # MAC
    apple_script = (
        f'display notification "{message}" with title "{title}" subtitle "{subtitle}"'
    )
    try:
        subprocess.run(["osascript", "-e", apple_script], check=True)
    except Exception as e:
        print(f"macOS notification error: {e}")

    # DISCORD
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if webhook_url:
        payload = {
            "embeds": [{
                "title": title,
                "description": message,
                "color": 15158332,
                "fields": [{"name": "Current score", "value": f"**{score}**"}]
            }]
        }
        resp = requests.post(webhook_url, json=payload)
        if not resp.ok:
            print(f"Discord notification error: {resp.status_code} {resp.text}")