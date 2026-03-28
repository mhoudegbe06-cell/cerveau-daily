import json
import os
import requests
from datetime import datetime

# Charger les secrets
TELEGRAM_TOKEN = os.environ["8738095625:AAGJrCvwy2alSmmyZvxhZ-CoFZuz3X6bwUk"]
TELEGRAM_CHAT_ID = os.environ["6042268454"]

# Charger les lecons pre-generees
with open("lecons.json", "r", encoding="utf-8") as f:
    lecons = json.load(f)

# Determiner la lecon du jour
jour = datetime.now().timetuple().tm_yday
index = (jour - 1) % len(lecons)
lecon = lecons[index]

message = lecon["message"]

# Envoyer sur Telegram
telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
response = requests.post(telegram_url, json={
    "chat_id": TELEGRAM_CHAT_ID,
    "text": message
})

print(f"Sujet envoye : {lecon['sujet']}")
print(f"Telegram status: {response.status_code}")
