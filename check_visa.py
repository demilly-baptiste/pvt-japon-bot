import requests
import os
import sys

# Configuration
URL_AMBASSADE = "https://www.fr.emb-japan.go.jp/itpr_fr/v0002b.html"
PHRASE_FERMETURE = "fermé jusqu’à nouvel ordre"

# Récupération des secrets (configurés sur GitHub)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_notification(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Erreur : Les secrets Telegram ne sont pas configurés.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Erreur lors de l'envoi Telegram : {e}")

def check_status():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(URL_AMBASSADE, headers=headers, timeout=20)
        response.raise_for_status()
        
        # On force l'encodage en utf-8 pour éviter les problèmes avec les accents
        response.encoding = 'utf-8'
        html_content = response.text

        if PHRASE_FERMETURE in html_content:
            print("Le système est toujours fermé.")
        else:
            print("ALERTE : La phrase de fermeture n'a pas été trouvée !")
            send_notification("🚨 **PVT JAPON : Changement détecté !**\n\nLa phrase 'fermé jusqu’à nouvel ordre' a disparu de la page de l'ambassade.\n\nVérifie vite : " + URL_AMBASSADE)

    except Exception as e:
        print(f"Erreur lors du check : {e}")
        # Optionnel : envoyer une notification en cas d'erreur technique du script
        # send_notification(f"⚠️ Erreur script PVT : {e}")

if __name__ == "__main__":
    check_status()
