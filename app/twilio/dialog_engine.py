# app/twilio/dialog_engine.py

from typing import List, Dict
from app.services.session_service import get_user_state, set_user_state, reset_user_state
from app.services.vector_store import find_top_matches


def get_next_response(user_number: str, history: List[Dict[str, str]]) -> str:
    state = get_user_state(user_number)

    last_input = next(
        (msg["message"].strip() for msg in reversed(history) if msg["direction"] == "inbound"),
        ""
    )

    if state == "initial":
        set_user_state(user_number, "awaiting_choice")
        return (
            "Hallo 👋! Ich bin der AushilfBot. Wie kann ich dir helfen?\n"
            "1 - Ich suche Hilfe\n"
            "2 - Ich biete Hilfe\n"
            "3 - Mein Profil anzeigen"
        )

    elif state == "awaiting_choice":
        if last_input == "1":
            set_user_state(user_number, "awaiting_help_desc")
            return "Super! Bitte beschreibe kurz, wobei du Unterstützung brauchst."
        elif last_input == "2":
            set_user_state(user_number, "awaiting_offer_desc")
            return "Klasse! Was für Hilfe möchtest du anbieten?"
        elif last_input == "3":
            reset_user_state(user_number)
            return "Dein Profil ist aktuell leer. Du kannst später Infos hinterlegen."
        else:
            return (
                "Das habe ich leider nicht verstanden. Antworte mit:\n"
                "1 - Ich suche Hilfe\n"
                "2 - Ich biete Hilfe\n"
                "3 - Mein Profil anzeigen"
            )

    elif state == "awaiting_help_desc":
        matches = find_top_matches(last_input, top_k=5)
        reset_user_state(user_number)

        if not matches:
            return "Leider habe ich aktuell niemanden gefunden, der helfen kann. Versuche es später erneut."

        response = "Hier sind einige passende Helfer:innen:\n\n"
        response += "\n".join(f"- {m}" for m in matches)
        response += "\n\nViel Erfolg! Du kannst jederzeit wieder eine Anfrage stellen. 👋"
        return response

    elif state == "awaiting_offer_desc":
        reset_user_state(user_number)
        return "Vielen Dank für dein Hilfsangebot! Wir speichern das und melden uns bei Bedarf bei dir. 💪"

    else:
        reset_user_state(user_number)
        return "Etwas ist schiefgelaufen. Lass uns nochmal von vorne starten. Antworte mit 1, 2 oder 3."