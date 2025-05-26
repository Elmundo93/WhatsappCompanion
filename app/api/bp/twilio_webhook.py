# app/api/bp/twilio_webhook.py
from flask import Blueprint, request
from app.db.chat_history import save_message, get_history
from app.twilio.dialog_engine import get_next_response
from app.utils.twilio_client import send_whatsapp_reply
from app.utils.utils import is_valid_whatsapp_request

twilio_webhook = Blueprint("twilio_webhook", __name__)

@twilio_webhook.route("/webhook/twilio", methods=["POST"])
def handle_twilio_webhook():
    if not is_valid_whatsapp_request(request):
        return "Invalid request", 400

    user_number = request.form.get("From", "").strip()
    user_message = request.form.get("Body", "").strip()

    if not user_number or not user_message:
        return "Missing data", 400

    # Verlauf speichern
    save_message(user_number, "inbound", user_message)

    # Verlauf holen und nächste Antwort generieren
    history = get_history(user_number)
    reply = get_next_response(user_number, history)

    # Antwort senden und speichern
    send_whatsapp_reply(user_number, reply)
    save_message(user_number, "outbound", reply)

    return "OK", 200