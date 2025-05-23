from flask import Flask, request, abort
from twilio.twiml.messaging_response import MessagingResponse
from matcher import find_matches
from utils import is_valid_whatsapp_request, init_logger
import logging

app = Flask(__name__)
logger = init_logger()

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    from_number = request.form.get("From")
    message_body = request.form.get("Body")

    if not message_body or not from_number:
        logger.warning("Invalid request: missing body or from number")
        abort(400)

    logger.info(f"Incoming WhatsApp from {from_number}: {message_body}")

    response = MessagingResponse()
    reply = response.message()

    if "start" in message_body.lower():
        reply.body("👋 Willkommen bei 'Wir helfen aus e.V.'!
Bitte beschreibe kurz, wie du helfen möchtest oder wobei du Hilfe suchst.")
        return str(response)

    matches = find_matches(message_body)

    if matches:
        match_text = "\n".join(matches)
        reply.body(f"🔍 Ich habe folgende passende Kontakte gefunden:\n{match_text}")
    else:
        reply.body("❌ Leider habe ich aktuell keine passenden Kontakte gefunden. Bitte versuche es später erneut.")

    return str(response)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)