import requests
import os
import smtplib
from email.message import EmailMessage

# Configuration
URL_AMBASSADE = "https://www.fr.emb-japan.go.jp/itpr_fr/v0002b.html"
PHRASE_FERMETURE = "fermé jusqu’à nouvel ordre"

# Récupération des secrets
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

def send_email(subject, body):
    if not EMAIL_USER or not EMAIL_PASSWORD:
        print("Erreur : Les identifiants email ne sont pas configurés.")
        return

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_RECEIVER

    try:
        # Connexion au serveur SMTP de Gmail (port 465 pour SSL)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email envoyé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")

def check_status():
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
    }
    
    try:
        # On fait une première requête sur la page d'accueil pour obtenir les cookies éventuels
        session.get("https://www.fr.emb-japan.go.jp/", headers=headers, timeout=20)
        
        # Ensuite on va sur la page spécifique
        response = session.get(URL_AMBASSADE, headers=headers, timeout=20)
        response.raise_for_status()
        response.encoding = 'utf-8'
        html_content = response.text

        if PHRASE_FERMETURE in html_content:
            print("Le système est toujours fermé.")
            subject = "Le système est toujours fermé."
            body = f"La phrase '{PHRASE_FERMETURE}' apparaît encore sur la page.\n\nVérifiez ici : {URL_AMBASSADE}"
            send_email(subject, body)
        else:
            print("ALERTE : Changement détecté !")
            subject = "🚨 ALERTE PVT JAPON : Créneaux disponibles ?"
            body = f"La phrase '{PHRASE_FERMETURE}' n'apparaît plus sur la page.\n\nVérifiez ici : {URL_AMBASSADE}"
            send_email(subject, body)

    except Exception as e:
        print(f"Erreur lors du check : {e}")

if __name__ == "__main__":
    check_status()
