import json
import os
import requests
from datetime import datetime

# Charger les secrets
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# Charger les sujets
with open("sujets.json", "r", encoding="utf-8") as f:
    sujets = json.load(f)

# Déterminer le sujet du jour
jour = datetime.now().timetuple().tm_yday
index = (jour - 1) % len(sujets)
sujet_du_jour = sujets[index]

numero = sujet_du_jour["numero"]
sujet = sujet_du_jour["sujet"]
domaine = sujet_du_jour["domaine"]

# Générer le contenu avec Gemini
prompt = f"""Tu es un professeur passionnant. Explique le sujet suivant en français de manière claire et engageante.

Sujet : {sujet}
Domaine : {domaine}

Réponds EXACTEMENT dans ce format :

📚 SUJET DU JOUR #{numero}/67
{domaine}

🎯 {sujet}

📖 DÉFINITION
[Une définition claire en 2-3 phrases]

🔍 DESCRIPTION COMPLÈTE
[Une explication détaillée de 150-200 mots, accessible à tous]

💡 EXEMPLES CONCRETS
Exemple 1 : [Exemple du quotidien très simple]
Exemple 2 : [Autre exemple pratique]
Exemple 3 : [Exemple lié à la vie en Afrique/Bénin si possible]

🧠 CE QU'IL FAUT RETENIR
[1 phrase clé à mémoriser]"""

gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

gemini_response = requests.post(gemini_url, json={
    "contents": [{"parts": [{"text": prompt}]}]
})

data = gemini_response.json()

# Afficher la réponse pour déboguer
print("Réponse Gemini:", json.dumps(data, indent=2, ensure_ascii=False))

# Vérifier si candidates existe
if "candidates" not in data:
    error_msg = data.get("error", {}).get("message", "Erreur inconnue")
    print(f"Erreur Gemini: {error_msg}")
    exit(1)

message = data["candidates"][0]["content"]["parts"][0]["text"]

# Envoyer sur Telegram
telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
response = requests.post(telegram_url, json={
    "chat_id": TELEGRAM_CHAT_ID,
    "text": message,
    "parse_mode": "Markdown"
})

print(f"✅ Message envoyé : {sujet}")
print(f"Telegram status: {response.status_code}")
