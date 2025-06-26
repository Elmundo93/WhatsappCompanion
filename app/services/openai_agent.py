from openai import OpenAI
from app.utils.config import OPENAI_API_KEY_MASTERSCHOOL


client = OpenAI(api_key=OPENAI_API_KEY_MASTERSCHOOL)
# ---------- 🧠 GPT: Lokale Hilfe & Matches -------------------------------------

def generate_agent_response(
    history: list[dict[str, str]],
    matches: list[dict[str, str]] = [],
    mode: str = "suchen",
    followup: bool = False
) -> str:
    """
    Erstellt eine GPT-Antwort basierend auf Chatverlauf, Matches und Anfrage-Modus.
    Optional: followup=True markiert es als Rückfrage.
    """
    user_role = "suchender" if mode == "suchen" else "helfender"

    # 📌 Systemprompt
    system_prompt = (
        f"Du bist ein empathischer WhatsApp-Assistent, der Nutzer:innen dabei hilft, über eine Nachbarschafts-App "
        f"Hilfe zu finden oder anzubieten. Achte auf einen freundlichen Ton, Klarheit und max. 3 Absätze. "
        f"Nenne konkrete Vorschläge oder stelle Rückfragen. Antworte WhatsApp-gerecht, Emoji erlaubt."
    )
    if followup:
        system_prompt += (
            "\nDies ist eine Rückfrage in einem laufenden Gespräch. Reagiere präzise und hilfreich, ohne alles zu wiederholen."
        )

    messages = [{"role": "system", "content": system_prompt}]

    # 📜 Kontextualisierter Verlauf
    for msg in history:
        role = "user" if msg["direction"] == "inbound" else "assistant"
        messages.append({"role": role, "content": msg["message"].strip()})

    # 🧩 Matches strukturiert bereitstellen
    if matches:
        match_text = "\n".join(
            f"👤 *{m['name']}*: {m['bio'].strip()}" for m in matches
        )
        summary = (
            "Hier sind mögliche passende Personen aus der App:\n\n"
            f"{match_text}"
        )
    else:
        summary = "Es wurden keine direkten Personen gefunden, die gut passen."

    messages.append({
        "role": "system",
        "content": f"Zusätzliche Info (nicht zeigen, aber nutzen):\n{summary}"
    })

    # 👉 Aufforderung zur Antwort
    messages.append({
        "role": "user",
        "content": "Kannst du mir jetzt bitte helfen oder etwas vorschlagen?"
    })

    # 💬 GPT-Antwort
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
        max_tokens=400,
    )

    return response.choices[0].message.content.strip()

# ---------- 🌍 GPT: Externe Online-Suche -------------------------------------

def generate_online_suggestions(query: str, location: str = "", mode: str = "suchen") -> str:
    """
    Erstellt externe Vorschläge basierend auf Anliegen und (optionalem) Standort.
    """
    user_role = "um Hilfe zu erhalten" if mode == "suchen" else "um Hilfe anzubieten"
    location_text = f" in {location}" if location else ""

    prompt = (
        f"Ein Nutzer möchte {user_role}. Das Anliegen lautet:\n\n\"{query}\"\n\n"
        f"Der Standort ist{location_text}.\n\n"
        "Erstelle eine WhatsApp-optimierte Antwort mit 2–3 konkreten externen Tipps oder Plattformen:\n"
        "- 🎯 *Titel (fett)*\n"
        "- 1 kurze Erklärung\n"
        "- 📎 Weblink \n\n"
        "Antwort max. 3 Absätze. Klar, hilfreich, empathisch. Keine Floskeln."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Du bist ein Recherche-Assistent für soziale Hilfen."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()

