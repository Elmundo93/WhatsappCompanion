# app/utils/twilio_client.py
from twilio.rest import Client
from app.utils.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp_reply(to_number: str, message: str):
    print(f"📤 Sende Antwort an {to_number}: {message}")
    client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        to=to_number,
        body=message
    )