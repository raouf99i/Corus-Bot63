import requests
from bs4 import BeautifulSoup
from telegram import Bot
import time
import os

# Utilise les variables d'environnement si tu préfères
TOKEN = "7840863675:AAETQXyAkyJv4JgqsNbhMyDnDpAQ6B7lrVM"
CHAT_ID = "902064209"
URL = "https://trouverunlogement.lescrous.fr/tools/search/logement?type[]=1&location=Clermont-Ferrand"

bot = Bot(token=TOKEN)
derniere_annonce = ""

def check_crous():
    global derniere_annonce
    try:
        response = requests.get(URL, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        annonces = soup.find_all("h2", class_="search-logement-title")

        if annonces:
            titre = annonces[0].get_text(strip=True)
            if titre != derniere_annonce:
                derniere_annonce = titre
                bot.send_message(chat_id=CHAT_ID, text=f"🏠 Nouveau logement : {titre}")
                print(f"Nouveau logement envoyé : {titre}")
            else:
                print("Aucune nouvelle annonce.")
        else:
            print("Aucune annonce trouvée.")
    except Exception as e:
        print(f"Erreur lors de la vérification : {e}")

print("🤖 Bot démarré. Surveillance toutes les 5 minutes.")

while True:
    check_crous()
    time.sleep(300)
