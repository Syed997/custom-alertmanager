import requests, os
from dotenv import load_dotenv

load_dotenv()

TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")

def send_teams_alert(message):
    """Send alert to Microsoft Teams via webhook"""
    payload = {
        "text": f"🚨 Alert from Flask API SigNoz:\n\n{message}"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(TEAMS_WEBHOOK_URL, json=payload, headers=headers)
    return response.status_code == 200