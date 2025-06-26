import json
from typing import List, Dict
from app.services.session_service import get_user_state, set_user_state, reset_user_state
from app.services.vector_store_services import find_top_matches
from app.services.openai_agent import generate_agent_response, generate_online_suggestions


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
            set_user_state(user_number, "agent_mode_help")
            return "Okay! Bitte beschreibe dein Anliegen so genau wie möglich."
        elif last_input == "2":
            set_user_state(user_number, "agent_mode_offer")
            return "Super! Was möchtest du anbieten und in welchem Bereich kannst du helfen?"
        elif last_input == "3":
            reset_user_state(user_number)
            return "Dein Profil ist aktuell leer. Du kannst später Infos hinterlegen."
        else:
            return (
                "Bitte antworte mit:\n"
                "1 - Ich suche Hilfe\n"
                "2 - Ich biete Hilfe\n"
                "3 - Mein Profil anzeigen"
            )

    elif state in ["agent_mode_help", "agent_mode_offer"]:
        mode = "suchen" if state == "agent_mode_help" else "bieten"
        matches = find_top_matches(last_input, top_k=5)

        set_user_state(user_number + "_query", last_input)
        set_user_state(user_number + "_matches", json.dumps(matches))
        set_user_state(user_number + "_mode", mode)
        set_user_state(user_number, "awaiting_online_search_confirmation")

        response = generate_agent_response(history, matches, mode=mode)
        response += (
            "\n\n🔍 Möchtest du, dass ich zusätzlich online nach passenden Lösungen suche?\n"
            "Antworte mit *ja* oder *nein*."
        )
        return response

    elif state == "awaiting_online_search_confirmation":
        if last_input.lower() in ["ja", "gern", "bitte", "okay", "ok"]:
            set_user_state(user_number, "awaiting_location_for_online_search")
            return (
                "Super! 📍 Sag mir bitte kurz, wo du dich ungefähr befindest "
                "(Stadtteil, PLZ oder Stadtname). So kann ich gezielter nach Hilfe suchen."
            )
        else:
            reset_user_state(user_number)
            return "Alles klar 😊 Wenn du später doch noch Hilfe brauchst, schreib einfach wieder. 👋"

    elif state == "awaiting_location_for_online_search":
        location = last_input.strip()
        query = get_user_state(user_number + "_query") or ""
        mode = get_user_state(user_number + "_mode") or "suchen"

        set_user_state(user_number, "followup_mode")
        set_user_state(user_number + "_followup_count", "0")

        suggestions = generate_online_suggestions(query=query, location=location, mode=mode)
        return suggestions + "\n\n💬 Hast du noch eine weitere Frage?"

    elif state == "followup_mode":
        count = int(get_user_state(user_number + "_followup_count") or "0")

        if count >= 2:
            reset_user_state(user_number)
            return (
                "Ich hoffe, ich konnte dir ein gutes Stück weiterhelfen 🙏\n\n"
                "Falls du noch offene Fragen hast oder persönliche Unterstützung brauchst, "
                "melde dich gern direkt bei *Wir helfen aus e.V.*:\n\n"
                "📞 Tel: 0173 7523673\n"
                "📧 Mail: Lemont-Kim@Wir-helfen-aus.de\n"
                "🌐 Website: https://www.wir-helfen-aus.de\n\n"
                "Alles Gute und bis bald! 💛"
            )
        else:
            updated_count = count + 1
            set_user_state(user_number + "_followup_count", str(updated_count))
            set_user_state(user_number, "followup_mode")

            followup_response = generate_agent_response(history, [], mode="suchen")
            return followup_response + "\n\n💬 Hast du noch eine weitere Frage?"

    else:
        reset_user_state(user_number)
        return "Etwas ist schiefgelaufen. Lass uns nochmal starten. Schreibe einfach 1, 2 oder 3."