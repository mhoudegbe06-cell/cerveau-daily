gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

gemini_response = requests.post(gemini_url, json={
    "contents": [{"parts": [{"text": prompt}]}]
})

data = gemini_response.json()

# Afficher la réponse complète pour déboguer
print("Réponse Gemini:", json.dumps(data, indent=2))

# Vérifier si candidates existe
if "candidates" not in data:
    error_msg = data.get("error", {}).get("message", "Erreur inconnue")
    print(f"Erreur Gemini: {error_msg}")
    exit(1)

message = data["candidates"][0]["content"]["parts"][0]["text"]

# Envoyer sur Telegram
telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
requests.post(telegram_url, json={
    "chat_id": TELEGRAM_CHAT_ID,
    "text": message,
    "parse_mode": "Markdown"
})

print(f"✅ Message envoyé : {sujet}")
