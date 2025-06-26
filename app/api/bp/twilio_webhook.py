import logging
import time
from flask import Blueprint, request
from app.db.chat_history import save_message, get_history
from app.twilio.dialog_engine import get_next_response
from app.utils.twilio_client import send_whatsapp_reply
from app.utils.utils import is_valid_whatsapp_request
from app.supabase.sync import sync_users_from_supabase
from app.utils.reset_user_state import reset_user_state
from app.services.open_transcripe import transcribe_voice_message

logger = logging.getLogger("twilio_webhook")
twilio_webhook = Blueprint("twilio_webhook", __name__)
# Optional: persistente Lösung (Redis/DB) für produktive Nutzung
# Optional: persistente Lösung für bereits synchronisierte Nutzer (besser wäre Redis)
synced_numbers = set()

@twilio_webhook.route("/webhook/twilio", methods=["POST"])
def handle_twilio_webhook():
    try:
        # 🔐 Request validieren (z. B. Twilio-Signatur)
        if not is_valid_whatsapp_request(request):
            logger.warning("❌ Ungültige Twilio-Anfrage.")
            return "Invalid request", 400

        # 📥 Eingabedaten extrahieren
        user_number = request.form.get("From", "").strip()
        user_message = request.form.get("Body", "").strip()
        num_media = int(request.form.get("NumMedia", 0))
        content_type = request.form.get("MediaContentType0", "")

        if not user_number:
            return "Missing user number", 400

        # 🔄 Reset-Befehl
        if user_message.lower() == "reset":
            reset_user_state(user_number)
            send_whatsapp_reply(user_number, "🔄 Dein Verlauf wurde zurückgesetzt. Schreib mir einfach erneut.")
            return "Reset done", 200

        # 🧩 Supabase-Sync beim ersten Mal
        if user_number not in synced_numbers:
            try:
                sync_users_from_supabase()
                synced_numbers.add(user_number)
                logger.info(f"✅ Supabase-Sync erfolgreich für {user_number}")
            except Exception as e:
                logger.error(f"❌ Fehler beim Supabase-Sync: {e}")

        # 🎧 Sprachnachricht erkennen & transkribieren
        if num_media > 0 and content_type.startswith("audio"):
            media_url = request.form.get("MediaUrl0")
            send_whatsapp_reply(user_number, "🎧 Ich höre kurz rein und antworte dir gleich...⏳")
            user_message = transcribe_voice_message(media_url)
            logger.info(f"🎤 Transkribierte Sprachnachricht von {user_number}: {user_message}")

        # ❌ Fallback falls keine Nachricht da
        if not user_message:
            logger.warning("❌ Keine Nachricht vorhanden.")
            return "No message content", 400

        # 💾 Verlauf speichern & laden
        save_message(user_number, "inbound", user_message)
        history = get_history(user_number)

        # 🤖 GPT-Antwort generieren (mit Zeitmessung)
        try:
            start = time.perf_counter()
            reply = get_next_response(user_number, history)
            duration = time.perf_counter() - start
            logger.info(f"🕓 GPT-Antwortzeit für {user_number}: {duration:.2f}s")
        except Exception as e:
            logger.exception(f"❌ Fehler bei GPT-Flow: {e}")
            reply = (
                "Es gab ein Problem mit meiner Antwort 😔 "
                "Magst du es später nochmal probieren?"
            )

        # 📤 Antwort senden & speichern
        send_whatsapp_reply(user_number, reply)
        save_message(user_number, "outbound", reply)

        return "OK", 200

    except Exception as e:
        logger.critical(f"🔥 Unerwarteter Webhook-Fehler: {e}")
        try:
            send_whatsapp_reply(user_number, "Etwas ist schiefgelaufen 😕 Bitte versuch es später nochmal.")
        except Exception as nested:
            logger.error(f"❗ Fehler beim Senden der Fehlerantwort: {nested}")
        return "Internal Server Error", 500