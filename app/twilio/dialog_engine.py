from typing import List, Dict
from app.services.session_service import get_user_state, set_user_state, reset_user_state
from app.services.vector_store_services import find_top_matches
from app.services.post_service import generate_help_post


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
            set_user_state(user_number, "awaiting_offer_input")
            return "Klasse! Erzähl uns gern etwas über deine Fähigkeiten oder wie du helfen kannst."
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
        set_user_state(user_number, "offer_post_suggestion")
        set_user_state(user_number + "_query", last_input)

        if not matches:
            post_text = generate_help_post(last_input, mode="suchen")
            reset_user_state(user_number)
            return (
                f"Ich habe gerade niemanden gefunden, der direkt helfen kann.\n\n"
                f"Aber hier wäre ein Vorschlag für dein Hilfegesuch:\n\n📝 *{post_text}*"
            )

        response = "Hier sind passende Helfer:innen:\n\n"
        response += "\n".join(f"- {m}" for m in matches)
        response += "\n\nMöchtest du zusätzlich ein Hilfegesuch posten? Antworte mit *ja* oder *nein*."
        return response

    elif state == "offer_post_suggestion":
        if last_input.lower() in ["ja", "yes", "gern", "ok"]:
            original_input = get_user_state(user_number + "_query") or ""
            post_text = generate_help_post(original_input, mode="suchen")
            reset_user_state(user_number)
            return f"Alles klar! Hier ist dein Post-Vorschlag:\n\n📝 *{post_text}*"
        else:
            reset_user_state(user_number)
            return "Kein Problem! Du kannst dich jederzeit wieder melden, wenn du Hilfe brauchst. 👋"

    elif state == "awaiting_offer_input":
        set_user_state(user_number, "show_offer_post")
        set_user_state(user_number + "_query", last_input)
        return "Möchtest du, dass ich daraus einen passenden Post-Text für dein Hilfsangebot erstelle? (ja/nein)"

    elif state == "show_offer_post":
        if last_input.lower() in ["ja", "yes", "bitte", "ok"]:
            original_input = get_user_state(user_number + "_query") or ""
            post_text = generate_help_post(original_input, mode="bieten")
            reset_user_state(user_number)
            return f"Super! Hier ist ein Vorschlag für dein Hilfsangebot:\n\n📝 *{post_text}*"
        else:
            reset_user_state(user_number)
            return "Alles klar. Danke für dein Angebot! Wir melden uns bei Bedarf. 💪"

    else:
        reset_user_state(user_number)
        return "Etwas ist schiefgelaufen. Lass uns nochmal von vorne starten. Antworte mit 1, 2 oder 3."