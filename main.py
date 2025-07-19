import requests
import time
import telegram
from bs4 import BeautifulSoup

# Ton token et ID Telegram
TELEGRAM_TOKEN = "7840863675:AAETQXyAkyJv4JgqsNbhMyDnDpAQ6B7lrVM"
CHAT_ID = 902064209

# Initialiser le bot
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# URL à surveiller
CROUS_URL = "https://trouverunlogement.lescrous.fr/tools/search/logement?type%5B%5D=1&location=Clermont-Ferrand"

# Dernier titre vu
dernier_titre = ""

def verifier_disponibilite():
    global dernier_titre

    try:
        response = requests.get(CROUS_URL, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        logements = soup.select(".search-logement-title")

        if logements:
            titre = logements[0].text.strip()

            if titre != dernier_titre:
                message = f"🏠 Nouveau logement à Clermont-Ferrand : {titre}"
                bot.send_message(chat_id=CHAT_ID, text=message)
                dernier_titre = titre
            else:
                print("Pas de nouveau logement.")
        else:
            print("Aucun logement trouvé.")
    except Exception as e:
        print(f"Erreur lors de la vérification : {e}")

# Boucle infinie (vérifie toutes les 5 minutes)
print("🤖 Bot lancé... Surveillance en cours.")
while True:
    verifier_disponibilite()
    time.sleep(300)  # 5 minutes
