import time
import requests
from flask import Flask
from threading import Thread

# === CONFIGURATION ===
BOT_TOKEN = "7840863675:AAETQXyAkyJv4JgqsNbhMyDnDpAQ6B7lrVM"
CHAT_ID = "902064209"
CHECK_INTERVAL = 300  # 5 minutes
CROUS_URL = "https://trouverunlogement.lescrous.fr/tools/4.1.2/search/logements?lieu=Clermont-Ferrand"

# === FUNCTIONS ===
def check_dispo():
    try:
        response = requests.get(CROUS_URL)
        data = response.json()
        return bool(data.get("logements"))
    except Exception as e:
        print("❌ Erreur :", e)
        return False

def envoyer(message):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={
            "chat_id": CHAT_ID,
            "text": message
        })
        print("✅ Message envoyé :", message)
    except Exception as e:
        print("❌ Erreur Telegram :", e)

# === KEEP-ALIVE FLASK SERVER ===
app = Flask('')

@app.route('/')
def home():
    return "✅ Bot CROUS actif"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

# === BOT FUNCTIONALITY ===
envoyer("🚀 Bot lancé et surveille les logements à Clermont-Ferrand")

sent = False
while True:
    dispo = check_dispo()
    if dispo and not sent:
        envoyer("🏠 Logement CROUS dispo ! Va vite voir.")
        sent = True
    elif not dispo:
        sent = False
    time.sleep(CHECK_INTERVAL)
